📘 API – Fila de Atendimento

Projeto desenvolvido como avaliação final da disciplina de Desenvolvimento de APIs, utilizando FastAPI para gerenciar uma fila de atendimento presencial.

🚀 Funcionalidades
Endpoints obrigatórios

GET /fila → Lista clientes não atendidos.

GET /fila/{id} → Retorna cliente pela posição da fila.

POST /fila → Adiciona cliente (nome + tipo N/P).

PUT /fila → Avança a fila (primeiro vira atendido).

DELETE /fila/{id} → Remove cliente e reordena a fila.

Bônus

Sistema de prioridade (P antes de N).

▶️ Como executar
pip install -r requirements.txt
uvicorn main:app --reload


Acesse a documentação:
👉 http://127.0.0.1:8000/docs

🧪 Testes
pytest

📂 Repositório

https://github.com/julianafabricio/avaliacao-api

👩‍💻 Autora

Juliana Soares
