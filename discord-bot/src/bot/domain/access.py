"""Política de acesso aos comandos, independente da representação do Discord."""

from collections.abc import Iterable

PUBLIC_COMMANDS = frozenset({"chamar", "id_usuario"})


def can_use_command(
    command_name: str | None,
    required_role_id: int | None,
    member_role_ids: Iterable[int],
    *,
    in_guild: bool,
) -> bool:
    if required_role_id is None or command_name in PUBLIC_COMMANDS:
        return True
    return in_guild and required_role_id in member_role_ids
