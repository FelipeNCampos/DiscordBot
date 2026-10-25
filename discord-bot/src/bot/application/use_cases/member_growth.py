"""Consulta o histórico observado e preenche os dias sem movimentação."""

from dataclasses import replace
from datetime import datetime, timedelta
from typing import Protocol

from bot.domain.member_growth import (
    REPORT_TIMEZONE,
    DailyMovement,
    GrowthData,
    GrowthMetrics,
    GrowthQuery,
    GrowthReport,
    GrowthWindow,
    MembershipEvent,
)


class GrowthReader(Protocol):
    async def get_activity(self, query: GrowthQuery) -> GrowthData: ...


class GrowthRepository(GrowthReader, Protocol):
    async def start_tracking(self, guild_id: int, started_at: datetime) -> None: ...

    async def record_event(self, event: MembershipEvent) -> None: ...


class AnalyzeMemberGrowth:
    def __init__(self, repository: GrowthReader) -> None:
        self._repository = repository

    async def execute(self, query: GrowthQuery) -> GrowthReport:
        data = await self._repository.get_activity(query)
        since = data.registered_since
        previous = None
        if (
            since is not None
            and since <= query.window.start
            and since <= query.window.previous.start
        ):
            earlier = await self._repository.get_activity(
                replace(query, window=query.window.previous)
            )
            previous = _metrics(query.window.previous, earlier)
        return GrowthReport(
            query,
            _metrics(query.window, data),
            previous,
            since,
            partial_history=since is None or since > query.window.start,
        )


def _metrics(window: GrowthWindow, data: GrowthData) -> GrowthMetrics:
    known = {day.day: day for day in data.days}
    day = window.start.astimezone(REPORT_TIMEZONE).date()
    last = (window.end - timedelta(microseconds=1)).astimezone(REPORT_TIMEZONE).date()
    days = []
    while day <= last:
        days.append(known.get(day, DailyMovement(day)))
        day += timedelta(days=1)
    return GrowthMetrics(tuple(days))
