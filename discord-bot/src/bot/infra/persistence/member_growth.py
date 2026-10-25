"""Histórico SQLite de membros, com consultas agregadas e índices por servidor e data."""

from __future__ import annotations

import asyncio
import sqlite3
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import TypeVar

from bot.application.errors import GrowthStorageError
from bot.domain.member_growth import DailyMovement, GrowthData, GrowthQuery, MembershipEvent

EPOCH = datetime(1970, 1, 1, tzinfo=UTC)
T = TypeVar("T")


class MemberGrowthStore:
    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    async def initialize(self) -> None:
        await self._run(self._initialize_sync)

    async def start_tracking(self, guild_id: int, started_at: datetime) -> None:
        await self._run(self._start_tracking_sync, guild_id, started_at)

    async def record_event(self, event: MembershipEvent) -> None:
        await self._run(self._record_event_sync, event)

    async def get_activity(self, query: GrowthQuery) -> GrowthData:
        return await self._run(self._get_activity_sync, query)

    async def _run(self, operation: Callable[..., T], *args: object) -> T:
        try:
            return await asyncio.to_thread(operation, *args)
        except (sqlite3.Error, OSError) as error:
            raise GrowthStorageError(
                "O histórico de membros está temporariamente indisponível."
            ) from error

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._database_path, timeout=10)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            with connection:
                yield connection
        finally:
            connection.close()

    def _initialize_sync(self) -> None:
        with self._connection() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS member_growth_tracking (
                    guild_id INTEGER PRIMARY KEY,
                    started_at_us INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS member_growth_events (
                    guild_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    kind TEXT NOT NULL CHECK (kind IN ('join', 'leave')),
                    is_bot INTEGER NOT NULL CHECK (is_bot IN (0, 1)),
                    occurred_at_us INTEGER NOT NULL,
                    UNIQUE (guild_id, member_id, kind, occurred_at_us)
                );
                CREATE INDEX IF NOT EXISTS idx_member_growth_guild_time
                    ON member_growth_events (guild_id, occurred_at_us);
            """)

    @staticmethod
    def _track(connection: sqlite3.Connection, guild_id: int, started_at: datetime) -> None:
        connection.execute(
            """
            INSERT INTO member_growth_tracking (guild_id, started_at_us) VALUES (?, ?)
            ON CONFLICT(guild_id) DO UPDATE
            SET started_at_us = MIN(started_at_us, excluded.started_at_us)
        """,
            (guild_id, _microseconds(started_at)),
        )

    def _start_tracking_sync(self, guild_id: int, started_at: datetime) -> None:
        with self._connection() as connection:
            self._track(connection, guild_id, started_at)

    def _record_event_sync(self, event: MembershipEvent) -> None:
        with self._connection() as connection:
            self._track(connection, event.guild_id, event.occurred_at)
            connection.execute(
                """
                INSERT OR IGNORE INTO member_growth_events
                    (guild_id, member_id, kind, is_bot, occurred_at_us) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    event.guild_id,
                    event.member_id,
                    event.kind,
                    int(event.is_bot),
                    _microseconds(event.occurred_at),
                ),
            )

    def _get_activity_sync(self, query: GrowthQuery) -> GrowthData:
        population_clause = {"all": "", "people": "AND is_bot = 0", "bots": "AND is_bot = 1"}[
            query.population
        ]
        with self._connection() as connection:
            connection.execute("BEGIN")
            tracking = connection.execute(
                "SELECT started_at_us FROM member_growth_tracking WHERE guild_id = ?",
                (query.guild_id,),
            ).fetchone()
            # Divisão inteira antes da conversão impede arredondar microssegundos para outro dia.
            rows = connection.execute(
                f"""
                SELECT date(occurred_at_us / 1000000, 'unixepoch', '-03:00') AS day,
                       SUM(kind = 'join'), SUM(kind = 'leave')
                FROM member_growth_events
                WHERE guild_id = ? AND occurred_at_us >= ? AND occurred_at_us < ?
                      {population_clause}
                GROUP BY day ORDER BY day
            """,
                (
                    query.guild_id,
                    _microseconds(query.window.start),
                    _microseconds(query.window.end),
                ),
            ).fetchall()
        return GrowthData(
            EPOCH + timedelta(microseconds=tracking[0]) if tracking else None,
            tuple(
                DailyMovement(date.fromisoformat(day), joins, leaves) for day, joins, leaves in rows
            ),
        )


def _microseconds(value: datetime) -> int:
    if value.utcoffset() is None:
        raise ValueError("O horário precisa incluir fuso horário.")
    delta = value.astimezone(UTC) - EPOCH
    return (delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds
