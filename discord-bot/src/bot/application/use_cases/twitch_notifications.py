"""Recebe eventos e entrega lives confirmadas sem depender de HTTP ou Discord."""

from __future__ import annotations

import contextlib
import logging

from bot.application.ports import (
    CurrentTwitchLiveRepository,
    TwitchEventQueue,
    TwitchEventRepository,
    TwitchNotificationSender,
    TwitchStreamClient,
)
from bot.domain.models import TwitchOnlineEvent

logger = logging.getLogger(__name__)


class ReceiveTwitchEvent:
    def __init__(self, repository: TwitchEventRepository, queue: TwitchEventQueue) -> None:
        self._repository = repository
        self._queue = queue

    async def execute(self, event: TwitchOnlineEvent) -> None:
        if await self._repository.register_twitch_event(event):
            self._queue.queue_twitch_notification(event)


class NotifyTwitchLive:
    def __init__(
        self,
        client: TwitchStreamClient,
        repository: TwitchEventRepository,
        current_live: CurrentTwitchLiveRepository,
        sender: TwitchNotificationSender,
    ) -> None:
        self._client = client
        self._repository = repository
        self._current_live = current_live
        self._sender = sender

    async def execute(self, event: TwitchOnlineEvent) -> None:
        try:
            stream = await self._client.get_stream(event.broadcaster_user_id)
            await self._current_live.set_current(event, stream)
            if not stream.is_live:
                await self._repository.update_twitch_event_status(event.message_id, "offline")
                logger.info("Live Twitch encerrada antes do envio da notificação.")
                return
            await self._sender.send_twitch_notification(event, stream)
            await self._repository.update_twitch_event_status(event.message_id, "notified")
            logger.info("Notificação de live da Twitch enviada.")
        except Exception:
            with contextlib.suppress(Exception):
                await self._repository.update_twitch_event_status(event.message_id, "failed")
            raise
