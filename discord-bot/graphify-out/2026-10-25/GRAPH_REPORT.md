# Graph Report - discord-bot  (2026-10-24)

## Corpus Check
- 103 files · ~433,404 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .example 1)

## Summary
- 1924 nodes · 4251 edges · 92 communities (71 shown, 20 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 546 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b698f603`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Settings
- test_role_management.py
- test_temporary_voice.py
- diagnose_server
- test_welcome.py
- .on_raw_reaction_add
- .from_environment
- TwitchStream
- TemporaryVoice
- test_media_reactions.py
- application/errors.py
- InstagramOAuthClient
- DiscordNotificationError
- test_cleanup_command.py
- test_music.py
- .play_youtube
- InstagramTokenData
- test_instagram.py
- GrowthQuery
- TwitchOnlineEvent
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
- models.py
- TwitchAuthClient
- test_call_moderator.py
- Music
- InstagramSettings
- test_youtube_audio.py
- test_web_app_exposes_health_and_initializes_shared_store
- ports.py
- FakeVoiceClient
- test_twitch_auth.py
- generate_deployment_article.py
- MediaReactions
- .send_welcome_message
- FakeInteractionResponse
- MemberGrowthStore
- InstagramOAuthStateStore
- general.py
- test_validator_validates_once_and_stops_cleanly
- .configure_roles
- SecretStore
- environment
- test_architecture.py
- ValueError
- InstagramMedia
- ServerGrowth
- use_cases/member_growth.py
- test_reports_expired_or_invalid_token_without_exposing_it
- .send_instagram_notification
- application/__init__.py
- InstagramPoller
- growth_report.py
- use_cases/__init__.py
- config/__init__.py
- domain/__init__.py
- infra/__init__.py
- bot/__init__.py
- integrations/__init__.py
- MembershipEvent
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
- .growth
- TwitchSettings
- InstagramTokenRefreshResult
- FakeInteractionResponse
- test_boolean_values_are_converted
- FakeSecretStore
- ._schedule_idle_from_audio_thread
- .__init__
- .expires_soon
- FakeAudioService

## God Nodes (most connected - your core abstractions)
1. `Settings` - 122 edges
2. `InstagramMedia` - 56 edges
3. `General` - 50 edges
4. `DiscordBot` - 45 edges
5. `TwitchOnlineEvent` - 42 edges
6. `InstagramTokenData` - 42 edges
7. `ConfigurationError` - 39 edges
8. `DiscordNotificationSender` - 35 edges
9. `TwitchClient` - 34 edges
10. `InstagramClient` - 33 edges

## Surprising Connections (you probably didn't know these)
- `FakeInstagramClient` --uses--> `InstagramAPIError`  [INFERRED]
  tests/test_live_commands.py → src/bot/application/errors.py
- `FailingInstagramClient` --uses--> `InstagramAuthenticationError`  [INFERRED]
  tests/test_instagram.py → src/bot/application/errors.py
- `test_reports_expired_or_invalid_token_without_exposing_it()` --uses--> `InstagramAuthenticationError`  [INFERRED]
  tests/test_instagram.py → src/bot/application/errors.py
- `test_refresh_reports_expired_token_without_exposing_it()` --uses--> `InstagramTokenExpiredError`  [INFERRED]
  tests/test_instagram.py → src/bot/application/errors.py
- `test_invalid_client_error_does_not_include_client_secret()` --uses--> `TwitchInvalidClientError`  [INFERRED]
  tests/test_twitch_auth.py → src/bot/application/errors.py

## Import Cycles
- None detected.

## Communities (92 total, 20 thin omitted)

### Community 0 - "Settings"
Cohesion: 0.07
Nodes (32): Configuração centralizada de logs., Configuração tipada e segura para inicializar o bot., Settings, Mapeamentos e regras de associação de cargos por reação., Configuração de uma mensagem de cargos por reação., Localiza somente um cargo explicitamente autorizado para o emoji., Configuração opcional dos cargos automáticos e menus por reação., Indica se há ao menos uma mensagem de reação configurada. (+24 more)

### Community 1 - "test_role_management.py"
Cohesion: 0.06
Nodes (45): discord_error(), FakeBot, FakeChannel, FakeGuild, FakeMember, FakeMessage, FakeRole, payload() (+37 more)

### Community 2 - "test_temporary_voice.py"
Cohesion: 0.06
Nodes (46): build_voice_fixture(), discord_error(), FakeBot, FakeCategory, FakeGuild, FakeMember, FakePrincipal, FakeRole (+38 more)

### Community 3 - "diagnose_server"
Cohesion: 0.10
Nodes (38): _diagnose_channel(), _diagnose_role(), diagnose_server(), Transforma fatos do servidor em problemas e correções acionáveis., ChannelSnapshot, DiagnosticCheck, DiagnosticReport, Instantâneos e resultados de diagnóstico independentes da API do Discord. (+30 more)

### Community 4 - "test_welcome.py"
Cohesion: 0.09
Nodes (31): discord_error(), FakeInteraction, FakeNamedChannel, FakeWelcomeClient, FakeWelcomeUser, asyncio, HTTPException, Testes da mensagem privada de boas-vindas, sem conexão com o Discord. (+23 more)

### Community 5 - ".on_raw_reaction_add"
Cohesion: 0.12
Nodes (14): RawReactionActionEvent, Guild, listener, Member, Role, Remove o cargo existente ou o adiciona, respeitando exclusividade., Resolve um membro do cache e usa API somente quando necessário., Remove somente a reação do usuário depois de uma alteração bem-sucedida. (+6 more)

### Community 6 - ".from_environment"
Cohesion: 0.04
Nodes (101): _activity_events(), _boolean(), ConfigurationError, _https_url(), _instagram_api_version(), _log_level(), _numeric_id(), _optional_https_url() (+93 more)

### Community 7 - "TwitchStream"
Cohesion: 0.07
Nodes (50): Dados de uma live consultada após a notificação EventSub., TwitchStream, CurrentTwitchLiveStore, Estado em memória da última live Twitch confirmada como aberta., Mantém uma única live atual com leituras e alterações consistentes. O conteúdo…, Atualiza dados da live sem sobrescrever uma live que chegou depois. Retorna…, FakeInstagramClient, FakeInteraction (+42 more)

### Community 8 - "TemporaryVoice"
Cohesion: 0.07
Nodes (33): Snowflake, Bot, Client, Guild, GuildChannel, listener, Lock, Member (+25 more)

### Community 9 - "test_media_reactions.py"
Cohesion: 0.12
Nodes (28): discord_error(), FakeAttachment, FakeMessage, media_cog(), media_reaction_settings(), asyncio, HTTPException, parametrize (+20 more)

### Community 10 - "application/errors.py"
Cohesion: 0.08
Nodes (41): InstagramAPIError, InstagramAuthenticationError, InstagramPermissionError, InstagramProfileNotFoundError, InstagramRateLimitError, InstagramTokenExpiredError, InstagramTokenRefreshError, InstagramTokenRevokedError (+33 more)

### Community 11 - "InstagramOAuthClient"
Cohesion: 0.17
Nodes (11): InstagramOAuthError, Erro seguro do fluxo OAuth, apropriado para uma resposta HTTP genérica., InstagramOAuthClient, Any, AsyncClient, datetime, OAuth do Instagram Login para autorizar uma conta profissional sem expor…, Executa Instagram Login, troca o código e salva apenas dados validados. (+3 more)

### Community 12 - "DiscordNotificationError"
Cohesion: 0.33
Nodes (3): DiscordNotificationError, Indica que uma notificação não pôde ser entregue no Discord., Envia uma notificação formatada para uma live iniciada.

### Community 13 - "test_cleanup_command.py"
Cohesion: 0.07
Nodes (35): AppCommandError, handle_app_command_error(), Interaction, Tratamento de erros de comandos de aplicativo., Registra um erro técnico e envia uma mensagem segura ao usuário., Envia uma resposta efêmera, inclusive após uma resposta já iniciada., _send_error_message(), cleanup_cog() (+27 more)

### Community 14 - "test_music.py"
Cohesion: 0.15
Nodes (25): FakeBot, FakeGuild, FakeInteraction, FakeMember, music_cog(), asyncio, MonkeyPatch, Testes sem Discord, FFmpeg ou YouTube reais para os comandos de música. (+17 more)

### Community 15 - ".play_youtube"
Cohesion: 0.16
Nodes (13): Connectable, command, describe, Guild, guild_only, Interaction, Para o áudio mantendo a conexão até o timeout de inatividade., Para e desconecta do canal do solicitante, limpando o estado da guild. (+5 more)

### Community 16 - "InstagramTokenData"
Cohesion: 0.09
Nodes (30): InstagramTokenStoreError, Falha segura ao ler ou persistir o token Instagram., _prepare_instagram_client(), Cria Instagram e seu armazenamento sem derrubar os serviços Discord se falhar., InstagramTokenData, Token Instagram e metadados mantidos em um armazenamento configurado., AwsSecretsManagerInstagramTokenStore, AwsSecretsManagerSecretStore (+22 more)

### Community 17 - "test_instagram.py"
Cohesion: 0.15
Nodes (25): FakeRefreshClient, FakeTokenStore, instagram_refresh_environment(), asyncio, datetime, Testes sem rede para cliente e polling da API oficial do Instagram., Armazena o token em memória para testar a tarefa sem persistência externa., Registra chamadas de renovação e devolve um resultado controlado. (+17 more)

### Community 18 - "GrowthQuery"
Cohesion: 0.17
Nodes (22): date, AnalyzeMemberGrowth, growth_window(), GrowthQuery, GrowthWindow, _parse_date(), datetime, Períodos e resultados de movimentação de membros, sem estimar histórico ausente. (+14 more)

### Community 19 - "TwitchOnlineEvent"
Cohesion: 0.10
Nodes (26): Protocol, TwitchEventQueue, TwitchEventRepository, TwitchNotificationSender, NotifyTwitchLive, Recebe eventos e entrega lives confirmadas sem depender de HTTP ou Discord., ReceiveTwitchEvent, Evento ``stream.online`` recebido pelo webhook EventSub. (+18 more)

### Community 20 - "test_twitch.py"
Cohesion: 0.14
Nodes (22): oauth_token_response(), asyncio, Response, Testes sem rede para Helix e EventSub com token Twitch renovável., Uma chamada GET recebe um token novo e é repetida uma única vez após HTTP 401., A ausência de dados de stream permite limpar a live atual sem notificar…, Retorna uma resposta OAuth curta e válida para os transportes simulados., EventSub consulta inscrições depois de 401 para não criar uma duplicata. (+14 more)

### Community 21 - "test_discord_sender.py"
Cohesion: 0.14
Nodes (18): InstagramNotificationView, View com botão para abrir a publicação original no Instagram., FakeChannel, FakeDiscordClient, instagram_environment(), asyncio, Testes do envio de embeds Discord sem conexão externa., Um Reel usa título enxuto no conteúdo, sem ser classificado como post. (+10 more)

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
Nodes (20): Falha segura em uma chamada à API Helix ou EventSub., TwitchApiError, Any, Response, Busca ID, login e nome exibido de um perfil pelo login., Obtém o ID do perfil configurado e o reutiliza apenas em memória., Expõe somente o ID já resolvido, sem I/O na rota do webhook., Busca o título atual da live para enriquecer uma notificação. (+12 more)

### Community 26 - "InstagramTokenStore"
Cohesion: 0.11
Nodes (16): InstagramTokenRefreshClient, InstagramTokenStore, InstagramRefreshPolicy, datetime, Renova autorizações com controle de concorrência e janela de tentativas., Informa a última tentativa sem expor informações secretas., Informa o resultado seguro mais recente da renovação., Recarrega, valida a janela e renova o token somente quando necessário. (+8 more)

### Community 27 - "General"
Cohesion: 0.15
Nodes (18): General, command, default_permissions, guild_only, has_permissions, Interaction, User, Retorna de forma privada o ID do usuário informado. (+10 more)

### Community 28 - "NotificationStore"
Cohesion: 0.06
Nodes (34): NotificationStore, Connection, Path, Armazenamento SQLite assíncrono para eventos de notificação., Persiste identificadores processados para evitar notificações duplicadas., Cria as tabelas e índices necessários, caso ainda não existam., Registra um evento EventSub e retorna se ele ainda não havia sido recebido., Atualiza o estado de envio de uma notificação Twitch. (+26 more)

### Community 29 - "generate_deployment_article_pdf.py"
Cohesion: 0.14
Nodes (19): article_sections(), build_article_text(), create_pdf(), https_url(), main(), page_number(), parse_arguments(), Namespace (+11 more)

### Community 30 - "bootstrap.py"
Cohesion: 0.05
Nodes (37): Server, Indica uma falha segura durante extração de áudio., YouTubeAudioError, BackgroundTask, _configure_background_tasks(), main(), _prepare_twitch_client(), Ponto de entrada que supervisiona o bot Discord e o servidor FastAPI. (+29 more)

### Community 31 - "test_instagram_oauth.py"
Cohesion: 0.09
Nodes (21): FakeBot, FakeOAuthService, MemoryTokenStore, oauth_environment(), asyncio, Testes do Instagram Login sem chamadas à Meta, Discord ou rede real., Uma autorização de outro perfil não sobrescreve o armazenamento atual., State inválido, replay e erro da Meta não liberam detalhes ao navegador. (+13 more)

### Community 32 - "Configuração"
Cohesion: 0.08
Nodes (23): API FastAPI local, Autorizar a conta, Canais de voz temporários, Cargos automáticos e por reação, Chamar moderador, Comandos Discord, Configuração, Crescimento, entradas e saídas por período (+15 more)

### Community 33 - "models.py"
Cohesion: 0.27
Nodes (9): RuntimeError, Modelos tipados trocados entre integrações, armazenamento e tarefas., parametrize, Casos de uso executados com portas em memória, sem Discord, HTTP ou SQLite., test_instagram_retries_initial_sync_without_announcing_historical_media(), test_twitch_delivery_checks_stream_and_records_result(), test_twitch_event_is_only_queued_when_new(), test_twitch_failed_delivery_is_recorded_and_propagated() (+1 more)

### Community 34 - "TwitchAuthClient"
Cohesion: 0.14
Nodes (20): Falha ao autenticar a aplicação Twitch., Client ID ou Client Secret foram recusados pela Twitch., Token Twitch inválido, expirado ou com resposta de validação incorreta., TwitchAuthenticationError, TwitchInvalidClientError, TwitchTokenError, App Access Token Twitch mantido exclusivamente na memória do processo., TwitchToken (+12 more)

### Community 35 - "test_call_moderator.py"
Cohesion: 0.10
Nodes (15): FakeDiscordClient, FakeFollowup, FakeInteraction, FakeModerator, FakeResponse, AllowedMentions, Testes do comando público /chamar., Registra respostas iniciais da interação. (+7 more)

### Community 36 - "Music"
Cohesion: 0.10
Nodes (17): Music, Bot, GuildChannel, listener, Lock, Member, VoiceState, Sai de uma sala sem humanos para não impedir a limpeza de salas temporárias. (+9 more)

### Community 37 - "InstagramSettings"
Cohesion: 0.18
Nodes (8): InstagramSettings, Configurações para a consulta oficial de mídia do Instagram., Indica se as três credenciais necessárias para OAuth foram informadas., Indica se há dados mínimos no ambiente para iniciar polling imediatamente., AsyncClient, InMemoryInstagramTokenStore, Armazenamento efêmero usado somente em testes isolados., Retorna o token em memória para testes unitários isolados.

### Community 38 - "test_youtube_audio.py"
Cohesion: 0.09
Nodes (20): is_valid_youtube_url(), Aceita links públicos que apontem para um vídeo específico do YouTube., FakeExtractor, asyncio, Exception, parametrize, Testes sem rede para validação e extração de áudio do YouTube., A extração não bloqueia o loop e retorna URL temporária apenas ao chamador… (+12 more)

### Community 39 - "test_web_app_exposes_health_and_initializes_shared_store"
Cohesion: 0.17
Nodes (11): FakeBot, asyncio, Testes da fábrica FastAPI e do seu lifespan sem iniciar Discord real., Representa a única instância compartilhada recebida pela fábrica web., Atende ao contrato da rota sem criar um cliente Discord., Registra a inicialização do armazenamento pelo lifespan da aplicação., A fábrica não instancia Discord e usa o store recebido durante o lifespan., A API de saúde continua disponível sem expor rota Twitch quando ela está… (+3 more)

### Community 40 - "ports.py"
Cohesion: 0.08
Nodes (20): AudioSource, InstagramGateway, InstagramOAuthService, NotificationRepository, Contratos mínimos usados pelos casos de uso e implementados pelos adaptadores., TwitchGateway, TwitchTokenClient, Metadados públicos e URL temporária usada somente pelo FFmpeg. (+12 more)

### Community 41 - "FakeVoiceClient"
Cohesion: 0.12
Nodes (9): FakeVoiceChannel, FailingVoiceChannel, FakeVoiceChannel, FakeVoiceClient, MissingPyNaClChannel, Cliente de voz controlável que não reproduz áudio real., Canal de voz com conexão local controlada., Canal que simula a ausência da dependência de voz no host. (+1 more)

### Community 42 - "test_twitch_auth.py"
Cohesion: 0.20
Nodes (11): asyncio, Testes unitários do OAuth de App Access Token Twitch, sem rede externa., O token recebido inclui vencimento calculado e não depende de variável legada., Falha HTTP 5xx é repetida de forma limitada antes de aceitar a resposta válida., O endpoint OAuth de validação sinaliza token inválido sem expor seu valor., Credenciais recusadas geram erro claro sem revelar o segredo configurado., test_invalid_client_error_does_not_include_client_secret(), test_requests_token_with_expiration_in_memory() (+3 more)

### Community 43 - "generate_deployment_article.py"
Cohesion: 0.22
Nodes (12): build_article(), _https_url(), main(), parse_arguments(), Namespace, Lê os links públicos e o destino sem incluir dados sensíveis., Gera o arquivo e informa uma contagem de palavras verificável., Valida links públicos sem fazer requisições de rede. (+4 more)

### Community 44 - "MediaReactions"
Cohesion: 0.15
Nodes (13): Message, MediaReactions, _message_contains_media(), Bot, Client, listener, Registra uma mensagem uma vez e limita o cache estritamente em memória., Registra o listener sem substituir o on_message do cliente principal. (+5 more)

### Community 45 - ".send_welcome_message"
Cohesion: 0.16
Nodes (9): Member, Path, User, Escolhe uma imagem aleatória para a notificação da Twitch., Escolhe uma imagem aleatória para a mensagem de boas-vindas., Envia por DM uma apresentação do Morcegão para o usuário., Obtém o nome atual de um canal ou retorna um fallback., Retorna o nome público mais adequado do usuário. (+1 more)

### Community 46 - "FakeInteractionResponse"
Cohesion: 0.18
Nodes (5): FakeFollowup, FakeInteractionResponse, Embed, Captura a resposta inicial da interação slash., Captura as respostas posteriores ao defer.

### Community 47 - "MemberGrowthStore"
Cohesion: 0.19
Nodes (7): MemberGrowthStore, _microseconds(), Connection, datetime, Path, Histórico SQLite de membros, com consultas agregadas e índices por servidor e…, T

### Community 48 - "InstagramOAuthStateStore"
Cohesion: 0.24
Nodes (6): InstagramOAuthStateStore, datetime, Estados OAuth de uso único para os endpoints de autorização., Guarda estados de uso único somente pelo tempo necessário para o callback., Cria um state criptograficamente aleatório e registra sua expiração., Valida e remove o state, impedindo seu reuso.

### Community 49 - "general.py"
Cohesion: 0.09
Nodes (21): Erro seguro e genérico de uma integração com a Twitch., TwitchError, CurrentTwitchLiveRepository, TwitchStreamClient, GetCurrentTwitchLive, Consulta a live configurada e confirma seu estado antes de um reenvio., Obtém a live atual e confirma que ela ainda está online antes do reenvio., is_instagram_post() (+13 more)

### Community 50 - "test_validator_validates_once_and_stops_cleanly"
Cohesion: 0.28
Nodes (6): FakeTwitchClient, asyncio, Testes do ciclo de vida do validador periódico de token Twitch., Cliente mínimo que registra validações sem chamadas HTTP., A tarefa pode ser iniciada uma vez e cancelada sem deixar trabalho pendente., test_validator_validates_once_and_stops_cleanly()

### Community 51 - ".configure_roles"
Cohesion: 0.40
Nodes (4): command, has_permissions, Interaction, Publica os menus uma única vez e devolve IDs para o administrador configurar.

### Community 52 - "SecretStore"
Cohesion: 0.25
Nodes (5): Protocol, Contrato mínimo para um serviço gerenciado de segredos., Lê o valor de um segredo pelo identificador configurado., Atualiza o valor de um segredo pelo identificador configurado., SecretStore

### Community 53 - "environment"
Cohesion: 0.33
Nodes (4): fixture, environment(), Fixtures compartilhadas, sem credenciais reais., Fornece o mínimo de configuração válida para os testes.

### Community 54 - "test_architecture.py"
Cohesion: 0.47
Nodes (5): parametrize, Protege as fronteiras para manter regras independentes de frameworks e I/O., test_adapters_do_not_import_each_other_or_the_composition_root(), test_architecture_has_explicit_layers(), test_inner_layers_only_depend_on_standard_library_and_inward_layers()

### Community 55 - "ValueError"
Cohesion: 0.25
Nodes (4): Client, View com botão de acesso à live da Twitch., TwitchNotificationView, ValueError

### Community 56 - "InstagramMedia"
Cohesion: 0.12
Nodes (22): LogCaptureFixture, InstagramMedia, Representa uma mídia retornada pela API Graph do Instagram., FailingInstagramClient, FailingSender, FakeInstagramClient, FakeSender, instagram_environment() (+14 more)

### Community 57 - "ServerGrowth"
Cohesion: 0.36
Nodes (15): GrowthStorageError, Falha segura ao registrar ou consultar movimentações do servidor., ServerGrowth, interaction(), parametrize, SimpleNamespace, Coleta sem cache de membros, privacidade do comando e exportação diária., repository() (+7 more)

### Community 58 - "use_cases/member_growth.py"
Cohesion: 0.20
Nodes (8): GrowthReader, GrowthRepository, _metrics(), datetime, Protocol, Consulta o histórico observado e preenche os dias sem movimentação., GrowthData, GrowthMetrics

### Community 59 - "test_reports_expired_or_invalid_token_without_exposing_it"
Cohesion: 0.14
Nodes (11): Erros de autenticação são convertidos em exceções seguras., A renovação usa GET, grant_type oficial e calcula a expiração em UTC., Token expirado pede reautorização e nunca reproduz o valor secreto no erro., Uma falha 5xx tem repetição limitada antes de aceitar a resposta oficial válida., A resposta oficial é convertida mesmo quando campos opcionais estão ausentes., test_lists_media_with_optional_fields(), handler(), test_refresh_reports_expired_token_without_exposing_it() (+3 more)

### Community 60 - ".send_instagram_notification"
Cohesion: 0.15
Nodes (9): File, AllowedMentions, Embed, Envia uma notificação para uma nova publicação do Instagram., Converte o tipo de produto Instagram em rótulo legível da notificação., Fornece a imagem local do gato quando o Reel não trouxer mídia da API., Envia conteúdo, embed, arquivo e componentes para um canal., Evita exceder os limites de texto do embed. (+1 more)

### Community 62 - "InstagramPoller"
Cohesion: 0.15
Nodes (10): InstagramMediaClient, InstagramMediaRepository, InstagramNotificationSender, PollInstagramMedia, Descobre novas publicações e registra apenas entregas confirmadas., InstagramPoller, Agenda consultas do Instagram sem incorporar as regras de notificação., Inicia uma única tarefa de polling quando a integração está ativada. (+2 more)

### Community 63 - "growth_report.py"
Cohesion: 0.33
Nodes (10): DailyMovement, GrowthReport, daily_coverage(), growth_csv(), growth_embed(), _local(), datetime, Embed (+2 more)

### Community 70 - "MembershipEvent"
Cohesion: 0.25
Nodes (5): RawMemberRemoveEvent, MembershipEvent, Guild, listener, Member

### Community 71 - "FakeResponse"
Cohesion: 0.20
Nodes (4): FakeFollowup, FakeResponse, Registra respostas iniciais de uma interaction., Registra mensagens posteriores ao defer.

### Community 82 - ".growth"
Cohesion: 0.25
Nodes (7): choices, command, default_permissions, describe, guild_only, has_permissions, Interaction

### Community 83 - "TwitchSettings"
Cohesion: 0.25
Nodes (5): Configurações necessárias para o EventSub da Twitch., TwitchSettings, AsyncClient, datetime, AsyncClient

### Community 84 - "InstagramTokenRefreshResult"
Cohesion: 0.33
Nodes (4): InstagramTokenRefreshResult, Resultado seguro de uma renovação bem-sucedida de token Instagram., Usa o mesmo cliente HTTP para renovar um token ainda válido., Exception

### Community 86 - "test_boolean_values_are_converted"
Cohesion: 0.40
Nodes (5): parametrize, Os formatos booleanos aceitos devem ser interpretados corretamente., O controle de repetição Twitch usa os mesmos formatos booleanos aceitos., test_boolean_values_are_converted(), test_twitch_retry_boolean_is_converted()

### Community 88 - "._schedule_idle_from_audio_thread"
Cohesion: 0.50
Nodes (3): AbstractEventLoop, Exception, Agenda a desconexão no loop correto após callback síncrono do player.

### Community 89 - ".__init__"
Cohesion: 0.50
Nodes (3): Bot, datetime, setup()

## Knowledge Gaps
- **21 isolated node(s):** `discord-bot`, `Organização do código`, `Requisitos`, `Instalação`, `API FastAPI local` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 869 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `test_role_management.py`, `test_temporary_voice.py`, `diagnose_server`, `test_welcome.py`, `.from_environment`, `TemporaryVoice`, `test_media_reactions.py`, `InstagramTokenData`, `test_instagram.py`, `TwitchOnlineEvent`, `test_twitch.py`, `test_discord_sender.py`, `test_run_services_composes_single_bot_and_cleans_up_tasks`, `MemberActivityLogs`, `NotificationStore`, `bootstrap.py`, `test_instagram_oauth.py`, `Music`, `test_web_app_exposes_health_and_initializes_shared_store`, `ports.py`, `test_twitch_auth.py`, `MediaReactions`, `test_validator_validates_once_and_stops_cleanly`, `ValueError`, `InstagramMedia`, `test_reports_expired_or_invalid_token_without_exposing_it`, `test_boolean_values_are_converted`?**
  _High betweenness centrality (0.259) - this node is a cross-community bridge._
- **Why does `DiscordBot` connect `Settings` to `Music`, `ports.py`, `TemporaryVoice`, `test_media_reactions.py`, `MediaReactions`, `general.py`, `GrowthQuery`, `TwitchOnlineEvent`, `CommandAccessTree`, `.__init__`, `use_cases/member_growth.py`, `bootstrap.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `Music` connect `Music` to `Settings`, `ports.py`, `test_music.py`, `.play_youtube`, `._schedule_idle_from_audio_thread`, `bootstrap.py`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 99 inferred relationships involving `Settings` (e.g. with `_configure_background_tasks()` and `main()`) actually correct?**
  _`Settings` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `InstagramMedia` (e.g. with `InstagramMediaClient` and `InstagramMediaRepository`) actually correct?**
  _`InstagramMedia` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 34 inferred relationships involving `General` (e.g. with `DiscordNotificationError` and `InstagramAPIError`) actually correct?**
  _`General` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `DiscordBot` (e.g. with `_configure_background_tasks()` and `AudioSource`) actually correct?**
  _`DiscordBot` has 23 INFERRED edges - model-reasoned connections that need verification._