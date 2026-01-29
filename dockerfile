# USAMOS PYTHON 3.11 (Compatible con tus dependencias)
FROM python:3.11-slim-bookworm

# 1. Instalamos uv (copiándolo desde su imagen oficial, es el truco moderno)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 2. Configuración de entorno
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# 3. Copiamos los archivos de dependencias primero (para aprovechar el caché de Docker)
COPY pyproject.toml uv.lock ./

# 4. Instalamos las dependencias en el sistema (sin crear venv virtual dentro de Docker)
RUN uv pip install --system -r pyproject.toml

# 5. Copiamos el código fuente
COPY src/ ./src/
COPY config/ ./config/
# Nota: No copiamos el .env por seguridad, se pasa al correr el contenedor

# 6. Exponemos el puerto
EXPOSE 8000

# 7. Comando para arrancar el servidor
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]