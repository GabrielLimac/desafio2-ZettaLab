# Dockerfile para API de Gerenciamento de Tarefas

# Usar imagem base do Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para banco de dados
RUN mkdir -p src/database

# Inicializar banco de dados
RUN python init_db.py <<< "n"

# Expor porta da aplicação
EXPOSE 5001

# Definir variáveis de ambiente
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Comando para executar a aplicação
CMD ["python", "src/main.py"]

