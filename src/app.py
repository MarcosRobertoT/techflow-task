from flask import Flask, jsonify, render_template, request

import database as db
from validacao import validar_status, validar_titulo


def create_app(db_path="tasks.db"):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path
    db.iniciar_banco(db_path)

    def caminho():
        return app.config["DB_PATH"]

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/tarefas", methods=["GET"])
    def listar():
        return jsonify(db.listar_tarefas(caminho()))

    @app.route("/api/tarefas/<int:tarefa_id>", methods=["GET"])
    def detalhar(tarefa_id):
        tarefa = db.buscar_tarefa(caminho(), tarefa_id)
        if tarefa is None:
            return jsonify({"erro": "Tarefa não encontrada."}), 404
        return jsonify(tarefa)

    @app.route("/api/tarefas", methods=["POST"])
    def criar():
        dados = request.get_json(silent=True) or {}
        try:
            titulo = validar_titulo(dados.get("titulo"))
            status = validar_status(dados.get("status", "A Fazer"))
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        tarefa = db.criar_tarefa(
            caminho(), titulo, str(dados.get("descricao", "")), status
        )
        return jsonify(tarefa), 201

    @app.route("/api/tarefas/<int:tarefa_id>", methods=["PUT"])
    def atualizar(tarefa_id):
        if db.buscar_tarefa(caminho(), tarefa_id) is None:
            return jsonify({"erro": "Tarefa não encontrada."}), 404
        dados = request.get_json(silent=True) or {}
        campos = {}
        try:
            if "titulo" in dados:
                campos["titulo"] = validar_titulo(dados["titulo"])
            if "status" in dados:
                campos["status"] = validar_status(dados["status"])
            if "descricao" in dados:
                campos["descricao"] = str(dados["descricao"])
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        return jsonify(db.atualizar_tarefa(caminho(), tarefa_id, **campos))

    @app.route("/api/tarefas/<int:tarefa_id>", methods=["DELETE"])
    def excluir(tarefa_id):
        if not db.excluir_tarefa(caminho(), tarefa_id):
            return jsonify({"erro": "Tarefa não encontrada."}), 404
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
