"""Movimentação persistente, filtros por período e isolamento entre servidores."""

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from bot.application.use_cases.member_growth import AnalyzeMemberGrowth
from bot.domain.member_growth import (
    GrowthQuery,
    GrowthWindow,
    MembershipEvent,
    growth_window,
)
from bot.infra.persistence.member_growth import MemberGrowthStore


def test_growth_window_supports_presets_and_inclusive_local_dates() -> None:
    now = datetime(2026, 10, 24, 18, tzinfo=UTC)
    window = growth_window(period="7d", now=now)
    assert window.end == now
    assert window.start == now - timedelta(days=7)
    custom = growth_window(start="01/10/2026", end="2026-10-02", now=now)
    assert custom.start == datetime(2026, 10, 1, 3, tzinfo=UTC)
    assert custom.end == datetime(2026, 10, 3, 3, tzinfo=UTC)


@pytest.mark.parametrize(
    "filters",
    [
        {"start": "2026-10-01"},
        {"start": "2026-10-03", "end": "2026-10-01"},
        {"start": "2026-10-01", "end": "2026-10-25"},
        {"start": "2026-02-30", "end": "2026-10-01"},
        {"period": "7d", "start": "2026-10-01", "end": "2026-10-02"},
        {"period": "invalid"},
        {"start": "2024-01-01", "end": "2026-01-01"},
    ],
)
def test_growth_window_rejects_ambiguous_invalid_or_unbounded_filters(filters: dict) -> None:
    with pytest.raises(ValueError):
        growth_window(**filters, now=datetime(2026, 10, 24, 18, tzinfo=UTC))


def test_current_day_is_only_counted_until_now() -> None:
    now = datetime(2026, 10, 24, 18, tzinfo=UTC)
    window = growth_window(start="2026-10-24", end="2026-10-24", now=now)
    assert window.end == now
    assert window.start == datetime(2026, 10, 24, 3, tzinfo=UTC)


async def test_repository_filters_guild_population_and_half_open_boundaries(tmp_path: Path) -> None:
    store = MemberGrowthStore(tmp_path / "growth.sqlite3")
    await store.initialize()
    begin = datetime(2026, 10, 1, 3, tzinfo=UTC)
    await store.start_tracking(1, begin - timedelta(days=10))
    events = [
        MembershipEvent(1, 10, "join", False, begin),
        MembershipEvent(1, 11, "join", True, begin + timedelta(hours=1)),
        MembershipEvent(1, 10, "leave", False, begin + timedelta(hours=2)),
        MembershipEvent(2, 12, "join", False, begin),
        MembershipEvent(1, 13, "join", False, begin + timedelta(days=1)),
    ]
    for event in events:
        await store.record_event(event)
    # Reenvio do mesmo evento não pode alterar o resultado.
    await store.record_event(events[0])
    query = GrowthQuery(1, GrowthWindow(begin, begin + timedelta(days=1)), "people")
    data = await MemberGrowthStore(tmp_path / "growth.sqlite3").get_activity(query)
    assert sum(day.joins for day in data.days) == 1
    assert sum(day.leaves for day in data.days) == 1
    assert data.days[0].day == date(2026, 10, 1)
    bots = await store.get_activity(GrowthQuery(1, query.window, "bots"))
    assert sum(day.joins for day in bots.days) == 1
    assert sum(day.leaves for day in bots.days) == 0


async def test_analysis_fills_days_and_compares_equal_previous_periods(tmp_path: Path) -> None:
    store = MemberGrowthStore(tmp_path / "growth.sqlite3")
    await store.initialize()
    begin = datetime(2026, 10, 1, 3, tzinfo=UTC)
    await store.start_tracking(1, begin - timedelta(days=20))
    for event in [
        MembershipEvent(1, 1, "join", False, begin - timedelta(days=1)),
        MembershipEvent(1, 2, "join", False, begin),
        MembershipEvent(1, 3, "join", False, begin),
        MembershipEvent(1, 4, "leave", False, begin + timedelta(days=2)),
    ]:
        await store.record_event(event)
    report = await AnalyzeMemberGrowth(store).execute(
        GrowthQuery(
            1,
            GrowthWindow(begin, begin + timedelta(days=3)),
            "all",
        )
    )
    assert report.current.joins == 2
    assert report.current.leaves == 1
    assert report.current.net == 1
    assert len(report.current.days) == 3
    assert report.current.days[1].joins == report.current.days[1].leaves == 0
    assert report.previous is not None and report.previous.net == 1
    assert not report.partial_history


async def test_history_before_installation_is_explicitly_partial(tmp_path: Path) -> None:
    store = MemberGrowthStore(tmp_path / "growth.sqlite3")
    await store.initialize()
    now = datetime(2026, 10, 24, 18, tzinfo=UTC)
    await store.start_tracking(1, now - timedelta(days=1))
    report = await AnalyzeMemberGrowth(store).execute(
        GrowthQuery(
            1,
            growth_window(period="7d", now=now),
            "all",
        )
    )
    assert report.partial_history
    assert report.previous is None
    assert report.registered_since == now - timedelta(days=1)
    assert report.current.joins == report.current.leaves == 0


async def test_empty_history_is_not_presented_as_a_complete_zero_period(tmp_path: Path) -> None:
    store = MemberGrowthStore(tmp_path / "growth.sqlite3")
    await store.initialize()
    now = datetime(2026, 10, 24, 18, tzinfo=UTC)
    report = await AnalyzeMemberGrowth(store).execute(
        GrowthQuery(
            1,
            growth_window(period="24h", now=now),
            "all",
        )
    )
    assert report.registered_since is None
    assert report.partial_history
    assert report.previous is None


async def test_daily_buckets_respect_local_midnight_to_the_microsecond(tmp_path: Path) -> None:
    store = MemberGrowthStore(tmp_path / "growth.sqlite3")
    await store.initialize()
    midnight = datetime(2026, 10, 2, 3, tzinfo=UTC)
    await store.record_event(
        MembershipEvent(1, 1, "join", False, midnight - timedelta(microseconds=1))
    )
    await store.record_event(MembershipEvent(1, 2, "leave", False, midnight))
    data = await store.get_activity(
        GrowthQuery(
            1,
            GrowthWindow(midnight - timedelta(days=1), midnight + timedelta(days=1)),
        )
    )
    assert [(day.day, day.joins, day.leaves) for day in data.days] == [
        (date(2026, 10, 1), 1, 0),
        (date(2026, 10, 2), 0, 1),
    ]


async def test_reconnect_does_not_reset_historical_start(tmp_path: Path) -> None:
    store = MemberGrowthStore(tmp_path / "growth.sqlite3")
    await store.initialize()
    begin = datetime(2026, 10, 1, 3, tzinfo=UTC)
    await store.start_tracking(1, begin)
    await store.start_tracking(1, begin + timedelta(days=10))
    data = await store.get_activity(GrowthQuery(1, GrowthWindow(begin, begin + timedelta(days=1))))
    assert data.registered_since == begin


async def test_period_before_history_does_not_try_to_compare_an_unsupported_previous_date(
    tmp_path: Path,
) -> None:
    store = MemberGrowthStore(tmp_path / "growth.sqlite3")
    await store.initialize()
    await store.start_tracking(1, datetime(2026, 10, 1, tzinfo=UTC))
    query = GrowthQuery(1, growth_window(start="0001-01-02", end="0001-01-04"))
    report = await AnalyzeMemberGrowth(store).execute(query)
    assert report.partial_history and report.previous is None
