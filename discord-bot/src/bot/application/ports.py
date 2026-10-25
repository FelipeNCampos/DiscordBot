"""Contratos mínimos usados pelos casos de uso e implementados pelos adaptadores."""

from __future__ import annotations

from typing import Protocol

from bot.domain.models import (
    CurrentTwitchLive,
    InstagramMedia,
    InstagramTokenData,
    InstagramTokenRefreshResult,
    TwitchOnlineEvent,
    TwitchStream,
    YouTubeAudio,
)


class InstagramMediaClient(Protocol):
    async def list_recent_media(self) -> list[InstagramMedia]: ...


class InstagramTokenRefreshClient(Protocol):
    async def refresh_access_token(self, access_token: str) -> InstagramTokenRefreshResult: ...


class InstagramTokenStore(Protocol):
    async def get_token(self) -> InstagramTokenData | None: ...

    async def save_token(self, token: InstagramTokenData) -> None: ...


class InstagramGateway(InstagramMediaClient, InstagramTokenRefreshClient, Protocol):
    async def aclose(self) -> None: ...


class InstagramMediaRepository(Protocol):
    async def has_processed_instagram_media(self, media_id: str) -> bool: ...

    async def mark_instagram_media_processed(
        self, media: InstagramMedia, *, status: str = "notified"
    ) -> None: ...


class TwitchEventRepository(Protocol):
    async def register_twitch_event(self, event: TwitchOnlineEvent) -> bool: ...

    async def update_twitch_event_status(self, message_id: str, status: str) -> None: ...


class NotificationRepository(InstagramMediaRepository, TwitchEventRepository, Protocol):
    async def initialize(self) -> None: ...


class InstagramNotificationSender(Protocol):
    async def send_instagram_notification(self, media: InstagramMedia) -> None: ...


class TwitchNotificationSender(Protocol):
    async def send_twitch_notification(
        self, event: TwitchOnlineEvent, stream: TwitchStream
    ) -> None: ...


class CurrentTwitchLiveRepository(Protocol):
    async def set_current(self, event: TwitchOnlineEvent, stream: TwitchStream) -> None: ...

    async def get_current(self) -> CurrentTwitchLive | None: ...

    async def clear_if_current(self, live: CurrentTwitchLive) -> bool: ...

    async def update_stream_if_current(
        self, live: CurrentTwitchLive, stream: TwitchStream
    ) -> CurrentTwitchLive | None: ...


class TwitchStreamClient(Protocol):
    async def get_stream(self, broadcaster_user_id: str) -> TwitchStream: ...

    async def get_user_by_login(self, login: str | None = None) -> tuple[str, str, str]: ...


class TwitchTokenClient(Protocol):
    async def ensure_valid_access_token(self) -> None: ...


class TwitchGateway(TwitchStreamClient, TwitchTokenClient, Protocol):
    @property
    def resolved_broadcaster_user_id(self) -> str | None: ...

    async def aclose(self) -> None: ...


class TwitchEventQueue(Protocol):
    def queue_twitch_notification(self, event: TwitchOnlineEvent) -> None: ...


class BackgroundTask(Protocol):
    def start(self) -> None: ...

    async def stop(self) -> None: ...


class AudioSource(Protocol):
    async def get_audio_source(self, url: str) -> YouTubeAudio: ...


class InstagramOAuthService(Protocol):
    def authorization_url(self, state: str) -> str: ...

    async def authorize(self, code: str) -> object: ...
