# TechFlow Tasks

Sistema web de gerenciamento de tarefas com Kanban, desenvolvido pela
TechFlow Solutions (empresa fictícia) para uma startup de logística.

## Objetivo
Permitir acompanhar o fluxo de trabalho da equipe em tempo real,
priorizar tarefas críticas e monitorar o desempenho.

## Escopo inicial (v1.0)
- Criar, listar, editar e excluir tarefas (CRUD)
- Quadro Kanban com colunas: A Fazer, Em Progresso, Concluído
- Validação de dados de entrada
- Testes automatizados + integração contínua

## Metodologia
Kanban (híbrido com ideias do Scrum): tarefas no GitHub Projects,
limite de trabalho em andamento, entregas pequenas e frequentes,
commits semânticos.

## Como executar
1. `python -m venv venv` e ative o ambiente
2. `pip install -r requirements.txt`
3. `python src/app.py`
4. Acesse http://127.0.0.1:5000

## Como testar
`pytest -v`

## Estrutura
- `src/` código-fonte · `tests/` testes · `docs/` diagramas