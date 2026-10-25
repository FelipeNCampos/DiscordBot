"""Renova autorizações com controle de concorrência e janela de tentativas."""

from __future__ import annotations

import asyncio
import logging
import math
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from bot.application.errors import (
    InstagramAPIError,
    InstagramAuthenticationError,
    InstagramTokenStoreError,
)
from bot.application.ports import InstagramTokenRefreshClient, InstagramTokenStore
from bot.domain.models import InstagramTokenData

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class InstagramRefreshPolicy:
    enabled: bool
    days_before_expiry: int
    check_interval_hours: int


class RefreshInstagramToken:
    def __init__(
        self,
        policy: InstagramRefreshPolicy,
        instagram_client: InstagramTokenRefreshClient,
        token_store: InstagramTokenStore,
        *,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._policy = policy
        self._instagram_client = instagram_client
        self._token_store = token_store
        self._now = now or (lambda: datetime.now(UTC))
        self._refresh_lock = asyncio.Lock()
        self._last_attempt_at: datetime | None = None
        self._last_status: str | None = None

    @property
    def last_attempt_at(self) -> datetime | None:
        """Informa a última tentativa sem expor informações secretas."""
        return self._last_attempt_at

    @property
    def last_status(self) -> str | None:
        """Informa o resultado seguro mais recente da renovação."""
        return self._last_status

    async def execute(self) -> None:
        try:
            await self._refresh_if_due()
        except Exception:
            self._last_status = "unexpected_error"
            raise

    async def _refresh_if_due(self) -> None:
        """Recarrega, valida a janela e renova o token somente quando necessário."""
        if not self._policy.enabled:
            return

        async with self._refresh_lock:
            now = self._now().astimezone(UTC)
            if self._last_attempt_at is not None and now - self._last_attempt_at < timedelta(
                hours=self._policy.check_interval_hours
            ):
                return

            try:
                token = await self._token_store.get_token()
            except InstagramTokenStoreError:
                self._last_attempt_at = now
                self._last_status = "storage_error"
                logger.exception("Não foi possível ler o token Instagram do armazenamento seguro.")
                return

            if token is None:
                self._last_attempt_at = now
                self._last_status = "missing_token"
                logger.warning(
                    "A autorização do Instagram precisa ser renovada. "
                    "Gere um novo token e atualize a configuração segura do bot."
                )
                return

            remaining = token.expires_at - now
            days_remaining = max(0, math.ceil(remaining.total_seconds() / 86400))
            logger.info("Token do Instagram expira em %d dia(s).", days_remaining)
            if remaining <= timedelta(0):
                self._last_attempt_at = now
                self._last_status = "expired"
                logger.warning(
                    "A autorização do Instagram precisa ser renovada. "
                    "Gere um novo token e atualize a configuração segura do bot."
                )
                return

            if remaining > timedelta(days=self._policy.days_before_expiry):
                self._last_status = "not_due"
                return

            self._last_attempt_at = now
            try:
                result = await self._instagram_client.refresh_access_token(token.access_token)
                await self._token_store.save_token(
                    InstagramTokenData(
                        access_token=result.access_token,
                        token_type=result.token_type,
                        expires_at=result.expires_at,
                        updated_at=now,
                        user_id=token.user_id,
                        username=token.username,
                    )
                )
            except InstagramAuthenticationError:
                self._last_status = "reauthorization_required"
                logger.warning(
                    "A autorização do Instagram precisa ser renovada. "
                    "Gere um novo token e atualize a configuração segura do bot."
                )
            except (InstagramAPIError, InstagramTokenStoreError):
                self._last_status = "refresh_error"
                logger.exception("Não foi possível renovar o token Instagram nesta verificação.")
            else:
                self._last_status = "refreshed"
                logger.info("Token do Instagram renovado com sucesso.")
