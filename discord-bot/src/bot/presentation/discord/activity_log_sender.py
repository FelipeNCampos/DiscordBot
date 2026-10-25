"""Publica logs sem pings e impede vazamento de eventos entre servidores."""

from __future__ import annotations

import logging

import discord
from discord.ext import commands

from bot.domain.activity import ServerActivity

logger = logging.getLogger(__name__)


class ActivityLogSender:
    def __init__(
        self,
        bot: commands.Bot,
        *,
        activity_channel_id: int | None = None,
        member_channel_id: int | None = None,
    ) -> None:
        self._bot = bot
        self._activity_channel_id = activity_channel_id
        self._member_channel_id = member_channel_id

    async def publish(self, event: ServerActivity) -> None:
        channel_id = (
            self._member_channel_id
            if event.member_action and self._member_channel_id
            else self._activity_channel_id or self._member_channel_id
        )
        if channel_id is None:
            return
        if event.category == "messages" and event.channel_id in {
            self._activity_channel_id,
            self._member_channel_id,
        }:
            return
        try:
            channel = self._bot.get_channel(channel_id)
            if channel is None:
                channel = await self._bot.fetch_channel(channel_id)
            guild = getattr(channel, "guild", None)
            if guild is None or guild.id != event.guild_id:
                logger.warning(
                    "Canal de atividade %s não pertence ao servidor %s.", channel_id, event.guild_id
                )
                return
            if not callable(getattr(channel, "send", None)):
                logger.warning("Canal de atividade %s não aceita mensagens.", channel_id)
                return
            await channel.send(self._format(event), allowed_mentions=discord.AllowedMentions.none())
        except (discord.NotFound, discord.Forbidden):
            logger.warning("Canal de atividade %s indisponível ou sem permissão.", channel_id)
        except discord.HTTPException as error:
            logger.warning(
                "Falha ao publicar atividade no canal %s: status=%s.", channel_id, error.status
            )

    @staticmethod
    def _format(event: ServerActivity) -> str:
        if event.member_action in {"join", "leave"}:
            icon, action = (
                ("📥", "entrou no servidor")
                if event.member_action == "join"
                else ("📤", "saiu do servidor")
            )
            return f"{icon} <@{event.subject_id}> {action}. (ID: {event.subject_id})"
        details = [
            discord.utils.escape_mentions(discord.utils.escape_markdown(detail))
            for detail in event.details
        ]
        message = f"📋 **{event.title}**\nID: {event.subject_id} · Servidor: {event.guild_id}"
        if event.channel_id is not None:
            message += f" · Canal: {event.channel_id}"
        return (message + "\n" + "\n".join(details))[:1900]
