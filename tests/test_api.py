import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "teste.db"))
    app.config["TESTING"] = True
    return app.test_client()


def test_criar_e_listar_tarefa(client):
    resposta = client.post("/api/tarefas", json={"titulo": "Tarefa 1"})
    assert resposta.status_code == 201
    assert resposta.get_json()["status"] == "A Fazer"
    assert len(client.get("/api/tarefas").get_json()) == 1


def test_criar_sem_titulo_retorna_400(client):
    resposta = client.post("/api/tarefas", json={"descricao": "sem título"})
    assert resposta.status_code == 400


def test_atualizar_status(client):
    tarefa = client.post("/api/tarefas", json={"titulo": "Mover"}).get_json()
    resposta = client.put(
        f"/api/tarefas/{tarefa['id']}", json={"status": "Em Progresso"}
    )
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "Em Progresso"


def test_atualizar_status_invalido(client):
    tarefa = client.post("/api/tarefas", json={"titulo": "X"}).get_json()
    resposta = client.put(
        f"/api/tarefas/{tarefa['id']}", json={"status": "Inventado"}
    )
    assert resposta.status_code == 400


def test_excluir_tarefa(client):
    tarefa = client.post("/api/tarefas", json={"titulo": "Apagar"}).get_json()
    assert client.delete(f"/api/tarefas/{tarefa['id']}").status_code == 204
    assert client.get(f"/api/tarefas/{tarefa['id']}").status_code == 404


def test_buscar_inexistente(client):
    assert client.get("/api/tarefas/999").status_code == 404