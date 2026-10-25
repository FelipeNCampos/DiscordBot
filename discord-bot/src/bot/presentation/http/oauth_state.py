"""Estados OAuth de uso único para os endpoints de autorização."""

from __future__ import annotations

import secrets
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

OAUTH_STATE_TTL = timedelta(minutes=10)


class InstagramOAuthStateStore:
    """Guarda estados de uso único somente pelo tempo necessário para o callback."""

    def __init__(self, *, now: Callable[[], datetime] | None = None) -> None:
        self._states: dict[str, datetime] = {}
        self._now = now or (lambda: datetime.now(UTC))

    def issue(self) -> str:
        """Cria um state criptograficamente aleatório e registra sua expiração."""
        self._remove_expired()
        state = secrets.token_urlsafe(32)
        self._states[state] = self._now() + OAUTH_STATE_TTL
        return state

    def consume(self, state: str) -> bool:
        """Valida e remove o state, impedindo seu reuso."""
        self._remove_expired()
        expires_at = self._states.pop(state, None)
        return expires_at is not None and expires_at >= self._now()

    def _remove_expired(self) -> None:
        now = self._now()
        for state, expires_at in tuple(self._states.items()):
            if expires_at < now:
                del self._states[state]
