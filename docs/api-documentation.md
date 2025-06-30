# Documentação da API - Gerenciamento de Tarefas

## Visão Geral

Esta API REST permite o gerenciamento completo de tarefas (to-do list) com autenticação de usuários. Todas as respostas são em formato JSON.

**Base URL**: `http://localhost:5001/api`

## Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação. Após fazer login, inclua o token no header de todas as requisições protegidas:

```
Authorization: Bearer <token>
```

## Endpoints de Autenticação

### 1. Registrar Usuário

**POST** `/register`

Registra um novo usuário no sistema.

**Body (JSON):**
```json
{
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "password": "senha123"
}
```

**Resposta de Sucesso (201):**
```json
{
  "message": "Usuário criado com sucesso",
  "user": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "created_at": "2025-06-23T14:16:17.630107",
    "updated_at": "2025-06-23T14:16:17.630111"
  }
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "password": "senha123"
  }'
```

### 2. Fazer Login

**POST** `/login`

Autentica um usuário e retorna tokens JWT.

**Body (JSON):**
```json
{
  "email": "joao@exemplo.com",
  "password": "senha123"
}
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Login realizado com sucesso",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "created_at": "2025-06-23T14:16:17.630107",
    "updated_at": "2025-06-23T14:16:17.630111"
  }
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@exemplo.com",
    "password": "senha123"
  }'
```

### 3. Renovar Token

**POST** `/refresh`

Renova o token de acesso usando o refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Token renovado com sucesso",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 4. Obter Perfil

**GET** `/profile`

Obtém informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de Sucesso (200):**
```json
{
  "user": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "created_at": "2025-06-23T14:16:17.630107",
    "updated_at": "2025-06-23T14:16:17.630111"
  }
}
```

### 5. Atualizar Perfil

**PUT** `/profile`

Atualiza informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body (JSON):**
```json
{
  "name": "João Santos",
  "email": "joao.santos@exemplo.com",
  "password": "nova_senha123"
}
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Perfil atualizado com sucesso",
  "user": {
    "id": 1,
    "name": "João Santos",
    "email": "joao.santos@exemplo.com",
    "created_at": "2025-06-23T14:16:17.630107",
    "updated_at": "2025-06-23T14:20:30.123456"
  }
}
```

## Endpoints de Tarefas

### 1. Criar Tarefa

**POST** `/tasks`

Cria uma nova tarefa para o usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body (JSON):**
```json
{
  "name": "Estudar Flask",
  "description": "Aprender sobre desenvolvimento de APIs com Flask",
  "status": "pendente"
}
```

**Resposta de Sucesso (201):**
```json
{
  "message": "Tarefa criada com sucesso",
  "task": {
    "id": 1,
    "name": "Estudar Flask",
    "description": "Aprender sobre desenvolvimento de APIs com Flask",
    "status": "pendente",
    "user_id": 1,
    "created_at": "2025-06-23T14:25:00.123456",
    "updated_at": "2025-06-23T14:25:00.123456"
  }
}
```

**Exemplo com curl:**
```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <seu_token>" \
  -d '{
    "name": "Estudar Flask",
    "description": "Aprender sobre desenvolvimento de APIs com Flask",
    "status": "pendente"
  }'
```

### 2. Listar Tarefas

**GET** `/tasks`

Lista todas as tarefas do usuário autenticado com suporte a filtros e paginação.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Parâmetros de Query:**
- `status` (opcional): Filtrar por status ('pendente' ou 'concluida')
- `page` (opcional): Número da página (padrão: 1)
- `per_page` (opcional): Itens por página (padrão: 20, máximo: 100)

**Resposta de Sucesso (200):**
```json
{
  "message": "Tarefas obtidas com sucesso",
  "tasks": [
    {
      "id": 1,
      "name": "Estudar Flask",
      "description": "Aprender sobre desenvolvimento de APIs com Flask",
      "status": "pendente",
      "user_id": 1,
      "created_at": "2025-06-23T14:25:00.123456",
      "updated_at": "2025-06-23T14:25:00.123456"
    }
  ],
  "pagination": {
    "page": 1,
    "pages": 1,
    "per_page": 20,
    "total": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

**Exemplos com curl:**
```bash
# Listar todas as tarefas
curl -X GET http://localhost:5001/api/tasks \
  -H "Authorization: Bearer <seu_token>"

# Listar apenas tarefas pendentes
curl -X GET "http://localhost:5001/api/tasks?status=pendente" \
  -H "Authorization: Bearer <seu_token>"

# Listar com paginação
curl -X GET "http://localhost:5001/api/tasks?page=1&per_page=10" \
  -H "Authorization: Bearer <seu_token>"
```

### 3. Obter Tarefa Específica

**GET** `/tasks/{id}`

Obtém uma tarefa específica do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Tarefa encontrada",
  "task": {
    "id": 1,
    "name": "Estudar Flask",
    "description": "Aprender sobre desenvolvimento de APIs com Flask",
    "status": "pendente",
    "user_id": 1,
    "created_at": "2025-06-23T14:25:00.123456",
    "updated_at": "2025-06-23T14:25:00.123456"
  }
}
```

### 4. Atualizar Tarefa

**PUT** `/tasks/{id}`

Atualiza uma tarefa específica do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body (JSON):**
```json
{
  "name": "Estudar Flask - Avançado",
  "description": "Aprender conceitos avançados de Flask",
  "status": "concluida"
}
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Tarefa atualizada com sucesso",
  "task": {
    "id": 1,
    "name": "Estudar Flask - Avançado",
    "description": "Aprender conceitos avançados de Flask",
    "status": "concluida",
    "user_id": 1,
    "created_at": "2025-06-23T14:25:00.123456",
    "updated_at": "2025-06-23T14:30:00.123456"
  }
}
```

### 5. Excluir Tarefa

**DELETE** `/tasks/{id}`

Exclui uma tarefa específica do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Tarefa excluída com sucesso"
}
```

### 6. Estatísticas das Tarefas

**GET** `/tasks/stats`

Obtém estatísticas das tarefas do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Estatísticas obtidas com sucesso",
  "statistics": {
    "total": 10,
    "pendente": 6,
    "concluida": 4,
    "completion_rate": 40.0
  }
}
```

### 7. Listar Tarefas Pendentes

**GET** `/tasks/pending`

Lista apenas as tarefas pendentes do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Parâmetros de Query:**
- `page` (opcional): Número da página
- `per_page` (opcional): Itens por página

### 8. Listar Tarefas Concluídas

**GET** `/tasks/completed`

Lista apenas as tarefas concluídas do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Parâmetros de Query:**
- `page` (opcional): Número da página
- `per_page` (opcional): Itens por página

## Endpoints Utilitários

### 1. Verificar Saúde da API

**GET** `/health`

Verifica se a API está funcionando corretamente.

**Resposta de Sucesso (200):**
```json
{
  "status": "healthy",
  "message": "API de Gerenciamento de Tarefas está funcionando",
  "version": "1.1"
}
```

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Erro de validação ou dados inválidos |
| 401 | Não autorizado (token inválido ou ausente) |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

## Tratamento de Erros

Todas as respostas de erro seguem o formato:

```json
{
  "error": "Descrição do erro"
}
```

### Exemplos de Erros Comuns

**Token inválido (401):**
```json
{
  "error": "Token inválido"
}
```

**Dados obrigatórios ausentes (400):**
```json
{
  "error": "Campos obrigatórios ausentes: name, email"
}
```

**Email já cadastrado (400):**
```json
{
  "error": "Email já cadastrado"
}
```

**Tarefa não encontrada (404):**
```json
{
  "error": "Tarefa não encontrada"
}
```

## Validações

### Usuário
- **name**: Obrigatório, não pode estar vazio
- **email**: Obrigatório, deve ter formato válido, único no sistema
- **password**: Obrigatório, mínimo 6 caracteres

### Tarefa
- **name**: Obrigatório, máximo 200 caracteres
- **description**: Opcional, máximo 1000 caracteres
- **status**: Deve ser 'pendente' ou 'concluida'

## Exemplo de Fluxo Completo

```bash
# 1. Registrar usuário
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "João", "email": "joao@teste.com", "password": "123456"}'

# 2. Fazer login
TOKEN=$(curl -s -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "joao@teste.com", "password": "123456"}' | \
  grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# 3. Criar tarefa
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Minha primeira tarefa", "description": "Teste da API"}'

# 4. Listar tarefas
curl -X GET http://localhost:5001/api/tasks \
  -H "Authorization: Bearer $TOKEN"

# 5. Atualizar tarefa (ID 1)
curl -X PUT http://localhost:5001/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "concluida"}'

# 6. Obter estatísticas
curl -X GET http://localhost:5001/api/tasks/stats \
  -H "Authorization: Bearer $TOKEN"
```

