"""Agenda consultas do Instagram sem incorporar as regras de notificação."""

from __future__ import annotations

import asyncio
import contextlib
import logging

from bot.application.ports import (
    InstagramMediaClient,
    InstagramMediaRepository,
    InstagramNotificationSender,
)
from bot.application.use_cases.instagram_notifications import PollInstagramMedia
from bot.config.settings import InstagramSettings

logger = logging.getLogger(__name__)


class InstagramPoller:
    def __init__(
        self,
        settings: InstagramSettings,
        instagram_client: InstagramMediaClient,
        store: InstagramMediaRepository,
        sender: InstagramNotificationSender,
    ) -> None:
        self._settings = settings
        self._poll = PollInstagramMedia(
            instagram_client,
            store,
            sender,
            notify_existing_latest=settings.notify_existing_latest,
        )
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        """Inicia uma única tarefa de polling quando a integração está ativada."""
        if not self._settings.enabled or (self._task is not None and not self._task.done()):
            return
        self._task = asyncio.create_task(self._run(), name="instagram-poller")
        logger.info("Polling do Instagram iniciado.")

    async def stop(self) -> None:
        """Cancela a tarefa pendente e aguarda seu encerramento."""
        if self._task is None:
            return
        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def poll_once(self) -> None:
        await self._poll.execute()

    async def _run(self) -> None:
        """Mantém o polling ativo sem derrubar o bot após uma falha recuperável."""
        while True:
            try:
                await self.poll_once()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Falha recuperável durante o polling do Instagram.")
            await asyncio.sleep(self._settings.poll_interval_seconds)
