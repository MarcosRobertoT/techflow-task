"""Camada de acesso ao banco de dados SQLite."""
import sqlite3
from contextlib import closing


def conectar(caminho):
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn


def _executar(caminho, sql, params=()):
    with closing(conectar(caminho)) as conn:
        with conn:  # faz commit automático
            cur = conn.execute(sql, params)
            linhas = [dict(linha) for linha in cur.fetchall()]
            return linhas, cur.lastrowid, cur.rowcount


def iniciar_banco(caminho):
    _executar(caminho, """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'A Fazer',
            prioridade TEXT NOT NULL DEFAULT 'Média'
        )
    """)


# ---------- CRUD ----------

def criar_tarefa(caminho, titulo, descricao="", status="A Fazer",prioridade="Média"):
    _, novo_id, _ = _executar(
        caminho,
        "INSERT INTO tarefas (titulo, descricao, status, prioridade) "
        "VALUES (?, ?, ?, ?)",
        (titulo, descricao, status, prioridade),
    )
    return buscar_tarefa(caminho, novo_id)


def listar_tarefas(caminho):
    return _executar(caminho, """
        SELECT * FROM tarefas
        ORDER BY CASE prioridade
        WHEN 'Alta' THEN 1 WHEN 'Média' THEN 2 ELSE 3 END, id
    """)[0]


def buscar_tarefa(caminho, tarefa_id):
    linhas = _executar(
        caminho, "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
    )[0]
    return linhas[0] if linhas else None


def atualizar_tarefa(caminho, tarefa_id, **campos):
    permitidos = {
        k: v for k, v in campos.items()
        if k in ("titulo", "descricao", "status", "prioridade")
    }
    if permitidos:
        sets = ", ".join(f"{k} = ?" for k in permitidos)
        _executar(
            caminho,
            f"UPDATE tarefas SET {sets} WHERE id = ?",
            (*permitidos.values(), tarefa_id),
        )
    return buscar_tarefa(caminho, tarefa_id)


def excluir_tarefa(caminho, tarefa_id):
    return _executar(
        caminho, "DELETE FROM tarefas WHERE id = ?", (tarefa_id,)
    )[2] > 0
