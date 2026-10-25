"""Registros administrativos com filtros, isolamento por servidor e conteúdo mínimo."""

from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import AsyncMock

import discord
import pytest

from bot.application.use_cases.server_activity import RecordServerActivity
from bot.config.settings import ConfigurationError, Settings
from bot.domain.activity import ServerActivity
from bot.presentation.discord.activity_log_sender import ActivityLogSender
from bot.presentation.discord.cogs.member_activity_logs import MemberActivityLogs


def activity(**changes: object) -> ServerActivity:
    event = ServerActivity("channels", "Canal criado", 1, 123, details=("Nome: geral",))
    return replace(event, **changes)


def test_activity_configuration_validates_channel_and_categories() -> None:
    settings = Settings.from_environment(
        {
            "DISCORD_TOKEN": "test",
            "DISCORD_ACTIVITY_LOG_CHANNEL_ID": "123",
            "DISCORD_ACTIVITY_LOG_EVENTS": " members, messages,members ",
        }
    )
    assert settings.activity_log_channel_id == 123
    assert settings.activity_log_events == frozenset({"members", "messages"})
    with pytest.raises(ConfigurationError, match="DISCORD_ACTIVITY_LOG_EVENTS"):
        Settings.from_environment(
            {"DISCORD_TOKEN": "test", "DISCORD_ACTIVITY_LOG_EVENTS": "unknown"}
        )


async def test_activity_use_case_only_publishes_enabled_categories() -> None:
    publisher = SimpleNamespace(publish=AsyncMock())
    recorder = RecordServerActivity(publisher, frozenset({"members"}))
    await recorder.execute(activity())
    publisher.publish.assert_not_awaited()
    await recorder.execute(activity(category="members"))
    publisher.publish.assert_awaited_once()


async def test_activity_sender_rejects_a_channel_from_another_server() -> None:
    channel = SimpleNamespace(guild=SimpleNamespace(id=2), send=AsyncMock())
    bot = SimpleNamespace(get_channel=lambda _: channel, fetch_channel=AsyncMock())
    sender = ActivityLogSender(bot, activity_channel_id=456)
    await sender.publish(activity())
    channel.send.assert_not_awaited()


async def test_activity_sender_prevents_mentions_and_skips_its_own_log_channels() -> None:
    channel = SimpleNamespace(guild=SimpleNamespace(id=1), send=AsyncMock())
    bot = SimpleNamespace(get_channel=lambda _: channel, fetch_channel=AsyncMock())
    sender = ActivityLogSender(bot, activity_channel_id=456)
    await sender.publish(activity(details=("@everyone <@123> **nome**",)))
    mentions = channel.send.await_args.kwargs["allowed_mentions"]
    assert isinstance(mentions, discord.AllowedMentions)
    assert not mentions.everyone and not mentions.users and not mentions.roles
    channel.send.reset_mock()
    await sender.publish(activity(category="messages", channel_id=456))
    channel.send.assert_not_awaited()


async def test_delivery_failure_does_not_break_other_bot_events() -> None:
    response = SimpleNamespace(status=403, reason="forbidden", headers={})
    channel = SimpleNamespace(
        guild=SimpleNamespace(id=1),
        send=AsyncMock(side_effect=discord.Forbidden(response, "test")),
    )
    bot = SimpleNamespace(get_channel=lambda _: channel, fetch_channel=AsyncMock())
    await ActivityLogSender(bot, activity_channel_id=456).publish(activity())


def event_cog(
    categories: str = "members,moderation,channels,roles,messages",
) -> tuple[MemberActivityLogs, SimpleNamespace]:
    channel = SimpleNamespace(guild=SimpleNamespace(id=1), send=AsyncMock())
    bot = SimpleNamespace(
        user=SimpleNamespace(id=99),
        get_channel=lambda _: channel,
        fetch_channel=AsyncMock(),
    )
    settings = Settings.from_environment(
        {
            "DISCORD_TOKEN": "test",
            "DISCORD_ACTIVITY_LOG_CHANNEL_ID": "456",
            "DISCORD_ACTIVITY_LOG_EVENTS": categories,
        }
    )
    return MemberActivityLogs(bot, settings), channel


async def test_raw_message_events_do_not_copy_content_or_fetch_deleted_messages() -> None:
    cog, channel = event_cog()
    payload = SimpleNamespace(
        guild_id=1,
        channel_id=20,
        message_id=30,
        cached_message=None,
        data={"content": "conteudo-secreto", "attachments": [{"url": "anexo-secreto"}]},
    )
    await cog.on_raw_message_edit(payload)
    await cog.on_raw_message_delete(payload)
    assert channel.send.await_count == 2
    for call in channel.send.await_args_list:
        assert "conteudo-secreto" not in call.args[0]
        assert "anexo-secreto" not in call.args[0]
        assert "30" in call.args[0]


async def test_message_logs_are_disabled_by_default_and_ignore_private_events() -> None:
    cog, channel = event_cog("members,moderation,channels,roles")
    payload = SimpleNamespace(guild_id=1, channel_id=20, message_id=30, cached_message=None)
    await cog.on_raw_message_delete(payload)
    channel.send.assert_not_awaited()
    cog, channel = event_cog()
    payload.guild_id = None
    await cog.on_raw_message_delete(payload)
    channel.send.assert_not_awaited()


async def test_bulk_delete_produces_one_summary_and_embed_updates_do_not_log() -> None:
    cog, channel = event_cog()
    await cog.on_raw_bulk_message_delete(
        SimpleNamespace(
            guild_id=1,
            channel_id=20,
            message_ids={1, 2, 3},
        )
    )
    assert channel.send.await_count == 1
    assert "Quantidade: 3" in channel.send.await_args.args[0]
    await cog.on_raw_message_edit(SimpleNamespace(guild_id=1, data={"embeds": []}))
    assert channel.send.await_count == 1


async def test_member_update_groups_role_changes_and_ignores_unrelated_updates() -> None:
    cog, channel = event_cog()
    before = SimpleNamespace(
        id=7,
        guild=SimpleNamespace(id=1),
        roles=[SimpleNamespace(id=10)],
        nick=None,
        timed_out_until=None,
    )
    after = SimpleNamespace(**vars(before))
    await cog.on_member_update(before, after)
    channel.send.assert_not_awaited()
    after.roles = [SimpleNamespace(id=11)]
    await cog.on_member_update(before, after)
    assert channel.send.await_count == 1
    assert "adicionados: 11" in channel.send.await_args.args[0]
    assert "removidos: 10" in channel.send.await_args.args[0]


async def test_channel_topic_changes_log_only_the_changed_attribute() -> None:
    cog, channel = event_cog()
    before = SimpleNamespace(id=7, guild=SimpleNamespace(id=1), topic="topico-antigo-secreto")
    after = SimpleNamespace(id=7, guild=before.guild, topic="topico-novo-secreto")
    await cog.on_guild_channel_update(before, after)
    text = channel.send.await_args.args[0]
    assert "tópico" in text
    assert "secreto" not in text


async def test_moderation_events_record_targets_without_inventing_an_actor() -> None:
    cog, channel = event_cog()
    await cog.on_member_ban(SimpleNamespace(id=1), SimpleNamespace(id=7))
    await cog.on_member_unban(SimpleNamespace(id=1), SimpleNamespace(id=7))
    assert channel.send.await_count == 2
    assert "Membro banido" in channel.send.await_args_list[0].args[0]
    assert "Banimento removido" in channel.send.await_args_list[1].args[0]
    assert all("ID: 7" in call.args[0] for call in channel.send.await_args_list)
