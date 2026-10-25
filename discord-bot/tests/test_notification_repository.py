"""Verifica persistência e liberação de recursos do adaptador SQLite."""

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from bot.domain.models import TwitchOnlineEvent
from bot.infra.persistence.notifications import NotificationStore


async def test_sqlite_connections_are_closed_after_each_operation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    connections = []
    connect = sqlite3.connect

    class TrackingConnection(sqlite3.Connection):
        closed = False

        def close(self) -> None:
            self.closed = True
            super().close()

    def tracked_connect(*args: object, **kwargs: object) -> TrackingConnection:
        connection = connect(*args, **kwargs, factory=TrackingConnection)
        connections.append(connection)
        return connection

    monkeypatch.setattr(sqlite3, "connect", tracked_connect)
    store = NotificationStore(tmp_path / "notifications.sqlite3")
    await store.initialize()
    event = TwitchOnlineEvent("id", "stream.online", "123", "canal", None, None, datetime.now(UTC))

    assert await store.register_twitch_event(event)
    assert not await store.register_twitch_event(event)
    await store.update_twitch_event_status("id", "notified")

    assert connections
    assert all(connection.closed for connection in connections)
