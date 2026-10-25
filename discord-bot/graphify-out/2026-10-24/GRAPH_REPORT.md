# Graph Report - discord-bot  (2026-10-24)

## Corpus Check
- 96 files · ~429,733 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .example 1)

## Summary
- 1807 nodes · 3919 edges · 84 communities (60 shown, 23 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 474 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b698f603`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DiscordBot
- test_role_management.py
- test_temporary_voice.py
- diagnose_server
- test_welcome.py
- .on_raw_reaction_add
- Settings
- test_live_commands.py
- TemporaryVoice
- test_media_reactions.py
- application/errors.py
- InstagramOAuthClient
- TwitchStream
- test_cleanup_command.py
- test_music.py
- .play_youtube
- InstagramTokenData
- test_instagram.py
- settings.py
- ports.py
- test_twitch.py
- test_discord_sender.py
- test_run_services_composes_single_bot_and_cleans_up_tasks
- MemberActivityLogs
- CommandAccessTree
- TwitchClient
- InstagramTokenStore
- General
- NotificationStore
- generate_deployment_article_pdf.py
- bootstrap.py
- test_instagram_oauth.py
- Configuração
- RuntimeError
- models.py
- test_call_moderator.py
- InstagramMedia
- InstagramSettings
- test_youtube_audio.py
- test_web_app_exposes_health_and_initializes_shared_store
- create_web_app
- .emoji_keys
- test_twitch_auth.py
- generate_deployment_article.py
- MediaReactions
- DiscordNotificationSender
- FakeInteractionResponse
- routes.py
- InstagramOAuthStateStore
- CurrentTwitchLiveRepository
- TwitchTokenValidator
- RoleManagement
- SecretStore
- environment
- test_architecture.py
- notification_sender.py
- InstagramAuthenticationError
- test_discord_bootstrap.py
- AwsSecretsManagerSecretStore
- InstagramPoller
- FakeTwitchClient
- application/__init__.py
- Protocol
- MemoryTokenStore
- use_cases/__init__.py
- config/__init__.py
- domain/__init__.py
- infra/__init__.py
- bot/__init__.py
- integrations/__init__.py
- .aclose
- WebSettings
- media/__init__.py
- memory/__init__.py
- persistence/__init__.py
- tasks/__init__.py
- discord-bot
- cogs/__init__.py
- discord/__init__.py
- http/__init__.py
- presentation/__init__.py
- .role_id_for_emoji
- .has_reaction_menu

## God Nodes (most connected - your core abstractions)
1. `Settings` - 122 edges
2. `InstagramMedia` - 56 edges
3. `General` - 50 edges
4. `TwitchOnlineEvent` - 42 edges
5. `InstagramTokenData` - 42 edges
6. `DiscordBot` - 42 edges
7. `ConfigurationError` - 39 edges
8. `DiscordNotificationSender` - 35 edges
9. `TwitchClient` - 34 edges
10. `InstagramClient` - 33 edges

## Surprising Connections (you probably didn't know these)
- `FakeInstagramClient` --uses--> `InstagramAPIError`  [INFERRED]
  tests/test_live_commands.py → src/bot/application/errors.py
- `test_reports_expired_or_invalid_token_without_exposing_it()` --uses--> `InstagramAuthenticationError`  [INFERRED]
  tests/test_instagram.py → src/bot/application/errors.py
- `test_refresh_reports_expired_token_without_exposing_it()` --uses--> `InstagramTokenExpiredError`  [INFERRED]
  tests/test_instagram.py → src/bot/application/errors.py
- `test_invalid_client_error_does_not_include_client_secret()` --uses--> `TwitchInvalidClientError`  [INFERRED]
  tests/test_twitch_auth.py → src/bot/application/errors.py
- `test_oauth_rejects_an_account_other_than_the_configured_profile()` --uses--> `InstagramOAuthError`  [INFERRED]
  tests/test_instagram_oauth.py → src/bot/application/errors.py

## Import Cycles
- None detected.

## Communities (84 total, 23 thin omitted)

### Community 0 - "DiscordBot"
Cohesion: 0.06
Nodes (32): AppCommandError, AudioSource, BackgroundTask, NotificationRepository, TwitchGateway, Configuração centralizada de logs., DiscordBot, Cliente principal do bot do Discord. (+24 more)

### Community 1 - "test_role_management.py"
Cohesion: 0.06
Nodes (45): discord_error(), FakeBot, FakeChannel, FakeGuild, FakeMember, FakeMessage, FakeRole, payload() (+37 more)

### Community 2 - "test_temporary_voice.py"
Cohesion: 0.06
Nodes (46): build_voice_fixture(), discord_error(), FakeBot, FakeCategory, FakeGuild, FakeMember, FakePrincipal, FakeRole (+38 more)

### Community 3 - "diagnose_server"
Cohesion: 0.11
Nodes (36): _diagnose_channel(), _diagnose_role(), diagnose_server(), Transforma fatos do servidor em problemas e correções acionáveis., ChannelSnapshot, DiagnosticCheck, DiagnosticReport, Instantâneos e resultados de diagnóstico independentes da API do Discord. (+28 more)

### Community 4 - "test_welcome.py"
Cohesion: 0.07
Nodes (31): discord_error(), FakeInteraction, FakeInteractionResponse, FakeNamedChannel, FakeWelcomeClient, FakeWelcomeUser, asyncio, HTTPException (+23 more)

### Community 5 - ".on_raw_reaction_add"
Cohesion: 0.12
Nodes (14): RawReactionActionEvent, Guild, listener, Member, Role, Remove o cargo existente ou o adiciona, respeitando exclusividade., Resolve um membro do cache e usa API somente quando necessário., Remove somente a reação do usuário depois de uma alteração bem-sucedida. (+6 more)

### Community 6 - "Settings"
Cohesion: 0.06
Nodes (64): Configuração tipada e segura para inicializar o bot., Cria as configurações a partir de variáveis de ambiente., Settings, parametrize, Testes unitários da configuração do ambiente., Variáveis removidas não voltam a ativar opções de pronomes., A ausência de token Discord deve interromper a leitura da configuração., Os formatos booleanos aceitos devem ser interpretados corretamente. (+56 more)

### Community 7 - "test_live_commands.py"
Cohesion: 0.10
Nodes (40): FakeInteraction, FakeNotificationSender, latest_instagram_media(), latest_instagram_post(), open_live(), asyncio, Testes dos comandos slash de reenvio de live e lista de comandos., Interação mínima para executar callbacks do cog diretamente. (+32 more)

### Community 8 - "TemporaryVoice"
Cohesion: 0.07
Nodes (30): Snowflake, Client, Guild, GuildChannel, listener, Lock, Member, PermissionOverwrite (+22 more)

### Community 9 - "test_media_reactions.py"
Cohesion: 0.12
Nodes (28): discord_error(), FakeAttachment, FakeMessage, media_cog(), media_reaction_settings(), asyncio, HTTPException, parametrize (+20 more)

### Community 10 - "application/errors.py"
Cohesion: 0.09
Nodes (33): InstagramAPIError, InstagramPermissionError, InstagramProfileNotFoundError, InstagramRateLimitError, InstagramTokenRefreshError, InstagramTokenRevokedError, Falhas seguras que os casos de uso podem tratar sem conhecer os adaptadores., Indica que o token foi revogado ou perdeu a autorização. (+25 more)

### Community 11 - "InstagramOAuthClient"
Cohesion: 0.17
Nodes (11): InstagramOAuthError, Erro seguro do fluxo OAuth, apropriado para uma resposta HTTP genérica., InstagramOAuthClient, Any, AsyncClient, datetime, OAuth do Instagram Login para autorizar uma conta profissional sem expor…, Executa Instagram Login, troca o código e salva apenas dados validados. (+3 more)

### Community 12 - "TwitchStream"
Cohesion: 0.16
Nodes (11): CurrentTwitchLive, Dados de uma live consultada após a notificação EventSub., Combina o evento EventSub e os dados mais recentes de uma live aberta., TwitchStream, CurrentTwitchLiveStore, Estado em memória da última live Twitch confirmada como aberta., Mantém uma única live atual com leituras e alterações consistentes. O conteúdo…, Registra a live somente se a API Twitch a confirmou como online. (+3 more)

### Community 13 - "test_cleanup_command.py"
Cohesion: 0.09
Nodes (28): cleanup_cog(), discord_error(), FakeChannel, FakeFollowup, FakeInteraction, FakeNotificationSender, FakeResponse, asyncio (+20 more)

### Community 14 - "test_music.py"
Cohesion: 0.07
Nodes (38): FakeVoiceChannel, FailingVoiceChannel, FakeBot, FakeFollowup, FakeGuild, FakeInteraction, FakeMember, FakeResponse (+30 more)

### Community 15 - ".play_youtube"
Cohesion: 0.06
Nodes (32): AbstractEventLoop, Connectable, describe, is_valid_youtube_url(), Aceita links públicos que apontem para um vídeo específico do YouTube., command, Exception, Guild (+24 more)

### Community 16 - "InstagramTokenData"
Cohesion: 0.12
Nodes (16): InstagramTokenStoreError, Falha segura ao ler ou persistir o token Instagram., InstagramTokenData, Token Instagram e metadados mantidos em um armazenamento configurado., AwsSecretsManagerInstagramTokenStore, JsonFileInstagramTokenStore, _parse_expires_at(), Grava uma resposta completa de modo atômico e atualiza o fallback em memória. (+8 more)

### Community 17 - "test_instagram.py"
Cohesion: 0.06
Nodes (60): LogCaptureFixture, InstagramTokenRefreshResult, Resultado seguro de uma renovação bem-sucedida de token Instagram., Usa o mesmo cliente HTTP para renovar um token ainda válido., FailingSender, FakeInstagramClient, FakeRefreshClient, FakeSecretStore (+52 more)

### Community 18 - "settings.py"
Cohesion: 0.07
Nodes (50): _activity_events(), _boolean(), ConfigurationError, _https_url(), _instagram_api_version(), _log_level(), _numeric_id(), _optional_https_url() (+42 more)

### Community 19 - "ports.py"
Cohesion: 0.16
Nodes (11): Contratos mínimos usados pelos casos de uso e implementados pelos adaptadores., TwitchEventQueue, TwitchEventRepository, TwitchNotificationSender, TwitchStreamClient, NotifyTwitchLive, Recebe eventos e entrega lives confirmadas sem depender de HTTP ou Discord., ReceiveTwitchEvent (+3 more)

### Community 20 - "test_twitch.py"
Cohesion: 0.14
Nodes (22): oauth_token_response(), asyncio, Response, Testes sem rede para Helix e EventSub com token Twitch renovável., Uma chamada GET recebe um token novo e é repetida uma única vez após HTTP 401., A ausência de dados de stream permite limpar a live atual sem notificar…, Retorna uma resposta OAuth curta e válida para os transportes simulados., EventSub consulta inscrições depois de 401 para não criar uma duplicata. (+14 more)

### Community 21 - "test_discord_sender.py"
Cohesion: 0.16
Nodes (16): FakeChannel, FakeDiscordClient, instagram_environment(), asyncio, Testes do envio de embeds Discord sem conexão externa., Um Reel usa título enxuto no conteúdo, sem ser classificado como post., Um ID que não resolve para canal de mensagens não é aceito., Canal que registra mensagens enviadas em memória. (+8 more)

### Community 22 - "test_run_services_composes_single_bot_and_cleans_up_tasks"
Cohesion: 0.09
Nodes (11): FakeBot, FakeServer, FakeStore, asyncio, MonkeyPatch, Testes da composição integrada sem conectar Discord, Twitch ou Uvicorn reais., Store sem I/O para confirmar que a composição cria apenas uma instância., Bot mínimo que permanece ativo até o desligamento coordenado. (+3 more)

### Community 23 - "MemberActivityLogs"
Cohesion: 0.06
Nodes (46): RawBulkMessageDeleteEvent, RawMessageDeleteEvent, RawMessageUpdateEvent, ActivityPublisher, Protocol, Seleciona os eventos de atividade habilitados para publicação., RecordServerActivity, Metadados mínimos de eventos administrativos, sem conteúdo de mensagens. (+38 more)

### Community 24 - "CommandAccessTree"
Cohesion: 0.12
Nodes (21): can_use_command(), Política de acesso aos comandos, independente da representação do Discord., CommandAccessTree, Interaction, Controle global de acesso aos comandos slash por cargo Discord., Impede comandos restritos, preservando exceções públicas explícitas., Valida o cargo antes de qualquer comando registrado na árvore., FakeResponse (+13 more)

### Community 25 - "TwitchClient"
Cohesion: 0.10
Nodes (18): Any, Response, Busca ID, login e nome exibido de um perfil pelo login., Obtém o ID do perfil configurado e o reutiliza apenas em memória., Expõe somente o ID já resolvido, sem I/O na rota do webhook., Busca o título atual da live para enriquecer uma notificação., Obtém inscrições EventSub para detectar duplicidades antes de criar uma nova., Monta o payload EventSub conforme o contrato ``stream.online`` v1. (+10 more)

### Community 26 - "InstagramTokenStore"
Cohesion: 0.12
Nodes (16): InstagramTokenRefreshClient, InstagramTokenStore, InstagramRefreshPolicy, datetime, Renova autorizações com controle de concorrência e janela de tentativas., Informa a última tentativa sem expor informações secretas., Informa o resultado seguro mais recente da renovação., Recarrega, valida a janela e renova o token somente quando necessário. (+8 more)

### Community 27 - "General"
Cohesion: 0.15
Nodes (18): General, command, default_permissions, guild_only, has_permissions, Interaction, User, Retorna de forma privada o ID do usuário informado. (+10 more)

### Community 28 - "NotificationStore"
Cohesion: 0.06
Nodes (34): Connection, NotificationStore, Path, Armazenamento SQLite assíncrono para eventos de notificação., Persiste identificadores processados para evitar notificações duplicadas., Cria as tabelas e índices necessários, caso ainda não existam., Registra um evento EventSub e retorna se ele ainda não havia sido recebido., Atualiza o estado de envio de uma notificação Twitch. (+26 more)

### Community 29 - "generate_deployment_article_pdf.py"
Cohesion: 0.14
Nodes (19): article_sections(), build_article_text(), create_pdf(), https_url(), main(), page_number(), parse_arguments(), Namespace (+11 more)

### Community 30 - "bootstrap.py"
Cohesion: 0.07
Nodes (34): Server, Erro seguro e genérico de uma integração com a Twitch., Indica uma falha segura durante extração de áudio., TwitchError, YouTubeAudioError, _configure_background_tasks(), main(), _prepare_twitch_client() (+26 more)

### Community 31 - "test_instagram_oauth.py"
Cohesion: 0.11
Nodes (19): FakeBot, FakeOAuthService, oauth_environment(), asyncio, Testes do Instagram Login sem chamadas à Meta, Discord ou rede real., Uma autorização de outro perfil não sobrescreve o armazenamento atual., State inválido, replay e erro da Meta não liberam detalhes ao navegador., Um callback válido é aceito uma vez e sua repetição é bloqueada. (+11 more)

### Community 32 - "Configuração"
Cohesion: 0.09
Nodes (22): API FastAPI local, Autorizar a conta, Canais de voz temporários, Cargos automáticos e por reação, Chamar moderador, Comandos Discord, Configuração, Diagnóstico administrativo e registros de atividade (+14 more)

### Community 33 - "RuntimeError"
Cohesion: 0.36
Nodes (8): RuntimeError, parametrize, Casos de uso executados com portas em memória, sem Discord, HTTP ou SQLite., test_instagram_retries_initial_sync_without_announcing_historical_media(), test_twitch_delivery_checks_stream_and_records_result(), test_twitch_event_is_only_queued_when_new(), test_twitch_failed_delivery_is_recorded_and_propagated(), twitch_event()

### Community 34 - "models.py"
Cohesion: 0.10
Nodes (25): Falha ao autenticar a aplicação Twitch., Client ID ou Client Secret foram recusados pela Twitch., Token Twitch inválido, expirado ou com resposta de validação incorreta., TwitchAuthenticationError, TwitchInvalidClientError, TwitchTokenError, datetime, Modelos tipados trocados entre integrações, armazenamento e tarefas. (+17 more)

### Community 35 - "test_call_moderator.py"
Cohesion: 0.10
Nodes (15): FakeDiscordClient, FakeFollowup, FakeInteraction, FakeModerator, FakeResponse, AllowedMentions, Testes do comando público /chamar., Registra respostas iniciais da interação. (+7 more)

### Community 36 - "InstagramMedia"
Cohesion: 0.18
Nodes (12): is_instagram_post(), is_instagram_reel(), Classificação de publicações e validação de links de vídeo., InstagramMedia, Representa uma mídia retornada pela API Graph do Instagram., Bot, Comandos gerais do bot., Registra o cog de comandos gerais na extensão. (+4 more)

### Community 37 - "InstagramSettings"
Cohesion: 0.11
Nodes (17): _prepare_instagram_client(), Cria Instagram e seu armazenamento sem derrubar os serviços Discord se falhar., InstagramSettings, Configurações para a consulta oficial de mídia do Instagram., Indica se as três credenciais necessárias para OAuth foram informadas., Indica se há dados mínimos no ambiente para iniciar polling imediatamente., AsyncClient, create_instagram_token_store() (+9 more)

### Community 38 - "test_youtube_audio.py"
Cohesion: 0.12
Nodes (15): FakeExtractor, asyncio, Exception, Testes sem rede para validação e extração de áudio do YouTube., A extração não bloqueia o loop e retorna URL temporária apenas ao chamador…, Falhas do yt-dlp não vazam detalhes do vídeo nem do stream., Extrator controlado compatível com o context manager do yt-dlp., A URL enviada ao yt-dlp referencia somente o vídeo selecionado. (+7 more)

### Community 39 - "test_web_app_exposes_health_and_initializes_shared_store"
Cohesion: 0.17
Nodes (11): FakeBot, asyncio, Testes da fábrica FastAPI e do seu lifespan sem iniciar Discord real., Representa a única instância compartilhada recebida pela fábrica web., Atende ao contrato da rota sem criar um cliente Discord., Registra a inicialização do armazenamento pelo lifespan da aplicação., A fábrica não instancia Discord e usa o store recebido durante o lifespan., A API de saúde continua disponível sem expor rota Twitch quando ela está… (+3 more)

### Community 40 - "create_web_app"
Cohesion: 0.15
Nodes (11): InstagramOAuthService, Cancela tarefas e fecha clientes auxiliares antes de encerrar o Discord., create_web_app(), lifespan(), FastAPI, Fábrica da aplicação FastAPI usada pelo webhook da Twitch., Cria o servidor HTTP sem instanciar um segundo cliente Discord., create_instagram_oauth_router() (+3 more)

### Community 42 - "test_twitch_auth.py"
Cohesion: 0.20
Nodes (11): asyncio, Testes unitários do OAuth de App Access Token Twitch, sem rede externa., O token recebido inclui vencimento calculado e não depende de variável legada., Falha HTTP 5xx é repetida de forma limitada antes de aceitar a resposta válida., O endpoint OAuth de validação sinaliza token inválido sem expor seu valor., Credenciais recusadas geram erro claro sem revelar o segredo configurado., test_invalid_client_error_does_not_include_client_secret(), test_requests_token_with_expiration_in_memory() (+3 more)

### Community 43 - "generate_deployment_article.py"
Cohesion: 0.22
Nodes (12): build_article(), _https_url(), main(), parse_arguments(), Namespace, Lê os links públicos e o destino sem incluir dados sensíveis., Gera o arquivo e informa uma contagem de palavras verificável., Valida links públicos sem fazer requisições de rede. (+4 more)

### Community 44 - "MediaReactions"
Cohesion: 0.15
Nodes (13): Message, MediaReactions, _message_contains_media(), Bot, Client, listener, Registra uma mensagem uma vez e limita o cache estritamente em memória., Registra o listener sem substituir o on_message do cliente principal. (+5 more)

### Community 45 - "DiscordNotificationSender"
Cohesion: 0.08
Nodes (24): File, DiscordNotificationError, Indica que uma notificação não pôde ser entregue no Discord., Expõe o remetente compartilhado para extensões do bot., DiscordNotificationSender, AllowedMentions, Embed, Member (+16 more)

### Community 46 - "FakeInteractionResponse"
Cohesion: 0.18
Nodes (5): FakeFollowup, FakeInteractionResponse, Embed, Captura a resposta inicial da interação slash., Captura as respostas posteriores ao defer.

### Community 47 - "routes.py"
Cohesion: 0.17
Nodes (15): create_twitch_router(), receive_twitch_webhook(), is_twitch_timestamp_fresh(), _parse_optional_timestamp(), _parse_twitch_online_event(), Any, APIRouter, datetime (+7 more)

### Community 48 - "InstagramOAuthStateStore"
Cohesion: 0.24
Nodes (6): InstagramOAuthStateStore, datetime, Estados OAuth de uso único para os endpoints de autorização., Guarda estados de uso único somente pelo tempo necessário para o callback., Cria um state criptograficamente aleatório e registra sua expiração., Valida e remove o state, impedindo seu reuso.

### Community 49 - "CurrentTwitchLiveRepository"
Cohesion: 0.19
Nodes (6): CurrentTwitchLiveRepository, GetCurrentTwitchLive, Consulta a live configurada e confirma seu estado antes de um reenvio., Obtém a live atual e confirma que ela ainda está online antes do reenvio., Expõe o estado em memória da última live Twitch ainda aberta., Client

### Community 50 - "TwitchTokenValidator"
Cohesion: 0.10
Nodes (16): TwitchTokenClient, Configurações necessárias para o EventSub da Twitch., TwitchSettings, Validação periódica do App Access Token Twitch em memória., Valida e recupera o token Twitch sem interromper o cliente Discord., Inicia no máximo uma tarefa periódica quando a integração está ativa., Cancela e aguarda a tarefa para encerrar o processo sem pendências., Executa uma validação para uso em testes ou disparos controlados. (+8 more)

### Community 51 - "RoleManagement"
Cohesion: 0.17
Nodes (10): Bot, command, has_permissions, Interaction, Publica os menus uma única vez e devolve IDs para o administrador configurar., Processa somente cargos e reações previamente mapeados na configuração., Monta uma mensagem com menções por ID, sem depender de nomes fixos., Registra o cog de cargos no único cliente Discord existente. (+2 more)

### Community 52 - "SecretStore"
Cohesion: 0.25
Nodes (5): Protocol, Contrato mínimo para um serviço gerenciado de segredos., Lê o valor de um segredo pelo identificador configurado., Atualiza o valor de um segredo pelo identificador configurado., SecretStore

### Community 53 - "environment"
Cohesion: 0.33
Nodes (4): fixture, environment(), Fixtures compartilhadas, sem credenciais reais., Fornece o mínimo de configuração válida para os testes.

### Community 54 - "test_architecture.py"
Cohesion: 0.47
Nodes (5): parametrize, Protege as fronteiras para manter regras independentes de frameworks e I/O., test_adapters_do_not_import_each_other_or_the_composition_root(), test_architecture_has_explicit_layers(), test_inner_layers_only_depend_on_standard_library_and_inward_layers()

### Community 55 - "notification_sender.py"
Cohesion: 0.18
Nodes (8): AsyncClient, InstagramNotificationView, Client, Envio seguro de notificações para canais do Discord., View com botão de acesso à live da Twitch., View com botão para abrir a publicação original no Instagram., TwitchNotificationView, ValueError

### Community 56 - "InstagramAuthenticationError"
Cohesion: 0.24
Nodes (9): InstagramAuthenticationError, InstagramTokenExpiredError, Indica que o token já expirou e precisa de nova autorização manual., Indica token inválido, expirado ou revogado., Response, Classifica falhas de autorização sem incluir a resposta nem o token na exceção., _token_authentication_error(), FailingInstagramClient (+1 more)

### Community 58 - "AwsSecretsManagerSecretStore"
Cohesion: 0.25
Nodes (5): AwsSecretsManagerSecretStore, Any, Adaptador assíncrono para AWS Secrets Manager via IAM Role da instância EC2., Lê SecretString sem registrar seu conteúdo ou detalhes da resposta AWS., Persiste SecretString usando as permissões da IAM Role configurada.

### Community 59 - "InstagramPoller"
Cohesion: 0.32
Nodes (4): InstagramPoller, Inicia uma única tarefa de polling quando a integração está ativada., Cancela a tarefa pendente e aguarda seu encerramento., Mantém o polling ativo sem derrubar o bot após uma falha recuperável.

### Community 60 - "FakeTwitchClient"
Cohesion: 0.33
Nodes (4): Falha segura em uma chamada à API Helix ou EventSub., TwitchApiError, FakeTwitchClient, Retorna o estado atual da live sem acessar a API Twitch.

### Community 62 - "Protocol"
Cohesion: 0.17
Nodes (9): InstagramGateway, InstagramMediaClient, InstagramMediaRepository, InstagramNotificationSender, Protocol, PollInstagramMedia, Descobre novas publicações e registra apenas entregas confirmadas., Agenda consultas do Instagram sem incorporar as regras de notificação. (+1 more)

## Knowledge Gaps
- **20 isolated node(s):** `discord-bot`, `Organização do código`, `Requisitos`, `Instalação`, `API FastAPI local` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 840 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `DiscordBot`, `test_role_management.py`, `test_temporary_voice.py`, `diagnose_server`, `test_welcome.py`, `TemporaryVoice`, `test_media_reactions.py`, `test_instagram.py`, `settings.py`, `test_twitch.py`, `test_discord_sender.py`, `test_run_services_composes_single_bot_and_cleans_up_tasks`, `MemberActivityLogs`, `NotificationStore`, `bootstrap.py`, `test_instagram_oauth.py`, `InstagramSettings`, `test_web_app_exposes_health_and_initializes_shared_store`, `create_web_app`, `test_twitch_auth.py`, `MediaReactions`, `DiscordNotificationSender`, `routes.py`, `TwitchTokenValidator`, `RoleManagement`, `notification_sender.py`, `test_discord_bootstrap.py`?**
  _High betweenness centrality (0.241) - this node is a cross-community bridge._
- **Why does `Music` connect `DiscordBot` to `.play_youtube`, `test_music.py`, `bootstrap.py`, `Settings`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `DiscordBot` connect `DiscordBot` to `InstagramMedia`, `Settings`, `create_web_app`, `test_media_reactions.py`, `MediaReactions`, `DiscordNotificationSender`, `CurrentTwitchLiveRepository`, `ports.py`, `RoleManagement`, `bootstrap.py`, `CommandAccessTree`, `test_discord_bootstrap.py`, `Protocol`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 99 inferred relationships involving `Settings` (e.g. with `_configure_background_tasks()` and `main()`) actually correct?**
  _`Settings` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `InstagramMedia` (e.g. with `InstagramMediaClient` and `InstagramMediaRepository`) actually correct?**
  _`InstagramMedia` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `General` (e.g. with `DiscordNotificationError` and `InstagramAPIError`) actually correct?**
  _`General` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `TwitchOnlineEvent` (e.g. with `CurrentTwitchLiveRepository` and `TwitchEventQueue`) actually correct?**
  _`TwitchOnlineEvent` has 15 INFERRED edges - model-reasoned connections that need verification._