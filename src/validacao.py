
"""Funções de validação das entradas do usuário."""

STATUS_VALIDOS = ("A Fazer", "Em Progresso", "Concluído")


def validar_titulo(titulo):
    """Retorna o título sem espaços extras ou lança ValueError."""
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("O título é obrigatório.")
    titulo = titulo.strip()
    if len(titulo) > 100:
        raise ValueError("O título deve ter no máximo 100 caracteres.")
    return titulo


def validar_status(status):
    """Retorna o status se for um dos permitidos ou lança ValueError."""
    if status not in STATUS_VALIDOS:
        raise ValueError(
            "Status inválido. Use: " + ", ".join(STATUS_VALIDOS) + "."
        )
    return status
