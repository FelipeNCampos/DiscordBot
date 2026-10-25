"""Coleta sem cache de membros, privacidade do comando e exportação diária."""

import csv
from datetime import UTC, date, datetime, timedelta
from io import StringIO
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot.application.errors import GrowthStorageError
from bot.application.use_cases.member_growth import AnalyzeMemberGrowth
from bot.domain.member_growth import DailyMovement, GrowthData, GrowthQuery, growth_window
from bot.presentation.discord.cogs.server_growth import ServerGrowth
from bot.presentation.discord.growth_report import daily_coverage, growth_csv, growth_embed

NOW = datetime(2026, 10, 24, 18, tzinfo=UTC)


def repository() -> SimpleNamespace:
    return SimpleNamespace(
        get_activity=AsyncMock(return_value=GrowthData(None, ())),
        start_tracking=AsyncMock(),
        record_event=AsyncMock(),
    )


def interaction(*, allowed: bool = True, attachments: bool = True) -> SimpleNamespace:
    return SimpleNamespace(
        guild=SimpleNamespace(id=123),
        permissions=SimpleNamespace(manage_guild=allowed),
        app_permissions=SimpleNamespace(attach_files=attachments),
        response=SimpleNamespace(send_message=AsyncMock(), defer=AsyncMock()),
        followup=SimpleNamespace(send=AsyncMock()),
    )


async def test_growth_requires_manage_guild_before_querying_history() -> None:
    store, request = repository(), interaction(allowed=False)
    cog = ServerGrowth(SimpleNamespace(), store, now=lambda: NOW)
    await ServerGrowth.growth.callback(cog, request)
    store.get_activity.assert_not_awaited()
    assert request.response.send_message.await_args.kwargs["ephemeral"]


@pytest.mark.parametrize(
    "arguments",
    [
        {"inicio": "2026-10-01"},
        {"periodo": "invalid"},
        {"tipo": "invalid"},
        {"inicio": "2026-10-25", "fim": "2026-10-26"},
    ],
)
async def test_bad_filters_do_not_query_or_defer(arguments: dict) -> None:
    store, request = repository(), interaction()
    await ServerGrowth.growth.callback(
        ServerGrowth(SimpleNamespace(), store, now=lambda: NOW),
        request,
        **arguments,
    )
    store.get_activity.assert_not_awaited()
    request.response.defer.assert_not_awaited()
    request.response.send_message.assert_awaited_once()


async def test_growth_response_is_private_and_attaches_only_daily_aggregates() -> None:
    store, request = repository(), interaction()
    await ServerGrowth.growth.callback(
        ServerGrowth(SimpleNamespace(), store, now=lambda: NOW),
        request,
        periodo="30d",
        tipo="people",
    )
    options = request.followup.send.await_args.kwargs
    assert options["ephemeral"] is True
    assert options["allowed_mentions"].everyone is False
    assert len(options["embed"].fields) <= 25 and len(options["embed"]) < 6000
    assert all(len(field.value) <= 1024 for field in options["embed"].fields)
    document = options["files"][0]
    rows = list(csv.DictReader(StringIO(document.fp.getvalue().decode("utf-8-sig")), delimiter=";"))
    assert len(rows) > 14
    assert set(rows[0]) == {"data_UTC-03", "entradas", "saidas", "saldo", "cobertura"}
    assert rows[0]["cobertura"] == "sem_historico"
    assert rows[0]["entradas"] == ""
    query = store.get_activity.await_args.args[0]
    assert query.guild_id == 123 and query.population == "people"


async def test_report_still_works_when_bot_cannot_attach_files() -> None:
    store, request = repository(), interaction(attachments=False)
    await ServerGrowth.growth.callback(
        ServerGrowth(SimpleNamespace(), store, now=lambda: NOW),
        request,
    )
    options = request.followup.send.await_args.kwargs
    assert options["files"] == []
    assert any(field.name == "CSV" for field in options["embed"].fields)


async def test_storage_failures_do_not_expose_technical_details() -> None:
    store, request = repository(), interaction()
    store.get_activity.side_effect = GrowthStorageError("/private/path.sqlite3")
    await ServerGrowth.growth.callback(
        ServerGrowth(SimpleNamespace(), store, now=lambda: NOW),
        request,
    )
    message = request.followup.send.await_args.args[0]
    assert "private" not in message and "sqlite3" not in message


async def test_membership_collection_uses_raw_departures_and_original_join_timestamp() -> None:
    store = repository()
    cog = ServerGrowth(SimpleNamespace(guilds=[SimpleNamespace(id=123)]), store, now=lambda: NOW)
    await cog.on_ready()
    store.start_tracking.assert_awaited_once_with(123, NOW)
    joined_at = NOW - timedelta(minutes=1)
    member = SimpleNamespace(guild=SimpleNamespace(id=123), id=7, bot=False, joined_at=joined_at)
    await cog.on_member_join(member)
    # O usuário raw não tem guild nem joined_at: não depende do cache de membros.
    await cog.on_raw_member_remove(
        SimpleNamespace(guild_id=123, user=SimpleNamespace(id=7, bot=False))
    )
    events = [call.args[0] for call in store.record_event.await_args_list]
    assert [event.kind for event in events] == ["join", "leave"]
    assert events[0].occurred_at == joined_at
    assert events[1].occurred_at == NOW
    listeners = {name for name, _ in cog.get_listeners()}
    assert "on_raw_member_remove" in listeners and "on_member_remove" not in listeners


async def test_history_failure_does_not_stop_membership_listeners() -> None:
    store = repository()
    store.record_event.side_effect = GrowthStorageError("indisponível")
    cog = ServerGrowth(SimpleNamespace(), store, now=lambda: NOW)
    await cog.on_raw_member_remove(
        SimpleNamespace(guild_id=123, user=SimpleNamespace(id=7, bot=True))
    )
    store.record_event.assert_awaited_once()


async def test_csv_marks_partial_days_and_retains_real_zeroes_after_tracking_started() -> None:
    since = datetime(2026, 10, 23, 15, tzinfo=UTC)
    store = repository()
    store.get_activity.return_value = GrowthData(since, (DailyMovement(date(2026, 10, 23), 2, 1),))
    query = GrowthQuery(123, growth_window(start="2026-10-22", end="2026-10-24", now=NOW))
    report = await AnalyzeMemberGrowth(store).execute(query)
    rows = list(csv.reader(StringIO(growth_csv(report).decode("utf-8-sig")), delimiter=";"))
    assert rows[1][1:] == ["", "", "", "sem_historico"]
    assert rows[2][1:] == ["2", "1", "1", "parcial"]
    assert rows[3][1:] == ["0", "0", "0", "observado"]
    assert daily_coverage(report, report.current.days[0]) == "sem_historico"
    assert "--" in growth_embed(report).fields[-1].value
