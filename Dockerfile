# --- Estágio 1: Builder ---
FROM python:3.10-slim AS builder

WORKDIR /build

# Instala Poetry
RUN pip install poetry

# Copia os arquivos de definição de projeto
COPY pyproject.toml poetry.lock ./

# Instala as dependências em um ambiente virtual
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-ansi --no-root --only main

# --- Estágio 2: Runner ---
FROM python:3.10-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
# ENV PYTHONPATH="/app"  <--- REMOVA ESTA LINHA

# Instala o curl (necessário para o healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Cria a estrutura de diretórios
WORKDIR /app

# Copia o ambiente virtual do estágio de build
COPY --from=builder /build/.venv /app/.venv

# Copia APENAS a pasta 'professors' (o módulo Python) para /app/professors
COPY professors/ /app/professors/

# --- REMOVA AS LINHAS ABAIXO ---
# COPY alembic/ /app/alembic/
# COPY alembic.ini /app/alembic.ini
# --- FIM DA REMOÇÃO ---

# Expõe a porta
EXPOSE 8081

# --- ALTERE O CMD ABAIXO ---
# Comando para iniciar a aplicação (sem alembic)
CMD ["python", "-m", "uvicorn", "professors.main:app", "--host", "0.0.0.0", "--port", "8082"]