"""Falhas seguras que os casos de uso podem tratar sem conhecer os adaptadores."""


class InstagramAPIError(RuntimeError):
    """Erro seguro para falhas na API oficial do Instagram."""


class InstagramAuthenticationError(InstagramAPIError):
    """Indica token inválido, expirado ou revogado."""


class InstagramTokenExpiredError(InstagramAuthenticationError):
    """Indica que o token já expirou e precisa de nova autorização manual."""


class InstagramTokenRevokedError(InstagramAuthenticationError):
    """Indica que o token foi revogado ou perdeu a autorização."""


class InstagramTokenRefreshError(InstagramAPIError):
    """Indica que a renovação não foi concluída por uma falha recuperável."""


class InstagramPermissionError(InstagramAPIError):
    """Indica que o token não tem permissões para a conta configurada."""


class InstagramProfileNotFoundError(InstagramAPIError):
    """Indica que a conta profissional autorizada não foi encontrada."""


class InstagramRateLimitError(InstagramAPIError):
    """Indica que a API aplicou limite de requisições."""


class TwitchError(RuntimeError):
    """Erro seguro e genérico de uma integração com a Twitch."""


class TwitchAuthenticationError(TwitchError):
    """Falha ao autenticar a aplicação Twitch."""


class TwitchInvalidClientError(TwitchAuthenticationError):
    """Client ID ou Client Secret foram recusados pela Twitch."""


class TwitchTokenError(TwitchAuthenticationError):
    """Token Twitch inválido, expirado ou com resposta de validação incorreta."""


class TwitchApiError(TwitchError):
    """Falha segura em uma chamada à API Helix ou EventSub."""


class InstagramTokenStoreError(RuntimeError):
    """Falha segura ao ler ou persistir o token Instagram."""


class InstagramOAuthError(RuntimeError):
    """Erro seguro do fluxo OAuth, apropriado para uma resposta HTTP genérica."""


class YouTubeAudioError(RuntimeError):
    """Indica uma falha segura durante extração de áudio."""


class DiscordNotificationError(RuntimeError):
    """Indica que uma notificação não pôde ser entregue no Discord."""


class GrowthStorageError(RuntimeError):
    """Falha segura ao registrar ou consultar movimentações do servidor."""
