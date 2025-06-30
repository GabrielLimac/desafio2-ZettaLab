# API de Gerenciamento de Tarefas (To-Do List)

Uma API REST completa para gerenciamento de tarefas desenvolvida com Flask, SQLite e autenticação JWT.

## 📋 Funcionalidades

- ✅ **Autenticação de usuários** com JWT
- ✅ **CRUD completo de tarefas**
- ✅ **Filtros por status** (pendente, concluída)
- ✅ **Associação de tarefas por usuário**
- ✅ **Validação de dados**
- ✅ **Testes unitários e de integração**
- ✅ **Documentação completa da API**

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11, Flask
- **Banco de Dados**: SQLite
- **Autenticação**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **Testes**: pytest
- **CORS**: Flask-CORS
- **Hash de Senhas**: Werkzeug

## 📁 Estrutura do Projeto

```
todo-api/
├── src/
│   ├── models/          # Modelos de dados (User, Task)
│   ├── routes/          # Rotas da API (auth, tasks)
│   ├── services/        # Lógica de negócio
│   ├── middleware/      # Middleware de autenticação
│   ├── config.py        # Configurações da aplicação
│   └── main.py          # Ponto de entrada da aplicação
├── tests/               # Testes unitários e de integração
├── venv/                # Ambiente virtual Python
├── init_db.py           # Script de inicialização do banco
├── requirements.txt     # Dependências Python
├── Dockerfile           # Configuração Docker
├── docker-compose.yml   # Orquestração Docker
└── README.md            # Documentação principal
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- pip (gerenciador de pacotes Python)

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd todo-api
```

### 2. Criar e ativar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Inicializar banco de dados

```bash
python init_db.py
```

O script perguntará se você deseja criar dados de exemplo. Digite 's' para criar um usuário de teste.

### 5. Executar a aplicação

```bash
python src/main.py
```

A API estará disponível em: `http://localhost:5001`

## 📊 Modelo de Dados

### Usuário (User)
- `id`: Identificador único
- `name`: Nome do usuário
- `email`: Email (único)
- `password_hash`: Senha hasheada
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Tarefa (Task)
- `id`: Identificador único
- `name`: Nome da tarefa
- `description`: Descrição (opcional)
- `status`: Status ('pendente' ou 'concluida')
- `user_id`: ID do usuário proprietário
- `created_at`: Data de criação
- `updated_at`: Data de atualização

## 🔗 Endpoints da API

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/register` | Registrar novo usuário |
| POST | `/api/login` | Fazer login |
| POST | `/api/refresh` | Renovar token |
| GET | `/api/profile` | Obter perfil do usuário |
| PUT | `/api/profile` | Atualizar perfil |

### Tarefas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/tasks` | Criar nova tarefa |
| GET | `/api/tasks` | Listar tarefas |
| GET | `/api/tasks/{id}` | Obter tarefa específica |
| PUT | `/api/tasks/{id}` | Atualizar tarefa |
| DELETE | `/api/tasks/{id}` | Excluir tarefa |
| GET | `/api/tasks/stats` | Estatísticas das tarefas |
| GET | `/api/tasks/pending` | Listar tarefas pendentes |
| GET | `/api/tasks/completed` | Listar tarefas concluídas |

### Utilitários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Verificar saúde da API |

## 🧪 Executar Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar testes com cobertura
pytest tests/ --cov=src

# Executar testes específicos
pytest tests/test_models.py -v
```

## 🐳 Docker

### Executar com Docker

```bash
# Construir imagem
docker build -t todo-api .

# Executar container
docker run -p 5001:5001 todo-api
```

### Executar com Docker Compose

```bash
docker-compose up -d
```

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` para configurações personalizadas:

```env
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta
JWT_SECRET_KEY=sua-chave-jwt
DATABASE_URL=sqlite:///app.db
```

## 🔒 Autenticação

A API usa JWT (JSON Web Tokens) para autenticação. Após fazer login, inclua o token no header:

```
Authorization: Bearer <seu-token-jwt>
```

## 📈 Status Codes

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Erro de validação
- `401` - Não autorizado
- `404` - Não encontrado
- `500` - Erro interno do servidor

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autor

Desenvolvido como parte de um projeto de demonstração de API REST com Flask.

---

Para mais detalhes sobre os endpoints, consulte a [Documentação da API](docs/api-documentation.md).

