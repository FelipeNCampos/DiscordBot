"""Instantâneos e resultados de diagnóstico independentes da API do Discord."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class ChannelSnapshot:
    label: str
    setting_key: str
    channel_id: int | None
    exists: bool = False
    same_guild: bool = False
    valid_type: bool = False
    missing_permissions: tuple[str, ...] = ()
    required: bool = False
    publicly_visible: bool = False


@dataclass(frozen=True, slots=True)
class RoleSnapshot:
    label: str
    role_id: int
    exists: bool
    assignable: bool
    requires_assignment: bool = True


@dataclass(frozen=True, slots=True)
class ServerSnapshot:
    connected: bool
    latency_ms: int | None
    members_intent: bool
    moderation_intent: bool
    messages_intent: bool
    bot_member_available: bool
    channels: tuple[ChannelSnapshot, ...] = ()
    roles: tuple[RoleSnapshot, ...] = ()


@dataclass(frozen=True, slots=True)
class DiagnosticCheck:
    label: str
    status: Literal["ok", "warning", "error", "disabled"]
    detail: str


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    checks: tuple[DiagnosticCheck, ...]

    @property
    def has_errors(self) -> bool:
        return any(check.status == "error" for check in self.checks)
