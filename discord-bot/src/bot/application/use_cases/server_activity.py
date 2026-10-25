"""Seleciona os eventos de atividade habilitados para publicação."""

from typing import Protocol

from bot.domain.activity import ServerActivity


class ActivityPublisher(Protocol):
    async def publish(self, event: ServerActivity) -> None: ...


class RecordServerActivity:
    def __init__(self, publisher: ActivityPublisher, enabled_categories: frozenset[str]) -> None:
        self._publisher = publisher
        self._enabled_categories = enabled_categories

    async def execute(self, event: ServerActivity) -> None:
        if event.category in self._enabled_categories:
            await self._publisher.publish(event)
