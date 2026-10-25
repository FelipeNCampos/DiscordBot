"""Lê o cache do Discord e traduz recursos para dados de diagnóstico."""

from __future__ import annotations

import math
from dataclasses import replace

import discord
from discord.ext import commands

from bot.config.settings import Settings
from bot.domain.diagnostics import ChannelSnapshot, RoleSnapshot, ServerSnapshot

PERMISSION_LABELS = {
    "view_channel": "Ver canal",
    "send_messages": "Enviar mensagens",
    "embed_links": "Inserir links",
    "attach_files": "Anexar arquivos",
    "read_message_history": "Ler histórico",
    "add_reactions": "Adicionar reações",
    "manage_messages": "Gerenciar mensagens",
    "manage_channels": "Gerenciar canais",
    "connect": "Conectar",
    "move_members": "Mover membros",
}
TEXT_PERMISSIONS = ("view_channel", "send_messages")


def collect_server_snapshot(
    bot: commands.Bot,
    guild: discord.Guild,
    settings: Settings,
) -> ServerSnapshot:
    channels = [
        _log_channel(
            bot,
            guild,
            "Logs de membros",
            "DISCORD_MEMBER_LOG_CHANNEL_ID",
            settings.member_log_channel_id,
        ),
        _log_channel(
            bot,
            guild,
            "Logs de atividade",
            "DISCORD_ACTIVITY_LOG_CHANNEL_ID",
            settings.activity_log_channel_id or settings.member_log_channel_id,
        ),
        _channel(
            bot,
            guild,
            "Reações de mídia",
            "DISCORD_MEDIA_REACTION_CHANNEL_ID",
            settings.media_reaction_channel_id,
            ("view_channel", "read_message_history", "add_reactions"),
        ),
        _channel(
            bot,
            guild,
            "Menu de cargos",
            "DISCORD_ROLE_MENU_CHANNEL_ID",
            settings.role_menu.channel_id,
            (*TEXT_PERMISSIONS, "read_message_history", "add_reactions", "manage_messages"),
        ),
        _channel(
            bot,
            guild,
            "Criador de salas",
            "DISCORD_TEMPORARY_VOICE_CREATOR_CHANNEL_ID",
            settings.temporary_voice_creator_channel_id,
            ("view_channel", "connect", "manage_channels", "move_members"),
            voice=True,
        ),
    ]
    for enabled, label, key, channel_id in (
        (
            settings.twitch.enabled,
            "Notificações Twitch",
            "DISCORD_NOTIFICATION_CHANNEL_ID",
            settings.twitch.notification_channel_id,
        ),
        (
            settings.instagram.enabled,
            "Notificações Instagram",
            "DISCORD_INSTAGRAM_CHANNEL_ID",
            settings.instagram.notification_channel_id,
        ),
    ):
        if enabled:
            channels.append(
                _channel(
                    bot,
                    guild,
                    label,
                    key,
                    channel_id,
                    (*TEXT_PERMISSIONS, "embed_links", "attach_files"),
                    mandatory=True,
                )
            )

    roles = []
    if settings.command_required_role_id is not None:
        roles.append(
            _role(
                guild,
                "Acesso aos comandos",
                settings.command_required_role_id,
                requires_assignment=False,
            )
        )
    if settings.role_menu.auto_role_id is not None:
        roles.append(_role(guild, "Cargo automático", settings.role_menu.auto_role_id))
    seen_roles = {role.role_id for role in roles if role.requires_assignment}
    for category in settings.role_menu.categories:
        for option in category.options:
            if option.role_id not in seen_roles:
                roles.append(_role(guild, f"Cargo do menu: {category.name}", option.role_id))
                seen_roles.add(option.role_id)

    latency = bot.latency
    return ServerSnapshot(
        connected=bot.is_ready(),
        latency_ms=round(latency * 1000) if math.isfinite(latency) else None,
        members_intent=bot.intents.members,
        moderation_intent=bot.intents.moderation,
        messages_intent=bot.intents.guild_messages,
        bot_member_available=guild.me is not None,
        channels=tuple(channels),
        roles=tuple(roles),
    )


def _channel(
    bot: commands.Bot,
    guild: discord.Guild,
    label: str,
    key: str,
    channel_id: int | None,
    required: tuple[str, ...],
    *,
    voice: bool = False,
    mandatory: bool = False,
) -> ChannelSnapshot:
    if channel_id is None:
        return ChannelSnapshot(label, key, None, required=mandatory)
    channel = guild.get_channel(channel_id) or bot.get_channel(channel_id)
    if channel is None:
        return ChannelSnapshot(label, key, channel_id)
    same_guild = getattr(getattr(channel, "guild", None), "id", None) == guild.id
    valid_type = (
        isinstance(channel, discord.VoiceChannel)
        if voice
        else (isinstance(channel, discord.TextChannel))
    )
    permissions = channel.permissions_for(guild.me) if same_guild and guild.me else None
    missing = tuple(
        PERMISSION_LABELS[name]
        for name in required
        if permissions is None or not getattr(permissions, name, False)
    )
    return ChannelSnapshot(label, key, channel_id, True, same_guild, valid_type, missing)


def _log_channel(
    bot: commands.Bot,
    guild: discord.Guild,
    label: str,
    key: str,
    channel_id: int | None,
) -> ChannelSnapshot:
    snapshot = _channel(bot, guild, label, key, channel_id, TEXT_PERMISSIONS)
    if not snapshot.same_guild or not snapshot.valid_type:
        return snapshot
    channel = guild.get_channel(channel_id) or bot.get_channel(channel_id)
    return replace(
        snapshot, publicly_visible=channel.permissions_for(guild.default_role).view_channel
    )


def _role(
    guild: discord.Guild,
    label: str,
    role_id: int,
    *,
    requires_assignment: bool = True,
) -> RoleSnapshot:
    role = guild.get_role(role_id)
    member = guild.me
    assignable = bool(
        role is not None
        and member is not None
        and member.guild_permissions.manage_roles
        and not role.is_default()
        and not role.managed
        and role < member.top_role
    )
    return RoleSnapshot(label, role_id, role is not None, assignable, requires_assignment)
