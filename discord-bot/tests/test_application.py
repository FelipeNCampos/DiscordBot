"""Casos de uso executados com portas em memória, sem Discord, HTTP ou SQLite."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from bot.application.use_cases.instagram_notifications import PollInstagramMedia
from bot.application.use_cases.instagram_token_refresh import (
    InstagramRefreshPolicy,
    RefreshInstagramToken,
)
from bot.application.use_cases.twitch_notifications import NotifyTwitchLive, ReceiveTwitchEvent
from bot.domain.models import (
    InstagramMedia,
    InstagramTokenData,
    InstagramTokenRefreshResult,
    TwitchOnlineEvent,
    TwitchStream,
)


def twitch_event() -> TwitchOnlineEvent:
    return TwitchOnlineEvent(
        "event-1", "stream.online", "123", "canal", "Canal", None, datetime.now(UTC)
    )


@pytest.mark.parametrize("is_new", [True, False])
async def test_twitch_event_is_only_queued_when_new(is_new: bool) -> None:
    repository = SimpleNamespace(register_twitch_event=AsyncMock(return_value=is_new))
    queue = SimpleNamespace(queue_twitch_notification=Mock())
    event = twitch_event()

    await ReceiveTwitchEvent(repository, queue).execute(event)

    repository.register_twitch_event.assert_awaited_once_with(event)
    assert queue.queue_twitch_notification.call_count == int(is_new)


@pytest.mark.parametrize("is_live", [True, False])
async def test_twitch_delivery_checks_stream_and_records_result(is_live: bool) -> None:
    stream = TwitchStream("Live", "https://twitch.tv/canal", is_live=is_live)
    client = SimpleNamespace(get_stream=AsyncMock(return_value=stream))
    repository = SimpleNamespace(update_twitch_event_status=AsyncMock())
    current_live = SimpleNamespace(set_current=AsyncMock())
    sender = SimpleNamespace(send_twitch_notification=AsyncMock())
    event = twitch_event()

    await NotifyTwitchLive(client, repository, current_live, sender).execute(event)

    current_live.set_current.assert_awaited_once_with(event, stream)
    assert sender.send_twitch_notification.await_count == int(is_live)
    repository.update_twitch_event_status.assert_awaited_once_with(
        event.message_id, "notified" if is_live else "offline"
    )


async def test_twitch_failed_delivery_is_recorded_and_propagated() -> None:
    client = SimpleNamespace(get_stream=AsyncMock(return_value=TwitchStream("Live", "url")))
    repository = SimpleNamespace(update_twitch_event_status=AsyncMock())
    current_live = SimpleNamespace(set_current=AsyncMock())
    sender = SimpleNamespace(send_twitch_notification=AsyncMock(side_effect=RuntimeError("envio")))
    event = twitch_event()

    with pytest.raises(RuntimeError, match="envio"):
        await NotifyTwitchLive(client, repository, current_live, sender).execute(event)

    repository.update_twitch_event_status.assert_awaited_once_with(event.message_id, "failed")


async def test_instagram_retries_initial_sync_without_announcing_historical_media() -> None:
    media = InstagramMedia("media-1", "perfil", None, "IMAGE", None, None, "url", datetime.now(UTC))
    client = SimpleNamespace(list_recent_media=AsyncMock(return_value=[media]))
    repository = SimpleNamespace(
        has_processed_instagram_media=AsyncMock(return_value=False),
        mark_instagram_media_processed=AsyncMock(side_effect=[RuntimeError("banco"), None]),
    )
    sender = SimpleNamespace(send_instagram_notification=AsyncMock())
    poll = PollInstagramMedia(client, repository, sender)

    with pytest.raises(RuntimeError, match="banco"):
        await poll.execute()
    await poll.execute()

    sender.send_instagram_notification.assert_not_awaited()
    repository.mark_instagram_media_processed.assert_awaited_with(media, status="known")


async def test_refresh_preserves_account_metadata_at_the_application_boundary() -> None:
    now = datetime(2026, 10, 24, tzinfo=UTC)
    token = InstagramTokenData(
        "old", "bearer", now + timedelta(days=2), now, user_id="123", username="perfil"
    )
    result = InstagramTokenRefreshResult("new", "bearer", 86400 * 60, now + timedelta(days=60))
    client = SimpleNamespace(refresh_access_token=AsyncMock(return_value=result))
    store = SimpleNamespace(get_token=AsyncMock(return_value=token), save_token=AsyncMock())
    refresh = RefreshInstagramToken(
        InstagramRefreshPolicy(True, 10, 24), client, store, now=lambda: now
    )

    await refresh.execute()

    saved = store.save_token.await_args.args[0]
    assert saved.access_token == "new"
    assert saved.user_id == "123"
    assert saved.username == "perfil"
    assert refresh.last_status == "refreshed"
