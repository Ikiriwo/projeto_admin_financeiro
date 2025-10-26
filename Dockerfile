FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretório de uploads e templates
RUN mkdir -p uploads templates

# Copiar o código da aplicação
COPY . .

# Copiar os templates para o diretório correto
COPY projeto_admin_financeiro/templates/ /app/templates/

# Expor a porta que o Flask vai usar
EXPOSE 5000

# Variáveis de ambiente para conexão com PostgreSQL
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=admin_financeiro
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Variáveis de ambiente para Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
