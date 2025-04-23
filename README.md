# Semana Code Desafio Backend

Este projeto foi desenvolvido como parte do desafio da **Semana Code - Backend**. Ele consiste em uma API para gerenciamento de enquetes com suporte a WebSockets para atualizações em tempo real.

## 📌 Tecnologias utilizadas

- **FastAPI** — framework web moderno e rápido
- **SQLModel** — ORM baseado em SQLAlchemy + Pydantic
- **Pydantic** — para validação e serialização de dados
- **WebSockets** — para comunicação em tempo real
- **Docker** — para containerização da aplicação e do banco de dados
- **PostgreSQL** — banco de dados relacional

## 🚀 Como rodar o projeto

### Pré-requisitos

- Docker e Docker Compose instalados

## 🛠️ Configuração do ambiente

Antes de rodar a aplicação, você precisa configurar um arquivo `.env` na raiz do projeto com as variáveis de ambiente essenciais para o funcionamento da API e do banco de dados.

1. Exemplo de `.env`

      ```env
   # URL base da aplicação frontend durante prod (Opcional)
   APP_URL=

   # URL da aplicação frontend durante desenvolvimento
   DEV_URL=http://localhost:3000

   # Conexão com o banco de dados
   DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<nome_do_banco>

   # Configurações do banco de dados para o container Docker
   POSTGRES_USER=<usuario>
   POSTGRES_PASSWORD=<senha>
   POSTGRES_DB=<nome_do_banco>

---


### Rodando com Docker

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/semana-code-backend.git
   cd semana-code-backend
2. Suba o container
   ```bash
   docker-compose up --build
3. Acesse a documentação Swagger
    ```bash
    http://0.0.0.0:8000

---

## 📄 Documentação da API

#### Cria uma nova enquete

\`\`\`http
POST /enquetes
\`\`\`

| Parâmetro          | Tipo         | Descrição                                  |
| :----------------- | :----------- | :------------------------------------------|
| \`pergunta\`         | \`string\`     | **Obrigatório**. Título da enquete         |
| \`data_inicio\`      | \`datetime\`   | **Obrigatório**. Data de início            |
| \`data_fim\`         | \`datetime\`   | **Obrigatório**. Data de término           |
| \`opcoes\`           | \`list\`       | **Obrigatório**. Lista de opções           |

#### Edita uma enquete existente

\`\`\`http
PATCH /enquetes?id={id}
\`\`\`

| Parâmetro   | Tipo       | Descrição                                |
| :---------- | :--------- | :----------------------------------------|
| \`id\`        | \`string\`   | **Obrigatório**. ID da enquete           |
| \`pergunta\`  | \`string\`   | Nova pergunta                            |
| \`data_inicio\` | \`datetime\` | Nova data de início                     |
| \`data_fim\`  | \`datetime\` | Nova data de término                     |
| \`status\`    | \`string\`   | Status da enquete                        |
| \`opcoes\`    | \`list\`     | Opções atualizadas                       |

#### Exclui uma enquete

\`\`\`http
DELETE /enquetes?id={id}
\`\`\`

| Parâmetro   | Tipo     | Descrição                                |
| :---------- | :------- | :----------------------------------------|
| \`id\`        | \`string\` | **Obrigatório**. ID da enquete           |

#### Retorna enquetes

\`\`\`http
GET /enquetes
\`\`\`

| Parâmetro   | Tipo     | Descrição                                |
| :---------- | :------- | :----------------------------------------|
| \`status\`    | \`string\` | (Opcional). Filtra por status da enquete |

#### Registra um voto

\`\`\`http
PUT /voto?id={opcao_id}
\`\`\`

| Parâmetro   | Tipo     | Descrição                                     |
| :---------- | :------- | :---------------------------------------------|
| \`id\`        | \`string\` | **Obrigatório**. ID da opção a ser votada     |

#### WebSocket para atualizações em tempo real

\`\`\`http
WS /ws/enquetes
\`\`\`

Conecte-se a este endpoint para receber atualizações de enquetes em tempo real sempre que um voto for registrado.

---

## 🧠 Estrutura do projeto

- \`controller/\`: lógica de controle das rotas
- \`database/\`: conexão e modelos do banco de dados
- \`requests/\`: schemas de entrada e validação
- \`infrastructure/\`: gerenciamento de conexões WebSocket (broadcast)
- \`setup/\`: Configurações da aplicação

---

## 📦 Instalação local (sem Docker)

1. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt

3. Execute a aplicação:

   ```bash
   uvicorn main:app --reload

---

