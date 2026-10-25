"""Descrições e exemplos exibidos pelo comando /comandos."""

COMMAND_HELP: dict[str, tuple[str, str, str]] = {
    "crescimento": (
        "Analisa entradas, saídas e saldo por período, com série diária e CSV.",
        "/crescimento periodo:7d ou /crescimento inicio:01/10/2026 fim:24/10/2026",
        "Gerenciar servidor.",
    ),
    "diagnostico": (
        "Mostra um relatório privado de configuração, canais, cargos e permissões.",
        "/diagnostico",
        "Gerenciar servidor.",
    ),
    "configurar-cargos": (
        "Cria ou atualiza as mensagens dos menus de cargos configurados.",
        "/configurar-cargos",
        "Gerenciar servidor.",
    ),
    "ping": (
        "Verifica se o bot está respondendo.",
        "/ping",
        "todos os membros.",
    ),
    "chamar": (
        "Envia um aviso privado ao moderador configurado.",
        "/chamar",
        "todos os membros.",
    ),
    "id_usuario": (
        "Exibe o ID Discord de um usuário selecionado.",
        "/id_usuario usuario:@membro",
        "todos os membros.",
    ),
    "boasvindas": (
        "Envia a mensagem privada de boas-vindas para um usuário.",
        "/boasvindas usuario:@membro",
        "Gerenciar servidor.",
    ),
    "reenviar_live": (
        "Reenvia a notificação da última live aberta.",
        "/reenviar_live",
        "Gerenciar servidor.",
    ),
    "reenviar_reel": (
        "Reenvia a notificação do Reel mais recente do Instagram.",
        "/reenviar_reel",
        "Gerenciar servidor.",
    ),
    "reenviar_post": (
        "Reenvia a notificação do post mais recente do Instagram.",
        "/reenviar_post",
        "Gerenciar servidor.",
    ),
    "comandos": (
        "Lista os comandos disponíveis e como usá-los.",
        "/comandos",
        "todos os membros.",
    ),
    "limpar": (
        "Apaga a quantidade informada de mensagens anteriores no mesmo canal.",
        "/limpar <quantidade>",
        "Gerenciar mensagens.",
    ),
}


MUSIC_COMMAND_HELP: tuple[tuple[str, str], ...] = (
    (
        "/tocar_youtube",
        "Entra no seu canal de voz e toca o áudio de um vídeo do YouTube.\n"
        "Uso: `/tocar_youtube url:https://www.youtube.com/watch?v=VIDEO_ID`\n"
        "Permissão: você precisa estar em um canal de voz.",
    ),
    (
        "/parar_musica",
        "Interrompe a reprodução atual.\nUso: `/parar_musica`\n"
        "Permissão: estar no mesmo canal de voz que o Morcegão.",
    ),
    (
        "/sair_call",
        "Para a música e desconecta do canal de voz.\nUso: `/sair_call`\n"
        "Permissão: estar no mesmo canal de voz que o Morcegão.",
    ),
)
