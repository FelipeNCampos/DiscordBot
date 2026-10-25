"""Consulta a live configurada e confirma seu estado antes de um reenvio."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from bot.application.errors import TwitchError
from bot.application.ports import CurrentTwitchLiveRepository, TwitchStreamClient
from bot.domain.models import CurrentTwitchLive, TwitchOnlineEvent

logger = logging.getLogger(__name__)


class GetCurrentTwitchLive:
    def __init__(
        self,
        current_live: CurrentTwitchLiveRepository | None,
        client: TwitchStreamClient | None,
    ) -> None:
        self._current_twitch_live = current_live
        self._twitch_client = client

    async def execute(self) -> CurrentTwitchLive | None:
        """Obtém a live atual e confirma que ela ainda está online antes do reenvio."""
        live = (
            await self._current_twitch_live.get_current()
            if self._current_twitch_live is not None
            else None
        )
        if live is not None:
            if not live.stream.is_live:
                await self._current_twitch_live.clear_if_current(live)
                return None
            if self._twitch_client is None:
                return live

            latest_stream = await self._twitch_client.get_stream(live.event.broadcaster_user_id)
            return await self._current_twitch_live.update_stream_if_current(live, latest_stream)

        if self._twitch_client is None:
            return None

        try:
            (
                broadcaster_user_id,
                broadcaster_login,
                broadcaster_name,
            ) = await self._twitch_client.get_user_by_login()
        except TwitchError:
            logger.exception("Não foi possível verificar a live Twitch configurada.")
            return None

        stream = await self._twitch_client.get_stream(broadcaster_user_id)
        if not stream.is_live:
            return None

        event = TwitchOnlineEvent(
            message_id="manual-live-resend",
            event_type="stream.online",
            broadcaster_user_id=broadcaster_user_id,
            broadcaster_login=broadcaster_login,
            broadcaster_name=broadcaster_name,
            started_at=None,
            received_at=datetime.now(UTC),
        )
        return CurrentTwitchLive(event, stream)
