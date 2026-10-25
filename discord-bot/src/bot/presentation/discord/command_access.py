"""Controle global de acesso aos comandos slash por cargo Discord."""

from __future__ import annotations

import logging

import discord
from discord import app_commands

from bot.domain.access import can_use_command

logger = logging.getLogger(__name__)

COMMAND_REQUIRED_ROLE_MESSAGE = "Você não possui o cargo necessário para usar comandos do bot."


class CommandAccessTree(app_commands.CommandTree):
    """Impede comandos restritos, preservando exceções públicas explícitas."""

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Valida o cargo antes de qualquer comando registrado na árvore."""
        settings = getattr(self.client, "settings", None)
        required_role_id = getattr(settings, "command_required_role_id", None)
        command_name = interaction.command.qualified_name if interaction.command else None
        if can_use_command(
            command_name,
            required_role_id,
            (role.id for role in getattr(interaction.user, "roles", ())),
            in_guild=interaction.guild is not None,
        ):
            return True

        logger.warning(
            "Comando slash recusado por cargo: usuário=%s guild=%s comando=%s.",
            interaction.user.id,
            interaction.guild_id,
            command_name or "desconhecido",
        )
        if interaction.response.is_done():
            await interaction.followup.send(COMMAND_REQUIRED_ROLE_MESSAGE, ephemeral=True)
        else:
            await interaction.response.send_message(COMMAND_REQUIRED_ROLE_MESSAGE, ephemeral=True)
        return False
