"""Coleta entradas/saídas e oferece análise privada filtrada por tempo."""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import UTC, datetime
from io import BytesIO
from typing import cast

import discord
from discord import app_commands
from discord.ext import commands

from bot.application.errors import GrowthStorageError
from bot.application.use_cases.member_growth import AnalyzeMemberGrowth, GrowthRepository
from bot.domain.member_growth import GrowthQuery, MembershipEvent, growth_window
from bot.presentation.discord.client import DiscordBot
from bot.presentation.discord.errors import MISSING_MANAGE_GUILD_PERMISSION_MESSAGE
from bot.presentation.discord.growth_report import growth_csv, growth_embed

logger = logging.getLogger(__name__)


class ServerGrowth(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        repository: GrowthRepository,
        *,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._bot = bot
        self._repository = repository
        self._analysis = AnalyzeMemberGrowth(repository)
        self._now = now or (lambda: datetime.now(UTC))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self._bot.guilds:
            await self.on_guild_join(guild)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        try:
            await self._repository.start_tracking(guild.id, self._now())
        except GrowthStorageError:
            logger.exception("Não foi possível iniciar o histórico de membros: guild=%s.", guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self._record(
            MembershipEvent(
                member.guild.id,
                member.id,
                "join",
                member.bot,
                member.joined_at or self._now(),
            )
        )

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent) -> None:
        # Somente o evento raw conta saídas; contar também on_member_remove duplicaria a medição.
        await self._record(
            MembershipEvent(
                payload.guild_id,
                payload.user.id,
                "leave",
                payload.user.bot,
                self._now(),
            )
        )

    async def _record(self, event: MembershipEvent) -> None:
        try:
            await self._repository.record_event(event)
        except GrowthStorageError:
            logger.exception("Falha ao registrar movimentação de membro: guild=%s.", event.guild_id)

    @app_commands.command(
        name="crescimento", description="Analisa entradas, saídas e saldo de membros por período."
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.describe(
        periodo="Janela pronta; padrão: últimos 7 dias. Use datas sem selecionar período.",
        inicio="Data inicial: AAAA-MM-DD ou DD/MM/AAAA.",
        fim="Data final inclusiva: AAAA-MM-DD ou DD/MM/AAAA.",
        tipo="Inclua pessoas, bots ou ambos.",
    )
    @app_commands.choices(
        periodo=[
            app_commands.Choice(name=label, value=value)
            for label, value in (
                ("24h · últimas 24 horas", "24h"),
                ("7d · últimos 7 dias", "7d"),
                ("30d · últimos 30 dias", "30d"),
                ("90d · últimos 90 dias", "90d"),
            )
        ],
        tipo=[
            app_commands.Choice(name=label, value=value)
            for label, value in (
                ("Pessoas e bots", "all"),
                ("Somente pessoas", "people"),
                ("Somente bots", "bots"),
            )
        ],
    )
    async def growth(
        self,
        interaction: discord.Interaction,
        periodo: str | None = None,
        inicio: str | None = None,
        fim: str | None = None,
        tipo: str = "all",
    ) -> None:
        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(
                MISSING_MANAGE_GUILD_PERMISSION_MESSAGE,
                ephemeral=True,
            )
            return
        if interaction.guild is None:
            await interaction.response.send_message(
                "Execute dentro de um servidor.", ephemeral=True
            )
            return
        try:
            query = GrowthQuery(
                interaction.guild.id,
                growth_window(
                    period=periodo,
                    start=inicio,
                    end=fim,
                    now=self._now(),
                ),
                tipo,
            )
        except ValueError as error:
            await interaction.response.send_message(str(error), ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        try:
            report = await self._analysis.execute(query)
        except GrowthStorageError:
            logger.exception("Falha ao consultar crescimento: guild=%s.", interaction.guild.id)
            await interaction.followup.send(
                "Não consegui consultar o histórico agora. Tente novamente mais tarde.",
                ephemeral=True,
            )
            return

        embed = growth_embed(report)
        files = []
        if interaction.app_permissions.attach_files:
            files.append(
                discord.File(BytesIO(growth_csv(report)), filename="crescimento_diario.csv")
            )
        else:
            embed.add_field(
                name="CSV",
                value="Conceda Anexar arquivos ao bot para receber a série completa.",
                inline=False,
            )
        await interaction.followup.send(
            embed=embed,
            files=files,
            ephemeral=True,
            allowed_mentions=discord.AllowedMentions.none(),
        )


async def setup(bot: commands.Bot) -> None:
    discord_bot = cast(DiscordBot, bot)
    await bot.add_cog(ServerGrowth(bot, discord_bot.growth_repository))
