"""Descobre novas publicações e registra apenas entregas confirmadas."""

from __future__ import annotations

from bot.application.ports import (
    InstagramMediaClient,
    InstagramMediaRepository,
    InstagramNotificationSender,
)
from bot.domain.models import InstagramMedia


class PollInstagramMedia:
    def __init__(
        self,
        client: InstagramMediaClient,
        repository: InstagramMediaRepository,
        sender: InstagramNotificationSender,
        *,
        notify_existing_latest: bool = False,
    ) -> None:
        self._client = client
        self._repository = repository
        self._sender = sender
        self._notify_existing_latest = notify_existing_latest
        self._initial_sync_completed = False

    async def execute(self) -> None:
        media_items = await self._client.list_recent_media()
        if not media_items:
            self._initial_sync_completed = True
            return

        if not self._initial_sync_completed:
            await self._initialize_history(media_items)
            self._initial_sync_completed = True
            return

        for media in sorted(media_items, key=lambda item: item.timestamp):
            await self._notify_if_new(media)

    async def _initialize_history(self, media_items: list[InstagramMedia]) -> None:
        latest = max(media_items, key=lambda media: media.timestamp)
        for media in media_items:
            if media.media_id == latest.media_id:
                continue
            await self._mark_known_if_new(media)

        if self._notify_existing_latest:
            await self._notify_if_new(latest)
        else:
            await self._mark_known_if_new(latest)

    async def _mark_known_if_new(self, media: InstagramMedia) -> None:
        if not await self._repository.has_processed_instagram_media(media.media_id):
            await self._repository.mark_instagram_media_processed(media, status="known")

    async def _notify_if_new(self, media: InstagramMedia) -> None:
        if await self._repository.has_processed_instagram_media(media.media_id):
            return
        await self._sender.send_instagram_notification(media)
        await self._repository.mark_instagram_media_processed(media, status="notified")
