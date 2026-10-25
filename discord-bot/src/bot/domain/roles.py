"""Mapeamentos e regras de associação de cargos por reação."""

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoleReactionOption:
    """Vínculo seguro entre um emoji configurado e um cargo do Discord."""

    emoji: str
    role_id: int

    @property
    def emoji_keys(self) -> frozenset[str]:
        """Retorna chaves compatíveis com emojis Unicode e personalizados."""
        keys = {self.emoji}
        custom_emoji = re.fullmatch(r"<a?:[^:]+:(\d+)>", self.emoji)
        if custom_emoji is not None:
            keys.add(custom_emoji.group(1))
        return frozenset(keys)


@dataclass(frozen=True, slots=True)
class RoleCategorySettings:
    """Configuração de uma mensagem de cargos por reação."""

    name: str
    message_id: int | None
    options: tuple[RoleReactionOption, ...]
    exclusive: bool

    def role_id_for_emoji(self, emoji: str, emoji_id: int | None) -> int | None:
        """Localiza somente um cargo explicitamente autorizado para o emoji."""
        candidate_keys = {emoji}
        if emoji_id is not None:
            candidate_keys.add(str(emoji_id))
        for option in self.options:
            if option.emoji_keys.intersection(candidate_keys):
                return option.role_id
        return None


@dataclass(frozen=True, slots=True)
class RoleMenuSettings:
    """Configuração opcional dos cargos automáticos e menus por reação."""

    auto_role_id: int | None
    channel_id: int | None
    categories: tuple[RoleCategorySettings, ...]

    @property
    def has_reaction_menu(self) -> bool:
        """Indica se há ao menos uma mensagem de reação configurada."""
        return self.channel_id is not None and any(
            category.message_id is not None and category.options for category in self.categories
        )
