"""Apresenta métricas e exporta totais diários, sem expor identificadores de membros."""

from __future__ import annotations

import csv
from datetime import UTC, datetime, time, timedelta
from io import StringIO

import discord

from bot.domain.member_growth import REPORT_TIMEZONE, DailyMovement, GrowthReport

POPULATION_LABELS = {"all": "Pessoas e bots", "people": "Pessoas", "bots": "Bots"}


def growth_embed(report: GrowthReport) -> discord.Embed:
    start = _local(report.query.window.start)
    end = _local(report.query.window.end)
    available = (
        report.registered_since is not None and report.registered_since < report.query.window.end
    )
    embed = discord.Embed(
        title="Crescimento do servidor",
        description=f"{start} até {end}\nUTC-03:00 · {POPULATION_LABELS[report.query.population]}",
        colour=(0x57F287 if report.current.net >= 0 else 0xED4245) if available else 0x5865F2,
    )
    for label, value in (
        ("Entradas", report.current.joins),
        ("Saídas", report.current.leaves),
        ("Saldo", f"{report.current.net:+d}"),
    ):
        embed.add_field(name=label, value=str(value) if available else "Sem histórico", inline=True)

    if report.previous is not None:
        previous = report.previous
        embed.add_field(
            name="Comparação com o período anterior de mesma duração",
            value=(
                f"Entradas: {previous.joins} → {report.current.joins}\n"
                f"Saídas: {previous.leaves} → {report.current.leaves}\n"
                f"Saldo: {previous.net:+d} → {report.current.net:+d} "
                f"(diferença {report.current.net - previous.net:+d})"
            ),
            inline=False,
        )
    else:
        embed.add_field(
            name="Comparação anterior",
            value="Sem histórico suficiente para comparar a janela anterior.",
            inline=False,
        )

    if report.partial_history:
        if report.registered_since is None:
            detail = "O registro de membros ainda não foi iniciado neste servidor."
        elif not available:
            detail = "Sem histórico neste período. A coleta começa em " + _local(
                report.registered_since
            )
        else:
            detail = "Contagens parciais: o histórico começa em " + _local(report.registered_since)
        embed.add_field(name="Cobertura do histórico", value=detail, inline=False)

    lines = ["Data     Entradas Saídas Saldo"]
    for day in report.current.days[-14:]:
        if daily_coverage(report, day) == "sem_historico":
            lines.append(f"{day.day:%d/%m/%y}       --     --    --")
        else:
            lines.append(f"{day.day:%d/%m/%y} {day.joins:8d} {day.leaves:6d} {day.net:+5d}")
    embed.add_field(
        name="Movimentação diária · até 14 dias mais recentes",
        value="```\n" + "\n".join(lines) + "\n```",
        inline=False,
    )
    embed.set_footer(
        text="Eventos observados; reentradas contam novamente. "
        "Períodos offline podem ter lacunas. -- = sem histórico."
    )
    return embed


def growth_csv(report: GrowthReport) -> bytes:
    output = StringIO(newline="")
    writer = csv.writer(output, delimiter=";")
    writer.writerow(("data_UTC-03", "entradas", "saidas", "saldo", "cobertura"))
    for day in report.current.days:
        coverage = daily_coverage(report, day)
        counts = ("", "", "") if coverage == "sem_historico" else (day.joins, day.leaves, day.net)
        writer.writerow((day.day.isoformat(), *counts, coverage))
    return output.getvalue().encode("utf-8-sig")


def daily_coverage(report: GrowthReport, day: DailyMovement) -> str:
    since = report.registered_since
    begin = datetime.combine(day.day, time(), REPORT_TIMEZONE).astimezone(UTC)
    end = min(begin + timedelta(days=1), report.query.window.end)
    if since is None or since >= end:
        return "sem_historico"
    if since > max(begin, report.query.window.start):
        return "parcial"
    return "observado"


def _local(value: datetime) -> str:
    return value.astimezone(REPORT_TIMEZONE).strftime("%d/%m/%Y %H:%M")
