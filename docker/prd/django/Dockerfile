FROM python:3.12-slim

RUN echo "==> Dockerfile setup started"
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN echo "==> Updating ubuntu apt packages..."
RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional \
    build-essential libpq-dev

RUN echo "==> Copying poetry files..."
COPY poetry.lock pyproject.toml /app/

RUN echo "==> Installing dependencies..."
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN echo "==> Copying entrypoint script..."
COPY ./docker/prd/django/start /start

RUN echo "==> Making start script executable..."
RUN chmod +x /start

COPY . /app/
