"""Diagnóstico sem credenciais e sem importar modelos do Discord no caso de uso."""

from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import discord

from bot.application.use_cases.server_diagnostics import diagnose_server
from bot.config.settings import Settings
from bot.domain.diagnostics import ChannelSnapshot, RoleSnapshot, ServerSnapshot
from bot.presentation.discord.cogs.server_administration import ServerAdministration
from bot.presentation.discord.server_snapshot import collect_server_snapshot


def test_diagnostics_reports_channel_permissions_and_role_hierarchy() -> None:
    report = diagnose_server(
        ServerSnapshot(
            connected=True,
            latency_ms=45,
            members_intent=True,
            moderation_intent=True,
            messages_intent=True,
            bot_member_available=True,
            channels=(
                ChannelSnapshot(
                    "Logs",
                    "DISCORD_ACTIVITY_LOG_CHANNEL_ID",
                    123,
                    exists=True,
                    same_guild=True,
                    valid_type=True,
                    missing_permissions=("Enviar mensagens",),
                ),
            ),
            roles=(RoleSnapshot("Cargo automático", 456, exists=True, assignable=False),),
        )
    )
    assert report.has_errors
    assert any("Enviar mensagens" in check.detail for check in report.checks)
    assert any("hierarquia" in check.detail for check in report.checks)


def test_diagnostics_distinguishes_disabled_features_from_errors() -> None:
    report = diagnose_server(
        ServerSnapshot(
            connected=True,
            latency_ms=45,
            members_intent=True,
            moderation_intent=True,
            messages_intent=True,
            bot_member_available=True,
            channels=(ChannelSnapshot("Logs", "DISCORD_ACTIVITY_LOG_CHANNEL_ID", None),),
        )
    )
    assert not report.has_errors
    assert any(check.status == "disabled" for check in report.checks)


def test_an_enabled_integration_without_its_channel_is_an_error() -> None:
    report = diagnose_server(
        ServerSnapshot(
            connected=True,
            latency_ms=45,
            members_intent=True,
            moderation_intent=True,
            messages_intent=True,
            bot_member_available=True,
            channels=(
                ChannelSnapshot(
                    "Instagram",
                    "DISCORD_INSTAGRAM_CHANNEL_ID",
                    None,
                    required=True,
                ),
            ),
        )
    )
    assert report.has_errors
    assert report.checks[-1].status == "error"


def test_public_activity_channel_is_reported_as_a_privacy_warning() -> None:
    report = diagnose_server(
        ServerSnapshot(
            connected=True,
            latency_ms=45,
            members_intent=True,
            moderation_intent=True,
            messages_intent=True,
            bot_member_available=True,
            channels=(
                ChannelSnapshot(
                    "Logs",
                    "DISCORD_ACTIVITY_LOG_CHANNEL_ID",
                    123,
                    exists=True,
                    same_guild=True,
                    valid_type=True,
                    publicly_visible=True,
                ),
            ),
        )
    )
    assert report.checks[-1].status == "warning"
    assert "@everyone" in report.checks[-1].detail


def test_diagnostics_does_not_claim_portal_intents_are_verified() -> None:
    report = diagnose_server(
        ServerSnapshot(
            connected=False,
            latency_ms=None,
            members_intent=False,
            moderation_intent=True,
            messages_intent=True,
            bot_member_available=False,
        )
    )
    assert report.has_errors
    assert any("Developer Portal" in check.detail for check in report.checks)


async def test_diagnostics_checks_permissions_before_reading_server_state() -> None:
    settings = Settings.from_environment({"DISCORD_TOKEN": "test"})
    interaction = SimpleNamespace(
        permissions=SimpleNamespace(manage_guild=False),
        response=SimpleNamespace(
            send_message=AsyncMock(),
            defer=AsyncMock(),
        ),
    )
    cog = ServerAdministration(SimpleNamespace(), settings)
    await ServerAdministration.diagnostics.callback(cog, interaction)
    interaction.response.send_message.assert_awaited_once()
    assert interaction.response.send_message.await_args.kwargs["ephemeral"] is True
    interaction.response.defer.assert_not_awaited()


async def test_diagnostics_returns_private_report_without_secrets() -> None:
    settings = Settings.from_environment({"DISCORD_TOKEN": "nao-expor-esse-token"})
    guild = SimpleNamespace(id=1, member_count=12, channels=[], roles=[], me=None)
    bot = SimpleNamespace(is_ready=lambda: True, latency=0.05, intents=discord.Intents.all())
    interaction = SimpleNamespace(
        permissions=SimpleNamespace(manage_guild=True),
        guild=guild,
        response=SimpleNamespace(defer=AsyncMock()),
        followup=SimpleNamespace(send=AsyncMock()),
    )
    await ServerAdministration.diagnostics.callback(
        ServerAdministration(bot, settings), interaction
    )
    args = interaction.followup.send.await_args.kwargs
    assert args["ephemeral"] is True
    assert 1 <= len(args["embeds"]) <= 10
    assert all(len(embed.fields) <= 25 and len(embed) <= 6000 for embed in args["embeds"])
    assert settings.discord_token not in str([embed.to_dict() for embed in args["embeds"]])


def test_snapshot_reports_cross_server_channels_without_reading_their_permissions() -> None:
    foreign = SimpleNamespace(guild=SimpleNamespace(id=2))
    guild = SimpleNamespace(id=1, me=None, get_channel=lambda _: None)
    bot = SimpleNamespace(
        is_ready=lambda: True,
        latency=0.05,
        intents=discord.Intents.all(),
        get_channel=lambda _: foreign,
    )
    settings = replace(
        Settings.from_environment({"DISCORD_TOKEN": "test"}), activity_log_channel_id=123
    )
    report = diagnose_server(collect_server_snapshot(bot, guild, settings))
    assert any("outro servidor" in check.detail for check in report.checks)


def test_snapshot_uses_effective_channel_permissions_and_everyone_visibility() -> None:
    member = SimpleNamespace()
    everyone = SimpleNamespace()
    channel = Mock(spec=discord.TextChannel)
    guild = SimpleNamespace(id=1, me=member, default_role=everyone, get_channel=lambda _: channel)
    channel.guild = guild

    def permissions_for(principal: object) -> discord.Permissions:
        return discord.Permissions(view_channel=True, send_messages=principal is member)

    channel.permissions_for.side_effect = permissions_for
    bot = SimpleNamespace(
        is_ready=lambda: True,
        latency=0.05,
        intents=discord.Intents.all(),
        get_channel=lambda _: channel,
    )
    settings = replace(
        Settings.from_environment({"DISCORD_TOKEN": "test"}), activity_log_channel_id=123
    )
    report = diagnose_server(collect_server_snapshot(bot, guild, settings))
    log_check = next(check for check in report.checks if check.label == "Logs de atividade")
    assert log_check.status == "warning"
    assert "@everyone" in log_check.detail
    channel.permissions_for.side_effect = lambda _: discord.Permissions(view_channel=True)
    report = diagnose_server(collect_server_snapshot(bot, guild, settings))
    log_check = next(check for check in report.checks if check.label == "Logs de atividade")
    assert log_check.status == "error"
    assert "Enviar mensagens" in log_check.detail
