"""Metadados mínimos de eventos administrativos, sem conteúdo de mensagens."""

from dataclasses import dataclass

ACTIVITY_CATEGORIES = frozenset({"members", "moderation", "channels", "roles", "messages"})
DEFAULT_ACTIVITY_CATEGORIES = ACTIVITY_CATEGORIES - {"messages"}


@dataclass(frozen=True, slots=True)
class ServerActivity:
    category: str
    title: str
    guild_id: int
    subject_id: int
    details: tuple[str, ...] = ()
    channel_id: int | None = None
    member_action: str | None = None
