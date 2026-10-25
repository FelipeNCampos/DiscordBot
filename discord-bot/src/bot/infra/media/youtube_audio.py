"""Extração segura de URLs temporárias de áudio do YouTube, sem downloads."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

from bot.application.errors import YouTubeAudioError
from bot.domain.media import normalize_youtube_video_url
from bot.domain.models import YouTubeAudio

logger = logging.getLogger(__name__)

YTDL_OPTIONS: dict[str, object] = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "socket_timeout": 15,
    # O YouTube exige JavaScript para alguns desafios de reprodução. O Node.js
    # é instalado no host; caso esteja ausente, o yt-dlp mantém seu erro seguro.
    "js_runtimes": {"node": {}},
}


class YouTubeAudioService:
    """Obtém stream temporário em uma thread, preservando o event loop do bot."""

    def __init__(
        self,
        extractor_factory: Callable[[dict[str, object]], Any] | None = None,
        *,
        cookies_file: str | None = None,
    ) -> None:
        self._extractor_factory = extractor_factory
        self._cookies_file = cookies_file

    async def get_audio_source(self, url: str) -> YouTubeAudio:
        """Extrai metadados e uma URL de áudio sem gravar arquivos em disco."""
        try:
            return await asyncio.to_thread(self._extract, url)
        except YouTubeAudioError:
            raise
        except Exception as error:
            logger.warning(
                "Falha inesperada ao extrair áudio do host %s: %s.",
                self._host(url),
                type(error).__name__,
            )
            raise YouTubeAudioError("Não foi possível extrair o áudio do vídeo.") from None

    def _extract(self, url: str) -> YouTubeAudio:
        """Executa a parte bloqueante do yt-dlp fora do loop assíncrono."""
        video_url = normalize_youtube_video_url(url)
        options = YTDL_OPTIONS.copy()
        if self._cookies_file is not None:
            options["cookiefile"] = self._cookies_file
        try:
            factory = self._extractor_factory or self._default_extractor_factory()
            with factory(options) as extractor:
                payload = extractor.extract_info(video_url, download=False)
        except Exception as error:
            logger.warning(
                "yt-dlp recusou um vídeo do host %s: %s.", self._host(url), type(error).__name__
            )
            raise YouTubeAudioError("Não foi possível obter áudio desse vídeo.") from None

        if not isinstance(payload, dict) or not isinstance(payload.get("url"), str):
            raise YouTubeAudioError("O vídeo não forneceu uma fonte de áudio compatível.")
        title = payload.get("title")
        webpage_url = payload.get("webpage_url")
        duration = payload.get("duration")
        return YouTubeAudio(
            stream_url=payload["url"],
            title=title if isinstance(title, str) and title else "Áudio sem título",
            webpage_url=webpage_url if isinstance(webpage_url, str) else url,
            duration=duration if isinstance(duration, int) else None,
        )

    @staticmethod
    def _default_extractor_factory() -> Callable[[dict[str, object]], Any]:
        """Importa yt-dlp apenas quando a integração for efetivamente usada."""
        try:
            import yt_dlp
        except ImportError as error:
            raise YouTubeAudioError("yt-dlp não está instalado no servidor.") from error
        return yt_dlp.YoutubeDL

    @staticmethod
    def _host(url: str) -> str:
        """Retorna somente o host, seguro para logs."""
        return (urlparse(url).hostname or "desconhecido").lower()
