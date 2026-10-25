# Graph Report - discord-bot  (2026-10-25)

## Corpus Check
- 104 files · ~434,458 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .example 1)

## Summary
- 1957 nodes · 4341 edges · 93 communities (72 shown, 20 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 556 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6677e72a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DiscordBot
- test_role_management.py
- test_temporary_voice.py
- diagnose_server
- test_welcome.py
- RoleManagement
- Settings
- test_live_commands.py
- TemporaryVoice
- media_cog
- InstagramClient
- InstagramOAuthClient
- .from_environment
- test_cleanup_command.py
- test_music.py
- .play_youtube
- instagram_token_store.py
- test_instagram.py
- MemberGrowthStore
- ports.py
- test_twitch.py
- notification_sender.py
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
- raw_payload
- test_twitch_webhook.py
- test_call_moderator.py
- Music
- InstagramTokenData
- test_youtube_url_validation
- test_web_app_exposes_health_and_initializes_shared_store
- create_web_app
- FakeVoiceClient
- test_retries_transient_token_endpoint_failure
- generate_deployment_article.py
- FakeMessage
- DiscordNotificationSender
- FakeInteractionResponse
- FakeMember
- InstagramOAuthStateStore
- TwitchStream
- test_validator_validates_once_and_stops_cleanly
- .configure_roles
- SecretStore
- environment
- test_architecture.py
- RoleCategorySettings
- InstagramAuthenticationError
- server_growth.py
- general.py
- _parse_twitch_online_event
- InstagramAPIError
- application/__init__.py
- InstagramMedia
- .growth
- use_cases/__init__.py
- config/__init__.py
- domain/__init__.py
- infra/__init__.py
- bot/__init__.py
- integrations/__init__.py
- RoleMenuMessageStore
- FakeResponse
- media/__init__.py
- memory/__init__.py
- persistence/__init__.py
- tasks/__init__.py
- discord-bot
- cogs/__init__.py
- discord/__init__.py
- http/__init__.py
- presentation/__init__.py
- InstagramPoller
- main
- InstagramTokenRefreshResult
- ._run
- http/instagram_oauth.py
- FakeSecretStore
- ._schedule_idle_from_audio_thread
- test_sqlite_connections_are_closed_after_each_operation
- .expires_soon
- FakeAudioService
- test_resend_instagram_post_sends_latest_feed_post

## God Nodes (most connected - your core abstractions)
1. `Settings` - 122 edges
2. `InstagramMedia` - 56 edges
3. `General` - 50 edges
4. `DiscordBot` - 46 edges
5. `TwitchOnlineEvent` - 42 edges
6. `InstagramTokenData` - 42 edges
7. `ConfigurationError` - 39 edges
8. `DiscordNotificationSender` - 35 edges
9. `TwitchClient` - 34 edges
10. `InstagramClient` - 33 edges

## Surprising Connections (you probably didn't know these)
- `test_reports_expired_or_invalid_token_without_exposing_it()` --uses--> `InstagramAuthenticationError`  [INFERRED]
  tests/test_instagram.py → src/bot/application/errors.py
- `test_refresh_reports_expired_token_without_exposing_it()` --uses--> `InstagramTokenExpiredError`  [INFERRED]
  tests/test_instagram.py → src/bot/application/errors.py
- `test_invalid_client_error_does_not_include_client_secret()` --uses--> `TwitchInvalidClientError`  [INFERRED]
  tests/test_twitch_auth.py → src/bot/application/errors.py
- `FakeTwitchClient` --uses--> `TwitchApiError`  [INFERRED]
  tests/test_live_commands.py → src/bot/application/errors.py
- `test_oauth_rejects_an_account_other_than_the_configured_profile()` --uses--> `InstagramOAuthError`  [INFERRED]
  tests/test_instagram_oauth.py → src/bot/application/errors.py

## Import Cycles
- None detected.

## Communities (93 total, 20 thin omitted)

### Community 0 - "DiscordBot"
Cohesion: 0.06
Nodes (28): AppCommandError, AudioSource, BackgroundTask, NotificationRepository, RoleMenuMessageCache, TwitchGateway, Configuração centralizada de logs., DiscordBot (+20 more)

### Community 1 - "test_role_management.py"
Cohesion: 0.15
Nodes (22): asyncio, Testes isolados do sistema de cargos automáticos e por reação., Retorna os menus de idade e pronomes com IDs e emojis Unicode., Cria o cog em memória, sem instanciar outro cliente Discord., O membro novo recebe apenas o cargo inicial configurado., O bot completa as reações dos menus configurados sem depender do cache., Cargo existente e cargo acima do bot não são alterados., Reagir adiciona; reagir novamente remove o mesmo cargo exclusivo. (+14 more)

### Community 2 - "test_temporary_voice.py"
Cohesion: 0.06
Nodes (44): build_voice_fixture(), discord_error(), FakeBot, FakeCategory, FakeGuild, FakeMember, FakePrincipal, FakeRole (+36 more)

### Community 3 - "diagnose_server"
Cohesion: 0.10
Nodes (38): _diagnose_channel(), _diagnose_role(), diagnose_server(), Transforma fatos do servidor em problemas e correções acionáveis., ChannelSnapshot, DiagnosticCheck, DiagnosticReport, Instantâneos e resultados de diagnóstico independentes da API do Discord. (+30 more)

### Community 4 - "test_welcome.py"
Cohesion: 0.07
Nodes (33): discord_error(), FakeInteraction, FakeInteractionResponse, FakeNamedChannel, FakeWelcomeClient, FakeWelcomeUser, asyncio, HTTPException (+25 more)

### Community 5 - "RoleManagement"
Cohesion: 0.11
Nodes (19): RawReactionActionEvent, Bot, Guild, listener, Member, Role, Alterna um cargo mapeado mesmo quando a mensagem não está no cache., Remove o cargo existente ou o adiciona, respeitando exclusividade. (+11 more)

### Community 6 - "Settings"
Cohesion: 0.05
Nodes (62): Configuração tipada e segura para inicializar o bot., Settings, parametrize, Testes unitários da configuração do ambiente., Variáveis removidas não voltam a ativar opções de pronomes., A ausência de token Discord deve interromper a leitura da configuração., Os formatos booleanos aceitos devem ser interpretados corretamente., O controle de repetição Twitch usa os mesmos formatos booleanos aceitos. (+54 more)

### Community 7 - "test_live_commands.py"
Cohesion: 0.11
Nodes (32): FakeInteraction, FakeNotificationSender, FakeTwitchClient, open_live(), asyncio, Testes dos comandos slash de reenvio de live e lista de comandos., Interação mínima para executar callbacks do cog diretamente., Cria dados imutáveis de uma live que está efetivamente online. (+24 more)

### Community 8 - "TemporaryVoice"
Cohesion: 0.07
Nodes (33): Snowflake, Bot, Client, Guild, GuildChannel, listener, Lock, Member (+25 more)

### Community 9 - "media_cog"
Cohesion: 0.08
Nodes (36): Message, MediaReactions, _message_contains_media(), Bot, Client, listener, Registra uma mensagem uma vez e limita o cache estritamente em memória., Registra o listener sem substituir o on_message do cliente principal. (+28 more)

### Community 10 - "InstagramClient"
Cohesion: 0.06
Nodes (38): InstagramPermissionError, InstagramProfileNotFoundError, InstagramRateLimitError, InstagramTokenRefreshError, Indica que a renovação não foi concluída por uma falha recuperável., Indica que o token não tem permissões para a conta configurada., Indica que a conta profissional autorizada não foi encontrada., Indica que a API aplicou limite de requisições. (+30 more)

### Community 11 - "InstagramOAuthClient"
Cohesion: 0.17
Nodes (11): InstagramOAuthError, Erro seguro do fluxo OAuth, apropriado para uma resposta HTTP genérica., InstagramOAuthClient, Any, AsyncClient, datetime, OAuth do Instagram Login para autorizar uma conta profissional sem expor…, Executa Instagram Login, troca o código e salva apenas dados validados. (+3 more)

### Community 12 - ".from_environment"
Cohesion: 0.09
Nodes (49): _activity_events(), _boolean(), ConfigurationError, _https_url(), _instagram_api_version(), _log_level(), _numeric_id(), _optional_https_url() (+41 more)

### Community 13 - "test_cleanup_command.py"
Cohesion: 0.09
Nodes (28): cleanup_cog(), discord_error(), FakeChannel, FakeFollowup, FakeInteraction, FakeNotificationSender, FakeResponse, asyncio (+20 more)

### Community 14 - "test_music.py"
Cohesion: 0.15
Nodes (25): FakeBot, FakeGuild, FakeInteraction, FakeMember, music_cog(), asyncio, MonkeyPatch, Testes sem Discord, FFmpeg ou YouTube reais para os comandos de música. (+17 more)

### Community 15 - ".play_youtube"
Cohesion: 0.16
Nodes (13): Connectable, command, describe, Guild, guild_only, Interaction, Para o áudio mantendo a conexão até o timeout de inatividade., Para e desconecta do canal do solicitante, limpando o estado da guild. (+5 more)

### Community 16 - "instagram_token_store.py"
Cohesion: 0.11
Nodes (22): InstagramTokenStoreError, Falha segura ao ler ou persistir o token Instagram., AwsSecretsManagerInstagramTokenStore, AwsSecretsManagerSecretStore, create_instagram_token_store(), JsonFileInstagramTokenStore, _parse_expires_at(), Any (+14 more)

### Community 17 - "test_instagram.py"
Cohesion: 0.07
Nodes (52): LogCaptureFixture, FailingSender, FakeInstagramClient, FakeRefreshClient, FakeSender, instagram_environment(), instagram_refresh_environment(), asyncio (+44 more)

### Community 18 - "MemberGrowthStore"
Cohesion: 0.08
Nodes (34): date, AnalyzeMemberGrowth, GrowthReader, _metrics(), Consulta o histórico observado e preenche os dias sem movimentação., growth_window(), GrowthData, GrowthMetrics (+26 more)

### Community 19 - "ports.py"
Cohesion: 0.12
Nodes (21): Contratos mínimos usados pelos casos de uso e implementados pelos adaptadores., TwitchEventQueue, TwitchEventRepository, TwitchNotificationSender, NotifyTwitchLive, Recebe eventos e entrega lives confirmadas sem depender de HTTP ou Discord., ReceiveTwitchEvent, Modelos tipados trocados entre integrações, armazenamento e tarefas. (+13 more)

### Community 20 - "test_twitch.py"
Cohesion: 0.14
Nodes (22): oauth_token_response(), asyncio, Response, Testes sem rede para Helix e EventSub com token Twitch renovável., Uma chamada GET recebe um token novo e é repetida uma única vez após HTTP 401., A ausência de dados de stream permite limpar a live atual sem notificar…, Retorna uma resposta OAuth curta e válida para os transportes simulados., EventSub consulta inscrições depois de 401 para não criar uma duplicata. (+14 more)

### Community 21 - "notification_sender.py"
Cohesion: 0.10
Nodes (22): InstagramNotificationView, Client, Envio seguro de notificações para canais do Discord., View com botão de acesso à live da Twitch., View com botão para abrir a publicação original no Instagram., TwitchNotificationView, FakeChannel, FakeDiscordClient (+14 more)

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
Cohesion: 0.05
Nodes (45): Falha ao autenticar a aplicação Twitch., Client ID ou Client Secret foram recusados pela Twitch., Token Twitch inválido, expirado ou com resposta de validação incorreta., Falha segura em uma chamada à API Helix ou EventSub., TwitchApiError, TwitchAuthenticationError, TwitchInvalidClientError, TwitchTokenError (+37 more)

### Community 26 - "InstagramTokenStore"
Cohesion: 0.12
Nodes (16): InstagramTokenRefreshClient, InstagramTokenStore, InstagramRefreshPolicy, datetime, Renova autorizações com controle de concorrência e janela de tentativas., Informa a última tentativa sem expor informações secretas., Informa o resultado seguro mais recente da renovação., Recarrega, valida a janela e renova o token somente quando necessário. (+8 more)

### Community 27 - "General"
Cohesion: 0.15
Nodes (18): General, command, default_permissions, guild_only, has_permissions, Interaction, User, Retorna de forma privada o ID do usuário informado. (+10 more)

### Community 28 - "NotificationStore"
Cohesion: 0.12
Nodes (9): NotificationStore, Connection, Path, Persiste identificadores processados para evitar notificações duplicadas., Cria as tabelas e índices necessários, caso ainda não existam., Registra um evento EventSub e retorna se ele ainda não havia sido recebido., Atualiza o estado de envio de uma notificação Twitch., Informa se uma mídia já foi conhecida ou notificada. (+1 more)

### Community 29 - "generate_deployment_article_pdf.py"
Cohesion: 0.14
Nodes (19): article_sections(), build_article_text(), create_pdf(), https_url(), main(), page_number(), parse_arguments(), Namespace (+11 more)

### Community 30 - "bootstrap.py"
Cohesion: 0.04
Nodes (56): RuntimeError, Server, GrowthStorageError, Falhas seguras que os casos de uso podem tratar sem conhecer os adaptadores., Erro seguro e genérico de uma integração com a Twitch., Indica uma falha segura durante extração de áudio., Falha segura ao registrar ou consultar movimentações do servidor., Falha segura ao ler ou persistir os IDs das mensagens de cargos. (+48 more)

### Community 31 - "test_instagram_oauth.py"
Cohesion: 0.11
Nodes (19): FakeBot, FakeOAuthService, oauth_environment(), asyncio, Testes do Instagram Login sem chamadas à Meta, Discord ou rede real., Uma autorização de outro perfil não sobrescreve o armazenamento atual., State inválido, replay e erro da Meta não liberam detalhes ao navegador., Um callback válido é aceito uma vez e sua repetição é bloqueada. (+11 more)

### Community 32 - "Configuração"
Cohesion: 0.08
Nodes (23): API FastAPI local, Autorizar a conta, Canais de voz temporários, Cargos automáticos e por reação, Chamar moderador, Comandos Discord, Configuração, Crescimento, entradas e saídas por período (+15 more)

### Community 33 - "raw_payload"
Cohesion: 0.12
Nodes (16): discord_error(), payload(), HTTPException, MonkeyPatch, Path, SimpleNamespace, Cria um payload raw compatível com os atributos usados pelo cog., Emoji Unicode que implementa a conversão usada pelo payload real. (+8 more)

### Community 34 - "test_twitch_webhook.py"
Cohesion: 0.19
Nodes (17): FakeBot, post_webhook(), asyncio, FastAPI, Path, Response, Testes isolados do webhook EventSub, sem chamadas externas., Mensagens antigas são recusadas antes de qualquer processamento. (+9 more)

### Community 35 - "test_call_moderator.py"
Cohesion: 0.10
Nodes (15): FakeDiscordClient, FakeFollowup, FakeInteraction, FakeModerator, FakeResponse, AllowedMentions, Testes do comando público /chamar., Registra respostas iniciais da interação. (+7 more)

### Community 36 - "Music"
Cohesion: 0.10
Nodes (17): Music, Bot, GuildChannel, listener, Lock, Member, VoiceState, Sai de uma sala sem humanos para não impedir a limpeza de salas temporárias. (+9 more)

### Community 37 - "InstagramTokenData"
Cohesion: 0.13
Nodes (9): InstagramTokenData, Token Instagram e metadados mantidos em um armazenamento configurado., Retorna o token em memória para testes unitários isolados., Substitui o token em memória depois de validá-lo., Lê o JSON persistido; usa o ambiente apenas quando ainda não há arquivo., FakeTokenStore, MemoryTokenStore, Armazena apenas dados de teste para verificar a persistência do callback. (+1 more)

### Community 38 - "test_youtube_url_validation"
Cohesion: 0.67
Nodes (3): parametrize, Somente links públicos que apontem para um vídeo YouTube são aceitos., test_youtube_url_validation()

### Community 39 - "test_web_app_exposes_health_and_initializes_shared_store"
Cohesion: 0.17
Nodes (11): FakeBot, asyncio, Testes da fábrica FastAPI e do seu lifespan sem iniciar Discord real., Representa a única instância compartilhada recebida pela fábrica web., Atende ao contrato da rota sem criar um cliente Discord., Registra a inicialização do armazenamento pelo lifespan da aplicação., A fábrica não instancia Discord e usa o store recebido durante o lifespan., A API de saúde continua disponível sem expor rota Twitch quando ela está… (+3 more)

### Community 40 - "create_web_app"
Cohesion: 0.15
Nodes (12): Cancela tarefas e fecha clientes auxiliares antes de encerrar o Discord., create_web_app(), lifespan(), FastAPI, Fábrica da aplicação FastAPI usada pelo webhook da Twitch., Cria o servidor HTTP sem instanciar um segundo cliente Discord., create_instagram_oauth_router(), APIRouter (+4 more)

### Community 41 - "FakeVoiceClient"
Cohesion: 0.12
Nodes (9): FakeVoiceChannel, FailingVoiceChannel, FakeVoiceChannel, FakeVoiceClient, MissingPyNaClChannel, Cliente de voz controlável que não reproduz áudio real., Canal de voz com conexão local controlada., Canal que simula a ausência da dependência de voz no host. (+1 more)

### Community 42 - "test_retries_transient_token_endpoint_failure"
Cohesion: 0.20
Nodes (10): asyncio, O token recebido inclui vencimento calculado e não depende de variável legada., Falha HTTP 5xx é repetida de forma limitada antes de aceitar a resposta válida., O endpoint OAuth de validação sinaliza token inválido sem expor seu valor., Credenciais recusadas geram erro claro sem revelar o segredo configurado., test_invalid_client_error_does_not_include_client_secret(), test_requests_token_with_expiration_in_memory(), handler() (+2 more)

### Community 43 - "generate_deployment_article.py"
Cohesion: 0.22
Nodes (12): build_article(), _https_url(), main(), parse_arguments(), Namespace, Lê os links públicos e o destino sem incluir dados sensíveis., Gera o arquivo e informa uma contagem de palavras verificável., Valida links públicos sem fazer requisições de rede. (+4 more)

### Community 44 - "FakeMessage"
Cohesion: 0.12
Nodes (8): FakeBot, FakeChannel, FakeMessage, PublishingChannel, Canal buscável mesmo fora do cache do cliente., Canal que cria mensagens distintas para testar a publicação dos menus., Cliente mínimo, sem conexão real ao Discord., Mensagem que registra remoções individuais de reação.

### Community 45 - "DiscordNotificationSender"
Cohesion: 0.08
Nodes (24): File, DiscordNotificationError, Indica que uma notificação não pôde ser entregue no Discord., Expõe o remetente compartilhado para extensões do bot., DiscordNotificationSender, AllowedMentions, Embed, Member (+16 more)

### Community 46 - "FakeInteractionResponse"
Cohesion: 0.18
Nodes (5): FakeFollowup, FakeInteractionResponse, Embed, Captura a resposta inicial da interação slash., Captura as respostas posteriores ao defer.

### Community 47 - "FakeMember"
Cohesion: 0.15
Nodes (10): FakeGuild, FakeMember, FakeRole, FakeGuild, parametrize, Novos menus funcionam imediatamente e após recriar o bot, sem editar o .env., Cargo mínimo com ordenação de hierarquia do Discord., Membro controlado que registra alterações de cargos. (+2 more)

### Community 48 - "InstagramOAuthStateStore"
Cohesion: 0.24
Nodes (6): InstagramOAuthStateStore, datetime, Estados OAuth de uso único para os endpoints de autorização., Guarda estados de uso único somente pelo tempo necessário para o callback., Cria um state criptograficamente aleatório e registra sua expiração., Valida e remove o state, impedindo seu reuso.

### Community 49 - "TwitchStream"
Cohesion: 0.10
Nodes (17): CurrentTwitchLiveRepository, TwitchStreamClient, GetCurrentTwitchLive, Consulta a live configurada e confirma seu estado antes de um reenvio., Obtém a live atual e confirma que ela ainda está online antes do reenvio., CurrentTwitchLive, Dados de uma live consultada após a notificação EventSub., Combina o evento EventSub e os dados mais recentes de uma live aberta. (+9 more)

### Community 50 - "test_validator_validates_once_and_stops_cleanly"
Cohesion: 0.28
Nodes (6): FakeTwitchClient, asyncio, Testes do ciclo de vida do validador periódico de token Twitch., Cliente mínimo que registra validações sem chamadas HTTP., A tarefa pode ser iniciada uma vez e cancelada sem deixar trabalho pendente., test_validator_validates_once_and_stops_cleanly()

### Community 51 - ".configure_roles"
Cohesion: 0.29
Nodes (5): command, has_permissions, Interaction, Publica e ativa os menus imediatamente, persistindo seus IDs no cache., Monta uma mensagem com menções por ID, sem depender de nomes fixos.

### Community 52 - "SecretStore"
Cohesion: 0.25
Nodes (5): Protocol, Contrato mínimo para um serviço gerenciado de segredos., Lê o valor de um segredo pelo identificador configurado., Atualiza o valor de um segredo pelo identificador configurado., SecretStore

### Community 53 - "environment"
Cohesion: 0.33
Nodes (4): fixture, environment(), Fixtures compartilhadas, sem credenciais reais., Fornece o mínimo de configuração válida para os testes.

### Community 54 - "test_architecture.py"
Cohesion: 0.47
Nodes (5): parametrize, Protege as fronteiras para manter regras independentes de frameworks e I/O., test_adapters_do_not_import_each_other_or_the_composition_root(), test_architecture_has_explicit_layers(), test_inner_layers_only_depend_on_standard_library_and_inward_layers()

### Community 55 - "RoleCategorySettings"
Cohesion: 0.14
Nodes (10): Mapeamentos e regras de associação de cargos por reação., Retorna chaves compatíveis com emojis Unicode e personalizados., Configuração de uma mensagem de cargos por reação., Localiza somente um cargo explicitamente autorizado para o emoji., Configuração opcional dos cargos automáticos e menus por reação., Indica se há ao menos uma mensagem de reação configurada., Vínculo seguro entre um emoji configurado e um cargo do Discord., RoleCategorySettings (+2 more)

### Community 56 - "InstagramAuthenticationError"
Cohesion: 0.21
Nodes (11): InstagramAuthenticationError, InstagramTokenExpiredError, InstagramTokenRevokedError, Indica que o token já expirou e precisa de nova autorização manual., Indica que o token foi revogado ou perdeu a autorização., Indica token inválido, expirado ou revogado., Response, Classifica falhas de autorização sem incluir a resposta nem o token na exceção. (+3 more)

### Community 57 - "server_growth.py"
Cohesion: 0.13
Nodes (25): RawMemberRemoveEvent, GrowthRepository, datetime, Protocol, MembershipEvent, Bot, datetime, Guild (+17 more)

### Community 58 - "general.py"
Cohesion: 0.19
Nodes (10): is_instagram_post(), is_instagram_reel(), is_valid_youtube_url(), Classificação de publicações e validação de links de vídeo., Aceita links públicos que apontem para um vídeo específico do YouTube., Bot, Comandos gerais do bot., Registra o cog de comandos gerais na extensão. (+2 more)

### Community 59 - "_parse_twitch_online_event"
Cohesion: 0.17
Nodes (13): receive_twitch_webhook(), is_twitch_timestamp_fresh(), _parse_optional_timestamp(), _parse_twitch_online_event(), Any, datetime, Converte um payload EventSub mínimo, tolerando campos opcionais., Converte timestamps opcionais sem rejeitar um evento válido por esse campo. (+5 more)

### Community 60 - "InstagramAPIError"
Cohesion: 0.24
Nodes (10): InstagramAPIError, Erro seguro para falhas na API oficial do Instagram., FakeInstagramClient, latest_instagram_media(), Cria a publicação usada nos testes do reenvio Instagram., O reenvio manual usa o remetente existente e o Reel mais recente da API., Falhas técnicas não são reveladas ao administrador., Retorna uma mídia controlada sem chamar a API Instagram. (+2 more)

### Community 62 - "InstagramMedia"
Cohesion: 0.13
Nodes (12): InstagramGateway, InstagramMediaClient, InstagramMediaRepository, InstagramNotificationSender, Protocol, TwitchTokenClient, PollInstagramMedia, Descobre novas publicações e registra apenas entregas confirmadas. (+4 more)

### Community 63 - ".growth"
Cohesion: 0.16
Nodes (17): choices, DailyMovement, GrowthReport, command, default_permissions, describe, guild_only, has_permissions (+9 more)

### Community 70 - "RoleMenuMessageStore"
Cohesion: 0.18
Nodes (5): Path, Consulta IDs sem I/O durante as reações e grava cada atualização por canal., Restaura os IDs gravados sem alterar as configurações do ambiente., Ativa o ID imediatamente, mesmo se a persistência ficar indisponível., RoleMenuMessageStore

### Community 71 - "FakeResponse"
Cohesion: 0.20
Nodes (4): FakeFollowup, FakeResponse, Registra respostas iniciais de uma interaction., Registra mensagens posteriores ao defer.

### Community 82 - "InstagramPoller"
Cohesion: 0.32
Nodes (4): InstagramPoller, Inicia uma única tarefa de polling quando a integração está ativada., Cancela a tarefa pendente e aguarda seu encerramento., Mantém o polling ativo sem derrubar o bot após uma falha recuperável.

### Community 83 - "main"
Cohesion: 0.33
Nodes (5): main(), Carrega o ambiente, valida a configuração e inicia os serviços., configure_logging(), Configura logs para o terminal sem registrar dados sensíveis., Permite iniciar o projeto com ``python -m bot``.

### Community 84 - "InstagramTokenRefreshResult"
Cohesion: 0.33
Nodes (4): InstagramTokenRefreshResult, Resultado seguro de uma renovação bem-sucedida de token Instagram., Usa o mesmo cliente HTTP para renovar um token ainda válido., Exception

### Community 85 - "._run"
Cohesion: 0.33
Nodes (3): Inicia no máximo uma tarefa periódica quando a integração está ativa., Executa uma validação para uso em testes ou disparos controlados., Mantém a validação independente e recuperável enquanto o bot estiver aberto.

### Community 88 - "._schedule_idle_from_audio_thread"
Cohesion: 0.50
Nodes (3): AbstractEventLoop, Exception, Agenda a desconexão no loop correto após callback síncrono do player.

### Community 89 - "test_sqlite_connections_are_closed_after_each_operation"
Cohesion: 0.50
Nodes (4): MonkeyPatch, Path, test_sqlite_connections_are_closed_after_each_operation(), close()

### Community 92 - "test_resend_instagram_post_sends_latest_feed_post"
Cohesion: 0.50
Nodes (4): latest_instagram_post(), Cria o post de feed usado nos testes do reenvio Instagram., O comando de post ignora Reels e reenvia apenas uma mídia de feed., test_resend_instagram_post_sends_latest_feed_post()

## Knowledge Gaps
- **21 isolated node(s):** `discord-bot`, `Organização do código`, `Requisitos`, `Instalação`, `API FastAPI local` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 887 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `DiscordBot`, `test_role_management.py`, `diagnose_server`, `test_welcome.py`, `RoleManagement`, `TemporaryVoice`, `media_cog`, `.from_environment`, `test_instagram.py`, `ports.py`, `test_twitch.py`, `notification_sender.py`, `test_run_services_composes_single_bot_and_cleans_up_tasks`, `MemberActivityLogs`, `bootstrap.py`, `test_instagram_oauth.py`, `test_twitch_webhook.py`, `Music`, `test_web_app_exposes_health_and_initializes_shared_store`, `create_web_app`, `test_retries_transient_token_endpoint_failure`, `DiscordNotificationSender`, `test_validator_validates_once_and_stops_cleanly`, `RoleCategorySettings`, `main`?**
  _High betweenness centrality (0.262) - this node is a cross-community bridge._
- **Why does `DiscordBot` connect `DiscordBot` to `Music`, `RoleManagement`, `Settings`, `create_web_app`, `media_cog`, `TemporaryVoice`, `.from_environment`, `DiscordNotificationSender`, `TwitchStream`, `ports.py`, `bootstrap.py`, `CommandAccessTree`, `server_growth.py`, `general.py`, `InstagramMedia`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `General` connect `General` to `test_call_moderator.py`, `test_welcome.py`, `test_live_commands.py`, `DiscordNotificationSender`, `test_cleanup_command.py`, `test_resend_instagram_post_sends_latest_feed_post`, `TwitchStream`, `InstagramMedia`, `general.py`, `InstagramAPIError`, `bootstrap.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 99 inferred relationships involving `Settings` (e.g. with `_configure_background_tasks()` and `main()`) actually correct?**
  _`Settings` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `InstagramMedia` (e.g. with `InstagramMediaClient` and `InstagramMediaRepository`) actually correct?**
  _`InstagramMedia` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `General` (e.g. with `DiscordNotificationError` and `InstagramAPIError`) actually correct?**
  _`General` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `DiscordBot` (e.g. with `_configure_background_tasks()` and `AudioSource`) actually correct?**
  _`DiscordBot` has 24 INFERRED edges - model-reasoned connections that need verification._