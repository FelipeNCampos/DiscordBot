"""Classificação de publicações e validação de links de vídeo."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from bot.domain.models import InstagramMedia

MAX_YOUTUBE_URL_LENGTH = 2_048
YOUTUBE_HOSTS = frozenset(
    {"youtube.com", "www.youtube.com", "music.youtube.com", "youtu.be", "www.youtu.be"}
)


def is_valid_youtube_url(value: str) -> bool:
    """Aceita links públicos que apontem para um vídeo específico do YouTube."""
    url = value.strip()
    if not url or len(url) > MAX_YOUTUBE_URL_LENGTH:
        return False
    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower().rstrip(".")
        port = parsed.port
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"} or hostname not in YOUTUBE_HOSTS:
        return False
    if parsed.username or parsed.password or port is not None:
        return False
    query = parse_qs(parsed.query)
    if hostname in {"youtu.be", "www.youtu.be"}:
        return bool(parsed.path.strip("/"))
    return bool(query.get("v") or parsed.path.startswith("/shorts/"))


def normalize_youtube_video_url(value: str) -> str:
    """Retorna a URL canônica de um vídeo e descarta parâmetros de playlist/rádio."""
    parsed = urlparse(value.strip())
    hostname = (parsed.hostname or "").lower().rstrip(".")
    query = parse_qs(parsed.query)

    if hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/", maxsplit=1)[0]
    elif parsed.path.startswith("/shorts/"):
        video_id = parsed.path.removeprefix("/shorts/").split("/", maxsplit=1)[0]
    else:
        video_id = query.get("v", [""])[0]

    return f"https://www.youtube.com/watch?v={video_id}"


def is_instagram_reel(media: InstagramMedia) -> bool:
    return (media.media_product_type or media.media_type or "").upper() == "REELS"


def is_instagram_post(media: InstagramMedia) -> bool:
    return not is_instagram_reel(media) and (
        media.media_product_type is None or media.media_product_type.upper() == "FEED"
    )
