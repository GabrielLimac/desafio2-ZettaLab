# Modelo de Entidade e Relacionamento (ER)

## Visão Geral

O banco de dados da API de Gerenciamento de Tarefas é composto por duas entidades principais: **User** (Usuário) e **Task** (Tarefa), com um relacionamento de um-para-muitos entre elas.

## Entidades

### 1. User (Usuário)

Representa os usuários do sistema que podem criar e gerenciar tarefas.

**Atributos:**
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT): Identificador único do usuário
- `name` (VARCHAR(100), NOT NULL): Nome completo do usuário
- `email` (VARCHAR(120), UNIQUE, NOT NULL): Email do usuário (usado para login)
- `password_hash` (VARCHAR(255), NOT NULL): Senha hasheada do usuário
- `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP): Data e hora de criação
- `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE): Data e hora da última atualização

**Índices:**
- PRIMARY KEY: `id`
- UNIQUE INDEX: `email`

**Restrições:**
- `email` deve ser único no sistema
- `name` não pode ser vazio
- `password_hash` é gerado automaticamente pelo sistema

### 2. Task (Tarefa)

Representa as tarefas criadas pelos usuários.

**Atributos:**
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT): Identificador único da tarefa
- `name` (VARCHAR(200), NOT NULL): Nome/título da tarefa
- `description` (TEXT, NULLABLE): Descrição detalhada da tarefa
- `status` (VARCHAR(20), NOT NULL, DEFAULT 'pendente'): Status da tarefa
- `user_id` (INTEGER, FOREIGN KEY, NOT NULL): Referência ao usuário proprietário
- `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP): Data e hora de criação
- `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE): Data e hora da última atualização

**Índices:**
- PRIMARY KEY: `id`
- FOREIGN KEY INDEX: `user_id`

**Restrições:**
- `name` não pode ser vazio
- `status` deve ser 'pendente' ou 'concluida'
- `user_id` deve referenciar um usuário existente
- Ao excluir um usuário, suas tarefas são excluídas automaticamente (CASCADE)

## Relacionamentos

### User → Task (1:N)

- **Tipo**: Um-para-Muitos
- **Descrição**: Um usuário pode ter várias tarefas, mas cada tarefa pertence a apenas um usuário
- **Chave Estrangeira**: `task.user_id` → `user.id`
- **Comportamento de Exclusão**: CASCADE (ao excluir usuário, suas tarefas são excluídas)

## Diagrama ER

```
┌─────────────────────────────────┐
│             USER                │
├─────────────────────────────────┤
│ PK  id (INTEGER)                │
│     name (VARCHAR(100))         │
│ UK  email (VARCHAR(120))        │
│     password_hash (VARCHAR(255))│
│     created_at (DATETIME)       │
│     updated_at (DATETIME)       │
└─────────────────────────────────┘
                │
                │ 1
                │
                │ has
                │
                │ N
                ▼
┌─────────────────────────────────┐
│             TASK                │
├─────────────────────────────────┤
│ PK  id (INTEGER)                │
│     name (VARCHAR(200))         │
│     description (TEXT)          │
│     status (VARCHAR(20))        │
│ FK  user_id (INTEGER)           │
│     created_at (DATETIME)       │
│     updated_at (DATETIME)       │
└─────────────────────────────────┘
```

## Scripts SQL de Criação

### Tabela Users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Tabela Tasks

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

### Triggers para Updated_at (SQLite)

```sql
-- Trigger para atualizar updated_at na tabela users
CREATE TRIGGER update_users_updated_at 
    AFTER UPDATE ON users
    FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para atualizar updated_at na tabela tasks
CREATE TRIGGER update_tasks_updated_at 
    AFTER UPDATE ON tasks
    FOR EACH ROW
BEGIN
    UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

## Consultas Comuns

### Buscar todas as tarefas de um usuário

```sql
SELECT t.* FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.id = ?
ORDER BY t.created_at DESC;
```

### Buscar tarefas por status

```sql
SELECT * FROM tasks
WHERE user_id = ? AND status = ?
ORDER BY created_at DESC;
```

### Estatísticas de tarefas por usuário

```sql
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) as pendente,
    SUM(CASE WHEN status = 'concluida' THEN 1 ELSE 0 END) as concluida
FROM tasks
WHERE user_id = ?;
```

### Buscar usuário por email

```sql
SELECT * FROM users WHERE email = ?;
```

## Considerações de Performance

1. **Índices**: Criados nos campos mais consultados (email, user_id, status)
2. **Paginação**: Implementada nas consultas de listagem para evitar sobrecarga
3. **Relacionamentos**: Uso de FOREIGN KEY com CASCADE para manter integridade
4. **Timestamps**: Triggers automáticos para atualização de `updated_at`

## Segurança

1. **Senhas**: Armazenadas como hash usando Werkzeug
2. **Isolamento**: Cada usuário só acessa suas próprias tarefas
3. **Validação**: Constraints de banco garantem integridade dos dados
4. **Autenticação**: JWT tokens para controle de acesso

## Escalabilidade

Para ambientes de produção com maior volume, considere:

1. **Migração para PostgreSQL**: Melhor performance e recursos avançados
2. **Particionamento**: Por usuário ou data para tabelas grandes
3. **Índices compostos**: Para consultas complexas frequentes
4. **Cache**: Redis para sessões e consultas frequentes

