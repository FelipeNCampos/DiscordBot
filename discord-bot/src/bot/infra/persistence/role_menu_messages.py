"""Cache em memória dos menus de cargos, persistido em SQLite entre execuções."""

from __future__ import annotations

import asyncio
import sqlite3
from pathlib import Path

from bot.application.errors import RoleMenuCacheError


class RoleMenuMessageStore:
    """Consulta IDs sem I/O durante as reações e grava cada atualização por canal."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._messages: dict[tuple[int, str], int] = {}
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Restaura os IDs gravados sem alterar as configurações do ambiente."""
        try:
            self._messages = await asyncio.to_thread(self._load)
        except (OSError, sqlite3.Error) as error:
            raise RoleMenuCacheError("Não foi possível carregar o cache de cargos.") from error

    def _load(self) -> dict[tuple[int, str], int]:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS role_menu_messages ("
                "channel_id INTEGER NOT NULL, category TEXT NOT NULL, "
                "message_id INTEGER NOT NULL, PRIMARY KEY (channel_id, category))"
            )
            return {
                (channel_id, category): message_id
                for channel_id, category, message_id in connection.execute(
                    "SELECT channel_id, category, message_id FROM role_menu_messages"
                )
            }

    def get_message_id(self, channel_id: int, category: str) -> int | None:
        return self._messages.get((channel_id, category))

    async def set_message_id(self, channel_id: int, category: str, message_id: int) -> None:
        """Ativa o ID imediatamente, mesmo se a persistência ficar indisponível."""
        async with self._lock:
            self._messages[channel_id, category] = message_id
            try:
                await asyncio.to_thread(self._save, channel_id, category, message_id)
            except (OSError, sqlite3.Error) as error:
                raise RoleMenuCacheError("Não foi possível persistir o cache de cargos.") from error

    def _save(self, channel_id: int, category: str, message_id: int) -> None:
        with sqlite3.connect(self._path) as connection:
            connection.execute(
                "INSERT INTO role_menu_messages (channel_id, category, message_id) "
                "VALUES (?, ?, ?) "
                "ON CONFLICT(channel_id, category) DO UPDATE SET message_id = excluded.message_id",
                (channel_id, category, message_id),
            )
