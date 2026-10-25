"""Verifica o carregamento real das extensões sem conectar ao Discord."""

from collections.abc import Callable
from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot.config.settings import Settings
from bot.infra.memory.current_twitch_live import CurrentTwitchLiveStore
from bot.presentation.discord.client import DiscordBot


async def test_bot_loads_every_extension_with_injected_dependencies(
    environment: Callable[[], dict[str, str]],
) -> None:
    settings = replace(
        Settings.from_environment(environment()),
        discord_guild_id=None,
        sync_global_commands=False,
    )
    store = SimpleNamespace(update_twitch_event_status=AsyncMock())
    audio = SimpleNamespace(get_audio_source=AsyncMock())
    bot = DiscordBot(
        settings,
        store=store,
        current_twitch_live=CurrentTwitchLiveStore(),
        audio_service=audio,
        growth_repository=SimpleNamespace(start_tracking=AsyncMock(), record_event=AsyncMock()),
    )

    async with bot:
        await bot.setup_hook()

        assert set(bot.cogs) == {
            "General",
            "MediaReactions",
            "RoleManagement",
            "MemberActivityLogs",
            "ServerAdministration",
            "ServerGrowth",
            "TemporaryVoice",
            "Music",
        }
        assert {command.name for command in bot.tree.get_commands()} == {
            "ping",
            "chamar",
            "id_usuario",
            "boasvindas",
            "reenviar_live",
            "reenviar_reel",
            "reenviar_post",
            "comandos",
            "limpar",
            "tocar_youtube",
            "parar_musica",
            "sair_call",
            "configurar-cargos",
            "diagnostico",
            "crescimento",
        }
        assert bot.audio_service is audio

        interaction = SimpleNamespace(response=SimpleNamespace(send_message=AsyncMock()))
        general = bot.get_cog("General")
        await general.commands_list.callback(general, interaction)
        help_embed = interaction.response.send_message.await_args.kwargs["embed"]
        assert "/diagnostico" in {field.name for field in help_embed.fields}
        assert "/crescimento" in {field.name for field in help_embed.fields}
        assert "/configurar-cargos" in {field.name for field in help_embed.fields}

    assert bot.is_closed()
