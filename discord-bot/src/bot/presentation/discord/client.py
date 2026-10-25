"""Cliente principal do bot do Discord."""

from __future__ import annotations

import asyncio
import contextlib
import logging

import discord
from discord.ext import commands

from bot.application.ports import (
    AudioSource,
    BackgroundTask,
    CurrentTwitchLiveRepository,
    InstagramGateway,
    NotificationRepository,
    TwitchGateway,
)
from bot.application.use_cases.member_growth import GrowthRepository
from bot.application.use_cases.twitch_notifications import NotifyTwitchLive
from bot.config.settings import Settings
from bot.domain.models import TwitchOnlineEvent
from bot.presentation.discord.command_access import CommandAccessTree
from bot.presentation.discord.errors import handle_app_command_error
from bot.presentation.discord.notification_sender import DiscordNotificationSender

logger = logging.getLogger(__name__)


class DiscordBot(commands.Bot):
    """Cliente Discord com comandos slash e o comando prefixado de moderação."""

    def __init__(
        self,
        settings: Settings,
        *,
        store: NotificationRepository,
        twitch_client: TwitchGateway | None = None,
        instagram_client: InstagramGateway | None = None,
        current_twitch_live: CurrentTwitchLiveRepository,
        audio_service: AudioSource,
        growth_repository: GrowthRepository,
    ) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        # Necessário para receber on_member_join e resolver membros em reações antigas.
        intents.members = True
        intents.presences = False
        intents.guilds = True
        intents.guild_messages = True
        intents.moderation = True
        intents.voice_states = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=None,
            application_id=settings.discord_application_id,
            tree_cls=CommandAccessTree,
        )
        self.settings = settings
        self.tree.on_error = handle_app_command_error
        self._store = store
        self.twitch_client = twitch_client
        self._instagram_client = instagram_client
        self._sender = DiscordNotificationSender(self, settings)
        self._current_twitch_live = current_twitch_live
        self.audio_service = audio_service
        self.growth_repository = growth_repository
        self._twitch_notification_queue: asyncio.Queue[TwitchOnlineEvent] = asyncio.Queue()
        self._twitch_worker_task: asyncio.Task[None] | None = None
        self._startup_tasks: tuple[BackgroundTask, ...] = ()
        self._ready_tasks: tuple[BackgroundTask, ...] = ()
        self._notify_twitch_live = (
            NotifyTwitchLive(twitch_client, store, current_twitch_live, self._sender)
            if twitch_client is not None
            else None
        )

    def configure_background_tasks(
        self,
        *,
        startup: tuple[BackgroundTask, ...] = (),
        ready: tuple[BackgroundTask, ...] = (),
    ) -> None:
        """Recebe tarefas compostas no bootstrap antes de conectar ao Gateway."""
        self._startup_tasks = startup
        self._ready_tasks = ready

    @property
    def notification_sender(self) -> DiscordNotificationSender:
        """Expõe o remetente compartilhado para extensões do bot."""
        return self._sender

    @property
    def current_twitch_live(self) -> CurrentTwitchLiveRepository:
        """Expõe o estado em memória da última live Twitch ainda aberta."""
        return self._current_twitch_live

    @property
    def instagram_client(self) -> InstagramGateway | None:
        """Expõe o cliente Instagram compartilhado para comandos administrativos."""
        return self._instagram_client

    async def setup_hook(self) -> None:
        """Carrega extensões e sincroniza comandos antes de conectar ao gateway."""
        await self.load_extension("bot.presentation.discord.cogs.general")
        await self.load_extension("bot.presentation.discord.cogs.media_reactions")
        await self.load_extension("bot.presentation.discord.cogs.role_management")
        await self.load_extension("bot.presentation.discord.cogs.member_activity_logs")
        await self.load_extension("bot.presentation.discord.cogs.server_administration")
        await self.load_extension("bot.presentation.discord.cogs.server_growth")
        await self.load_extension("bot.presentation.discord.cogs.temporary_voice")
        await self.load_extension("bot.presentation.discord.cogs.music")

        if self.settings.discord_guild_id is not None:
            guild = discord.Object(id=self.settings.discord_guild_id)
            self.tree.copy_global_to(guild=guild)
            synced_commands = await self.tree.sync(guild=guild)
            logger.info(
                "%d comando(s) slash sincronizado(s) no servidor de desenvolvimento.",
                len(synced_commands),
            )
        else:
            logger.warning(
                "DISCORD_GUILD_ID não foi definido; "
                "comandos de desenvolvimento não foram sincronizados."
            )

        if self.settings.sync_global_commands:
            synced_commands = await self.tree.sync()
            logger.info("%d comando(s) slash sincronizado(s) globalmente.", len(synced_commands))

        if self.twitch_client is not None and (
            self._twitch_worker_task is None or self._twitch_worker_task.done()
        ):
            self._twitch_worker_task = asyncio.create_task(
                self._run_twitch_notification_worker(), name="twitch-notification-worker"
            )
        for task in self._startup_tasks:
            task.start()

    def queue_twitch_notification(self, event: TwitchOnlineEvent) -> None:
        """Enfileira um evento EventSub sem bloquear a resposta HTTP da Twitch."""
        if self.twitch_client is None:
            logger.warning("Evento Twitch ignorado: integração desativada.")
            return
        expected_broadcaster_id = self.twitch_client.resolved_broadcaster_user_id
        if (
            expected_broadcaster_id is not None
            and event.broadcaster_user_id != expected_broadcaster_id
        ):
            logger.info("Evento Twitch ignorado: perfil diferente do perfil configurado.")
            return
        self._twitch_notification_queue.put_nowait(event)

    async def on_ready(self) -> None:
        """Registra a conexão e inicia serviços que dependem do cliente pronto."""
        if self.user is None:
            logger.info("O bot está pronto.")
        else:
            logger.info("O bot está pronto como %s (ID: %s).", self.user, self.user.id)

        for task in self._ready_tasks:
            task.start()

    async def close(self) -> None:
        """Cancela tarefas e fecha clientes auxiliares antes de encerrar o Discord."""
        for task in reversed((*self._startup_tasks, *self._ready_tasks)):
            await task.stop()

        if self._twitch_worker_task is not None:
            self._twitch_worker_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._twitch_worker_task
            self._twitch_worker_task = None

        if self._instagram_client is not None:
            await self._instagram_client.aclose()
        if self.twitch_client is not None:
            await self.twitch_client.aclose()
        await super().close()

    async def _run_twitch_notification_worker(self) -> None:
        """Entrega eventos Twitch após o cliente Discord ficar disponível."""
        while True:
            event = await self._twitch_notification_queue.get()
            try:
                await self.wait_until_ready()
                if self._notify_twitch_live is not None:
                    await self._notify_twitch_live.execute(event)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Falha recuperável ao enviar uma notificação da Twitch.")
            finally:
                self._twitch_notification_queue.task_done()
