"""Comandos gerais do bot."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import cast

import discord
from discord import app_commands
from discord.ext import commands

from bot.application.errors import DiscordNotificationError, InstagramAPIError, TwitchError
from bot.application.ports import (
    CurrentTwitchLiveRepository,
    InstagramMediaClient,
    TwitchStreamClient,
)
from bot.application.use_cases.current_twitch_live import GetCurrentTwitchLive
from bot.config.settings import DEFAULT_MAX_MESSAGES_TO_DELETE
from bot.domain.media import is_instagram_post, is_instagram_reel
from bot.domain.models import CurrentTwitchLive, InstagramMedia
from bot.presentation.discord.client import DiscordBot
from bot.presentation.discord.command_help import COMMAND_HELP, MUSIC_COMMAND_HELP
from bot.presentation.discord.errors import (
    MISSING_MANAGE_GUILD_PERMISSION_MESSAGE,
    MISSING_MANAGE_MESSAGES_PERMISSION_MESSAGE,
)
from bot.presentation.discord.notification_sender import DiscordNotificationSender

logger = logging.getLogger(__name__)

NO_OPEN_TWITCH_LIVE_MESSAGE = "Não há nenhuma live aberta para reenviar no momento."
TWITCH_RESEND_ERROR_MESSAGE = "Não foi possível reenviar a notificação da live."
INSTAGRAM_NOT_CONFIGURED_MESSAGE = "As notificações do Instagram não estão configuradas."
NO_INSTAGRAM_MEDIA_MESSAGE = "Não encontrei nenhuma publicação do Instagram para reenviar."
INSTAGRAM_RESEND_ERROR_MESSAGE = "Não foi possível reenviar a notificação do Instagram."
CLEANUP_NOT_FOUND_MESSAGE = "Não encontrei as mensagens que deveriam ser apagadas."
CLEANUP_HTTP_ERROR_MESSAGE = "O Discord não conseguiu apagar as mensagens. Tente novamente."
CLEANUP_DM_MESSAGE = "Este comando só pode ser usado em um servidor."
CALL_NOT_CONFIGURED_MESSAGE = "O moderador para o comando /chamar não está configurado."
CALL_DELIVERY_ERROR_MESSAGE = "Não foi possível avisar o moderador. Tente novamente mais tarde."


class General(commands.Cog):
    """Agrupa comandos slash de uso geral."""

    def __init__(
        self,
        notification_sender: DiscordNotificationSender,
        current_twitch_live: CurrentTwitchLiveRepository | None = None,
        twitch_client: TwitchStreamClient | None = None,
        max_messages_to_delete: int = DEFAULT_MAX_MESSAGES_TO_DELETE,
        temporary_voice_creator_channel_id: int | None = None,
        instagram_client: InstagramMediaClient | None = None,
        call_moderator_user_id: int | None = None,
        discord_client: discord.Client | None = None,
    ) -> None:
        self._notification_sender = notification_sender
        self._get_live = GetCurrentTwitchLive(current_twitch_live, twitch_client)
        self._twitch_client = twitch_client
        self._max_messages_to_delete = max_messages_to_delete
        self._temporary_voice_creator_channel_id = temporary_voice_creator_channel_id
        self._instagram_client = instagram_client
        self._call_moderator_user_id = call_moderator_user_id
        self._discord_client = discord_client

    @app_commands.command(name="ping", description="Verifica se o bot está respondendo.")
    async def ping(self, interaction: discord.Interaction) -> None:
        """Responde a um teste simples de conectividade."""
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="chamar", description="Envia um aviso privado ao moderador.")
    @app_commands.guild_only()
    async def call_moderator(self, interaction: discord.Interaction) -> None:
        """Avisa, por DM, o moderador definido na configuração do ambiente."""
        moderator_id = self._call_moderator_user_id
        if moderator_id is None or self._discord_client is None:
            await interaction.response.send_message(CALL_NOT_CONFIGURED_MESSAGE, ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        moderator = self._discord_client.get_user(moderator_id)
        try:
            if moderator is None:
                moderator = await self._discord_client.fetch_user(moderator_id)
            caller_name = getattr(interaction.user, "display_name", None) or getattr(
                interaction.user, "name", "um membro"
            )
            await moderator.send(
                f"📣 {caller_name} pediu a atenção de um moderador. (ID: {interaction.user.id})",
                allowed_mentions=discord.AllowedMentions.none(),
            )
        except discord.Forbidden:
            logger.warning("Não foi possível enviar /chamar ao moderador %s.", moderator_id)
            await interaction.followup.send(CALL_DELIVERY_ERROR_MESSAGE, ephemeral=True)
            return
        except discord.NotFound:
            logger.warning("Moderador configurado para /chamar não encontrado: %s.", moderator_id)
            await interaction.followup.send(CALL_DELIVERY_ERROR_MESSAGE, ephemeral=True)
            return
        except discord.HTTPException as error:
            logger.warning(
                "Falha HTTP ao executar /chamar para moderador %s: status=%s.",
                moderator_id,
                error.status,
            )
            await interaction.followup.send(CALL_DELIVERY_ERROR_MESSAGE, ephemeral=True)
            return

        await interaction.followup.send("O moderador foi avisado.", ephemeral=True)

    @app_commands.command(name="id_usuario", description="Exibe o ID Discord de um usuário.")
    async def user_id_command(
        self, interaction: discord.Interaction, usuario: discord.User
    ) -> None:
        """Retorna de forma privada o ID do usuário informado."""
        await interaction.response.send_message(
            f"ID de {usuario.display_name}: `{usuario.id}`",
            ephemeral=True,
        )

    @app_commands.command(
        name="boasvindas",
        description="Envia uma mensagem privada de boas-vindas para um usuário.",
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def welcome_command(
        self,
        interaction: discord.Interaction,
        user: discord.User,
    ) -> None:
        """Dispara uma DM de boas-vindas para o usuário selecionado."""
        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(
                MISSING_MANAGE_GUILD_PERMISSION_MESSAGE,
                ephemeral=True,
            )
            return

        try:
            await self._notification_sender.send_welcome_message(user)
        except DiscordNotificationError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "A tentativa de envio da mensagem de boas-vindas foi realizada.",
        )

    @app_commands.command(
        name="reenviar_live",
        description="Reenvia a notificação da última live aberta.",
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def resend_live_command(self, interaction: discord.Interaction) -> None:
        """Reenvia pelo fluxo habitual a última notificação Twitch ainda aberta."""
        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(
                MISSING_MANAGE_GUILD_PERMISSION_MESSAGE,
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        try:
            live = await self._get_current_open_twitch_live()
        except TwitchError:
            logger.exception("Não foi possível confirmar o estado atual da live Twitch.")
            await interaction.followup.send(TWITCH_RESEND_ERROR_MESSAGE, ephemeral=True)
            return
        if live is None:
            await interaction.followup.send(NO_OPEN_TWITCH_LIVE_MESSAGE, ephemeral=True)
            return

        try:
            await self._notification_sender.send_twitch_notification(live.event, live.stream)
        except DiscordNotificationError:
            logger.exception("Falha ao reenviar a notificação manual da live Twitch.")
            await interaction.followup.send(TWITCH_RESEND_ERROR_MESSAGE, ephemeral=True)
            return

        broadcaster = live.event.broadcaster_name or live.event.broadcaster_login
        await interaction.followup.send(
            f"A notificação da live de {broadcaster} foi reenviada com sucesso.",
            ephemeral=True,
        )

    @app_commands.command(
        name="reenviar_reel", description="Reenvia o Reel mais recente do Instagram."
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def resend_instagram_reel_command(self, interaction: discord.Interaction) -> None:
        """Reenvia o Reel Instagram mais recente sem alterar seu estado de processamento."""
        await self._resend_instagram_media(interaction, is_instagram_reel, "Reel")

    @app_commands.command(
        name="reenviar_post", description="Reenvia o post mais recente do Instagram."
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def resend_instagram_post_command(self, interaction: discord.Interaction) -> None:
        """Reenvia o post Instagram mais recente sem alterar seu estado de processamento."""
        await self._resend_instagram_media(interaction, is_instagram_post, "post")

    async def _resend_instagram_media(
        self,
        interaction: discord.Interaction,
        predicate: Callable[[InstagramMedia], bool],
        media_label: str,
    ) -> None:
        """Busca e reenvia a última mídia Instagram que corresponde ao tipo solicitado."""
        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(
                MISSING_MANAGE_GUILD_PERMISSION_MESSAGE,
                ephemeral=True,
            )
            return
        if self._instagram_client is None:
            await interaction.response.send_message(
                INSTAGRAM_NOT_CONFIGURED_MESSAGE,
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        try:
            media_items = await self._instagram_client.list_recent_media()
        except InstagramAPIError:
            logger.exception("Falha ao consultar a mídia Instagram para reenvio manual.")
            await interaction.followup.send(INSTAGRAM_RESEND_ERROR_MESSAGE, ephemeral=True)
            return

        media = max(
            (item for item in media_items if predicate(item)),
            key=lambda item: item.timestamp,
            default=None,
        )
        if media is None:
            await interaction.followup.send(
                f"Não encontrei nenhum {media_label} do Instagram para reenviar.",
                ephemeral=True,
            )
            return

        try:
            await self._notification_sender.send_instagram_notification(media)
        except DiscordNotificationError:
            logger.exception("Falha ao reenviar manualmente a notificação Instagram.")
            await interaction.followup.send(INSTAGRAM_RESEND_ERROR_MESSAGE, ephemeral=True)
            return

        await interaction.followup.send(
            f"A notificação do {media_label} mais recente do Instagram foi reenviada com sucesso.",
            ephemeral=True,
        )

    @app_commands.command(name="comandos", description="Lista os comandos disponíveis do bot.")
    async def commands_list(self, interaction: discord.Interaction) -> None:
        """Exibe os comandos efetivamente registrados neste cog e suas formas de uso."""
        embed = discord.Embed(
            title="Comandos do Morcegão",
            description=(
                "Sou o Morcegão, fiel pet do Vampirão. Veja abaixo os comandos disponíveis."
            ),
            colour=0x9146FF,
        )

        tree = getattr(self._discord_client, "tree", None)
        registered_commands = tree.get_commands() if tree is not None else self.get_app_commands()
        music_help = dict(MUSIC_COMMAND_HELP)
        for command in registered_commands:
            description, usage, permission = COMMAND_HELP.get(
                command.name,
                (command.description, f"/{command.qualified_name}", "consulte um administrador."),
            )
            limit_hint = (
                "\nExemplo: `/limpar quantidade:10`\nLimite: "
                f"{self._max_messages_to_delete} mensagens por vez."
                if command.name == "limpar"
                else ""
            )
            embed.add_field(
                name=f"/{command.qualified_name}",
                value=music_help.get(
                    f"/{command.qualified_name}",
                    f"{description}\nUso: `{usage}`{limit_hint}\nPermissão: {permission}",
                ),
                inline=False,
            )

        if tree is None:
            for name, value in MUSIC_COMMAND_HELP:
                embed.add_field(name=name, value=value, inline=False)

        if self._temporary_voice_creator_channel_id is not None:
            embed.add_field(
                name="Canais temporários de voz",
                value=(
                    "Entre no canal criador configurado para o Morcegão criar uma sala "
                    "exclusiva para você. Você será movido automaticamente e poderá "
                    "personalizar nome, limite e permissões da própria sala. Quando todos "
                    "saírem, a sala será excluída automaticamente."
                ),
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="limpar", description="Apaga mensagens anteriores deste canal.")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def limpar(self, interaction: discord.Interaction, quantidade: int) -> None:
        """Apaga até a quantidade solicitada de mensagens anteriores no próprio canal."""
        if not interaction.permissions.manage_messages:
            await interaction.response.send_message(
                MISSING_MANAGE_MESSAGES_PERMISSION_MESSAGE,
                ephemeral=True,
            )
            return
        if quantidade <= 0:
            await interaction.response.send_message(
                "Informe uma quantidade maior que zero.", ephemeral=True
            )
            return
        if quantidade > self._max_messages_to_delete:
            await interaction.response.send_message(
                f"Você pode apagar no máximo {self._max_messages_to_delete} mensagens por vez.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        try:
            if interaction.channel is None or not hasattr(interaction.channel, "purge"):
                await interaction.followup.send(CLEANUP_DM_MESSAGE, ephemeral=True)
                return
            deleted_messages = await interaction.channel.purge(limit=quantidade)
        except discord.NotFound:
            logger.warning(
                "Mensagens não encontradas durante uma limpeza no canal %s.", interaction.channel_id
            )
            await interaction.followup.send(CLEANUP_NOT_FOUND_MESSAGE, ephemeral=True)
            return
        except discord.Forbidden:
            logger.warning(
                "Bot sem permissão para limpar mensagens no canal %s.", interaction.channel_id
            )
            await interaction.followup.send(
                "Eu preciso da permissão “Gerenciar mensagens” para executar este comando.",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            logger.exception("Falha HTTP ao limpar mensagens no canal %s.", interaction.channel_id)
            await interaction.followup.send(CLEANUP_HTTP_ERROR_MESSAGE, ephemeral=True)
            return

        deleted_count = len(deleted_messages)
        logger.info(
            "Limpeza executada pelo usuário %s no canal %s: solicitadas=%d, apagadas=%d.",
            interaction.user.id,
            interaction.channel_id,
            quantidade,
            deleted_count,
        )
        await interaction.followup.send(
            f"🧹 {deleted_count} mensagens foram apagadas.",
            ephemeral=True,
        )

    async def _get_current_open_twitch_live(self) -> CurrentTwitchLive | None:
        return await self._get_live.execute()


async def setup(bot: commands.Bot) -> None:
    """Registra o cog de comandos gerais na extensão."""
    discord_bot = cast(DiscordBot, bot)
    await bot.add_cog(
        General(
            discord_bot.notification_sender,
            discord_bot.current_twitch_live,
            discord_bot.twitch_client,
            discord_bot.settings.max_messages_to_delete,
            discord_bot.settings.temporary_voice_creator_channel_id,
            instagram_client=discord_bot.instagram_client,
            call_moderator_user_id=discord_bot.settings.call_moderator_user_id,
            discord_client=discord_bot,
        )
    )
