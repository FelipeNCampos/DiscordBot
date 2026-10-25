"""Registros de membros, moderação, cargos, canais e metadados de mensagens."""

from __future__ import annotations

from typing import cast

import discord
from discord.ext import commands

from bot.application.use_cases.server_activity import RecordServerActivity
from bot.config.settings import Settings
from bot.domain.activity import ServerActivity
from bot.presentation.discord.activity_log_sender import ActivityLogSender


class MemberActivityLogs(commands.Cog):
    def __init__(self, bot: commands.Bot, settings: Settings) -> None:
        self._bot = bot
        self._recorder = RecordServerActivity(
            ActivityLogSender(
                bot,
                activity_channel_id=settings.activity_log_channel_id,
                member_channel_id=settings.member_log_channel_id,
            ),
            settings.activity_log_events,
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self._recorder.execute(
            ServerActivity(
                "members",
                "Entrada de membro",
                member.guild.id,
                member.id,
                member_action="join",
            )
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        await self._recorder.execute(
            ServerActivity(
                "members",
                "Saída de membro",
                member.guild.id,
                member.id,
                member_action="leave",
            )
        )

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        before_roles = {role.id for role in before.roles}
        after_roles = {role.id for role in after.roles}
        changes = []
        if before.nick != after.nick:
            changes.append("Apelido alterado.")
        if added := after_roles - before_roles:
            changes.append("Cargos adicionados: " + ", ".join(map(str, sorted(added))))
        if removed := before_roles - after_roles:
            changes.append("Cargos removidos: " + ", ".join(map(str, sorted(removed))))
        if changes:
            await self._recorder.execute(
                ServerActivity(
                    "members",
                    "Membro atualizado",
                    after.guild.id,
                    after.id,
                    tuple(changes),
                )
            )
        if before.timed_out_until != after.timed_out_until:
            detail = (
                f"Restrição até {after.timed_out_until.isoformat()}."
                if after.timed_out_until
                else "Restrição de comunicação removida."
            )
            await self._recorder.execute(
                ServerActivity(
                    "moderation",
                    "Timeout atualizado",
                    after.guild.id,
                    after.id,
                    (detail,),
                )
            )

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User) -> None:
        await self._recorder.execute(
            ServerActivity("moderation", "Membro banido", guild.id, user.id)
        )

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User) -> None:
        await self._recorder.execute(
            ServerActivity(
                "moderation",
                "Banimento removido",
                guild.id,
                user.id,
            )
        )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        await self._channel_event(channel, "Canal criado")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        await self._channel_event(channel, "Canal excluído")

    async def _channel_event(self, channel: discord.abc.GuildChannel, title: str) -> None:
        await self._recorder.execute(
            ServerActivity(
                "channels",
                title,
                channel.guild.id,
                channel.id,
                (f"Nome: {channel.name}",),
            )
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self,
        before: discord.abc.GuildChannel,
        after: discord.abc.GuildChannel,
    ) -> None:
        attributes = {
            "name": "nome",
            "category_id": "categoria",
            "overwrites": "permissões",
            "topic": "tópico",
            "slowmode_delay": "modo lento",
            "nsfw": "restrição etária",
            "user_limit": "limite de usuários",
            "bitrate": "qualidade de áudio",
        }
        changed = [
            label
            for name, label in attributes.items()
            if getattr(before, name, None) != getattr(after, name, None)
        ]
        if changed:
            await self._recorder.execute(
                ServerActivity(
                    "channels",
                    "Canal atualizado",
                    after.guild.id,
                    after.id,
                    ("Alterações: " + ", ".join(changed),),
                )
            )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        await self._role_event(role, "Cargo criado")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self._role_event(role, "Cargo excluído")

    async def _role_event(self, role: discord.Role, title: str) -> None:
        await self._recorder.execute(
            ServerActivity(
                "roles",
                title,
                role.guild.id,
                role.id,
                (f"Nome: {role.name}",),
            )
        )

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role) -> None:
        attributes = {
            "name": "nome",
            "permissions": "permissões",
            "position": "hierarquia",
            "colour": "cor",
            "hoist": "exibição separada",
            "mentionable": "menções",
        }
        changed = [
            label
            for name, label in attributes.items()
            if getattr(before, name, None) != getattr(after, name, None)
        ]
        if changed:
            await self._recorder.execute(
                ServerActivity(
                    "roles",
                    "Cargo atualizado",
                    after.guild.id,
                    after.id,
                    ("Alterações: " + ", ".join(changed),),
                )
            )

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent) -> None:
        if payload.guild_id is None:
            return
        author = getattr(payload.cached_message, "author", None)
        if self._is_self(author):
            return
        detail = (
            f"Autor da mensagem: {author.id}"
            if author
            else "Autor da mensagem indisponível: fora do cache."
        )
        await self._recorder.execute(
            ServerActivity(
                "messages",
                "Mensagem excluída",
                payload.guild_id,
                payload.message_id,
                (detail,),
                channel_id=payload.channel_id,
            )
        )

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload: discord.RawBulkMessageDeleteEvent) -> None:
        if payload.guild_id is None or not payload.message_ids:
            return
        await self._recorder.execute(
            ServerActivity(
                "messages",
                "Exclusão de mensagens em lote",
                payload.guild_id,
                payload.channel_id,
                (f"Quantidade: {len(payload.message_ids)}",),
                channel_id=payload.channel_id,
            )
        )

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent) -> None:
        if payload.guild_id is None or not {"content", "attachments"}.intersection(payload.data):
            return
        author = payload.data.get("author", {})
        if self._bot.user is not None and author.get("id") == str(self._bot.user.id):
            return
        cached = payload.cached_message
        if cached is not None and self._is_self(cached.author):
            return
        # Payloads raw funcionam sem buscar mensagens antigas nem armazenar seu conteúdo.
        await self._recorder.execute(
            ServerActivity(
                "messages",
                "Mensagem editada",
                payload.guild_id,
                payload.message_id,
                ("Conteúdo e anexos não são copiados para o registro.",),
                channel_id=payload.channel_id,
            )
        )

    def _is_self(self, user: discord.User | discord.Member | None) -> bool:
        return user is not None and self._bot.user is not None and user.id == self._bot.user.id


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemberActivityLogs(bot, cast(Settings, bot.settings)))
