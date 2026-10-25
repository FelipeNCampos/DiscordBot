"""Diagnóstico administrativo consultivo, sem alterar o servidor."""

from __future__ import annotations

from typing import cast

import discord
from discord import app_commands
from discord.ext import commands

from bot.application.use_cases.server_diagnostics import diagnose_server
from bot.config.settings import Settings
from bot.domain.diagnostics import DiagnosticReport
from bot.presentation.discord.errors import MISSING_MANAGE_GUILD_PERMISSION_MESSAGE
from bot.presentation.discord.server_snapshot import collect_server_snapshot

STATUS_LABELS = {"ok": "OK", "warning": "ATENÇÃO", "error": "ERRO", "disabled": "DESATIVADO"}


class ServerAdministration(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: Settings) -> None:
        self._bot = bot
        self._settings = settings

    @app_commands.command(
        name="diagnostico", description="Verifica configuração, permissões e registros do servidor."
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    async def diagnostics(self, interaction: discord.Interaction) -> None:
        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(
                MISSING_MANAGE_GUILD_PERMISSION_MESSAGE,
                ephemeral=True,
            )
            return
        if interaction.guild is None:
            await interaction.response.send_message(
                "Execute este comando dentro de um servidor.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)
        snapshot = collect_server_snapshot(self._bot, interaction.guild, self._settings)
        report = diagnose_server(snapshot)
        embeds = self._report_embeds(interaction.guild, report)
        await interaction.followup.send(
            embeds=embeds, ephemeral=True, allowed_mentions=discord.AllowedMentions.none()
        )

    def _report_embeds(self, guild: discord.Guild, report: DiagnosticReport) -> list[discord.Embed]:
        status = "Há problemas para corrigir." if report.has_errors else "Verificações concluídas."
        description = (
            f"{status}\nServidor: {guild.id} · Membros: {guild.member_count or 'não disponível'}\n"
            f"Canais: {len(guild.channels)} · Cargos: {len(guild.roles)}\n"
            "Categorias de log: "
            + (", ".join(sorted(self._settings.activity_log_events)) or "nenhuma")
        )
        embeds = []
        for offset in range(0, len(report.checks), 15):
            embed = discord.Embed(
                title="Diagnóstico do servidor",
                description=description,
                colour=0xED4245 if report.has_errors else 0x57F287,
            )
            for check in report.checks[offset : offset + 15]:
                embed.add_field(
                    name=f"{STATUS_LABELS[check.status]} · {check.label}",
                    value=check.detail[:1000],
                    inline=False,
                )
            embed.set_footer(text="Leitura do cache atual; nenhuma configuração foi alterada.")
            embeds.append(embed)
        return embeds


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ServerAdministration(bot, cast(Settings, bot.settings)))
