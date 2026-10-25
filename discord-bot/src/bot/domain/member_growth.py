"""Períodos e resultados de movimentação de membros, sem estimar histórico ausente."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta, timezone
from typing import Literal

REPORT_TIMEZONE = timezone(timedelta(hours=-3))
MAX_GROWTH_DAYS = 366
PRESET_WINDOWS = {
    "24h": timedelta(hours=24),
    "7d": timedelta(days=7),
    "30d": timedelta(days=30),
    "90d": timedelta(days=90),
}


@dataclass(frozen=True, slots=True)
class GrowthWindow:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start.utcoffset() is None or self.end.utcoffset() is None:
            raise ValueError("As datas precisam incluir fuso horário.")
        if not timedelta(0) < self.end - self.start <= timedelta(days=MAX_GROWTH_DAYS):
            raise ValueError(f"Escolha um intervalo positivo de até {MAX_GROWTH_DAYS} dias.")

    @property
    def previous(self) -> GrowthWindow:
        return GrowthWindow(self.start - (self.end - self.start), self.start)


@dataclass(frozen=True, slots=True)
class GrowthQuery:
    guild_id: int
    window: GrowthWindow
    population: Literal["all", "people", "bots"] = "all"

    def __post_init__(self) -> None:
        if self.guild_id <= 0 or self.population not in {"all", "people", "bots"}:
            raise ValueError("Servidor ou tipo de membro inválido.")


@dataclass(frozen=True, slots=True)
class MembershipEvent:
    guild_id: int
    member_id: int
    kind: Literal["join", "leave"]
    is_bot: bool
    occurred_at: datetime

    def __post_init__(self) -> None:
        if self.kind not in {"join", "leave"} or min(self.guild_id, self.member_id) <= 0:
            raise ValueError("Evento de membro inválido.")
        if self.occurred_at.utcoffset() is None:
            raise ValueError("O horário do evento precisa incluir fuso horário.")


@dataclass(frozen=True, slots=True)
class DailyMovement:
    day: date
    joins: int = 0
    leaves: int = 0

    @property
    def net(self) -> int:
        return self.joins - self.leaves


@dataclass(frozen=True, slots=True)
class GrowthData:
    registered_since: datetime | None
    days: tuple[DailyMovement, ...]


@dataclass(frozen=True, slots=True)
class GrowthMetrics:
    days: tuple[DailyMovement, ...]

    @property
    def joins(self) -> int:
        return sum(day.joins for day in self.days)

    @property
    def leaves(self) -> int:
        return sum(day.leaves for day in self.days)

    @property
    def net(self) -> int:
        return self.joins - self.leaves


@dataclass(frozen=True, slots=True)
class GrowthReport:
    query: GrowthQuery
    current: GrowthMetrics
    previous: GrowthMetrics | None
    registered_since: datetime | None
    partial_history: bool


def growth_window(
    *,
    period: str | None = None,
    start: str | None = None,
    end: str | None = None,
    now: datetime | None = None,
) -> GrowthWindow:
    current = now or datetime.now(UTC)
    if current.utcoffset() is None:
        raise ValueError("O horário atual precisa incluir fuso horário.")
    if start is not None or end is not None:
        if period is not None or start is None or end is None:
            raise ValueError("Informe início e fim juntos, sem selecionar um período pronto.")
        first, last = _parse_date(start), _parse_date(end)
        if last > current.astimezone(REPORT_TIMEZONE).date():
            raise ValueError("A data final não pode estar no futuro.")
        if first > last or (last - first).days + 1 > MAX_GROWTH_DAYS:
            raise ValueError(f"Escolha datas em ordem, cobrindo até {MAX_GROWTH_DAYS} dias.")
        begin = datetime.combine(first, time(), REPORT_TIMEZONE).astimezone(UTC)
        finish = datetime.combine(last + timedelta(days=1), time(), REPORT_TIMEZONE).astimezone(UTC)
        return GrowthWindow(begin, min(finish, current))
    duration = PRESET_WINDOWS.get(period or "7d")
    if duration is None:
        raise ValueError("Escolha 24h, 7d, 30d ou 90d.")
    return GrowthWindow(current - duration, current)


def _parse_date(value: str) -> date:
    for pattern in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value.strip(), pattern).date()
        except ValueError:
            continue
    raise ValueError("Use datas no formato AAAA-MM-DD ou DD/MM/AAAA.")
