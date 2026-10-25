"""Agenda a renovação; a decisão e a persistência pertencem ao caso de uso."""

from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import Callable
from datetime import datetime

from bot.application.ports import InstagramTokenRefreshClient, InstagramTokenStore
from bot.application.use_cases.instagram_token_refresh import (
    InstagramRefreshPolicy,
    RefreshInstagramToken,
)
from bot.config.settings import InstagramSettings

logger = logging.getLogger(__name__)


class InstagramTokenRefreshTask:
    def __init__(
        self,
        settings: InstagramSettings,
        instagram_client: InstagramTokenRefreshClient,
        token_store: InstagramTokenStore,
        *,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._settings = settings
        self._task: asyncio.Task[None] | None = None
        self._refresh = RefreshInstagramToken(
            InstagramRefreshPolicy(
                enabled=settings.enabled and settings.auto_refresh_token,
                days_before_expiry=settings.token_refresh_days_before_expiry,
                check_interval_hours=settings.token_refresh_check_interval_hours,
            ),
            instagram_client,
            token_store,
            now=now,
        )

    @property
    def last_attempt_at(self) -> datetime | None:
        return self._refresh.last_attempt_at

    @property
    def last_status(self) -> str | None:
        return self._refresh.last_status

    async def check_once(self) -> None:
        await self._refresh.execute()

    def start(self) -> None:
        """Inicia uma única tarefa se Instagram e renovação automática estiverem ativos."""
        if (
            not self._settings.enabled
            or not self._settings.auto_refresh_token
            or (self._task is not None and not self._task.done())
        ):
            return
        self._task = asyncio.create_task(self._run(), name="instagram-token-refresh")
        logger.info("Renovação automática do token Instagram ativada.")

    async def stop(self) -> None:
        """Cancela e aguarda a tarefa para não deixar trabalho pendente no desligamento."""
        if self._task is None:
            return
        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def _run(self) -> None:
        """Executa verificações periódicas sem repetir em ciclo rápido após uma falha."""
        while True:
            try:
                await self.check_once()
                logger.info(
                    "Próxima verificação do token Instagram em %d hora(s).",
                    self._settings.token_refresh_check_interval_hours,
                )
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Falha recuperável na tarefa de renovação do token Instagram.")
            await asyncio.sleep(self._settings.token_refresh_check_interval_hours * 3600)
