"""Transforma fatos do servidor em problemas e correções acionáveis."""

from bot.domain.diagnostics import (
    ChannelSnapshot,
    DiagnosticCheck,
    DiagnosticReport,
    RoleSnapshot,
    ServerSnapshot,
)


def diagnose_server(snapshot: ServerSnapshot) -> DiagnosticReport:
    checks = [
        DiagnosticCheck(
            "Conexão Discord",
            "ok" if snapshot.connected else "error",
            f"Gateway conectado; latência {snapshot.latency_ms} ms."
            if snapshot.connected and snapshot.latency_ms is not None
            else "Gateway sem conexão confirmada; verifique a conexão e os logs do processo.",
        ),
        DiagnosticCheck(
            "Membro do bot",
            "ok" if snapshot.bot_member_available else "error",
            "Membro do bot disponível no servidor."
            if snapshot.bot_member_available
            else "Não foi possível resolver o membro do bot para verificar permissões.",
        ),
        DiagnosticCheck(
            "Eventos de membros",
            "ok" if snapshot.members_intent else "error",
            "Intents.members solicitado pelo código. Confirme também Server Members Intent "
            "no Developer Portal; essa ativação não pode ser verificada por este comando."
            if snapshot.members_intent
            else "Habilite Intents.members no código e Server Members Intent no Developer Portal.",
        ),
        DiagnosticCheck(
            "Eventos de moderação",
            "ok" if snapshot.moderation_intent else "warning",
            "Intents.moderation solicitado."
            if snapshot.moderation_intent
            else "Eventos de banimento não chegarão sem Intents.moderation.",
        ),
        DiagnosticCheck(
            "Eventos de mensagens",
            "ok" if snapshot.messages_intent else "warning",
            "Intents.guild_messages solicitado; registros usam apenas metadados."
            if snapshot.messages_intent
            else "Eventos de edição/exclusão não chegarão sem Intents.guild_messages.",
        ),
    ]
    checks.extend(_diagnose_channel(channel) for channel in snapshot.channels)
    checks.extend(_diagnose_role(role) for role in snapshot.roles)
    return DiagnosticReport(tuple(checks))


def _diagnose_channel(channel: ChannelSnapshot) -> DiagnosticCheck:
    if channel.channel_id is None:
        return DiagnosticCheck(
            channel.label,
            "error" if channel.required else "disabled",
            f"Sem canal configurado. Defina {channel.setting_key}.",
        )
    if not channel.exists:
        return DiagnosticCheck(
            channel.label,
            "error",
            f"Canal {channel.channel_id} não encontrado ou sem acesso. "
            f"Confira {channel.setting_key}.",
        )
    if not channel.same_guild:
        return DiagnosticCheck(channel.label, "error", "O canal pertence a outro servidor.")
    if not channel.valid_type:
        return DiagnosticCheck(channel.label, "error", "O tipo do canal não atende a esse recurso.")
    if channel.missing_permissions:
        return DiagnosticCheck(
            channel.label,
            "error",
            "Ajuste as permissões efetivas do bot neste canal: "
            + ", ".join(channel.missing_permissions)
            + ".",
        )
    if channel.publicly_visible:
        return DiagnosticCheck(
            channel.label,
            "warning",
            "O canal de registros está visível para @everyone. "
            "Restrinja Ver canal à equipe para preservar os registros administrativos.",
        )
    return DiagnosticCheck(
        channel.label, "ok", f"Canal {channel.channel_id} acessível e configurado."
    )


def _diagnose_role(role: RoleSnapshot) -> DiagnosticCheck:
    if not role.exists:
        return DiagnosticCheck(role.label, "error", f"Cargo {role.role_id} não encontrado.")
    if role.requires_assignment and not role.assignable:
        return DiagnosticCheck(
            role.label,
            "error",
            "Confira Gerenciar cargos e a hierarquia: o cargo deve ficar abaixo do cargo "
            "mais alto do bot e não pode ser @everyone ou gerenciado por uma integração.",
        )
    return DiagnosticCheck(role.label, "ok", f"Cargo {role.role_id} disponível.")
