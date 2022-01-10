FROM python:alpine

ENV PYTHONPATH /bot
ENV POETRY_VIRTUALENVS_CREATE false

RUN apk add --update --no-cache build-base gcc make musl-dev libffi-dev \
    postgresql-dev python3-dev

WORKDIR /bot/

RUN pip install --upgrade pip && pip install poetry psycopg2

COPY poetry.lock pyproject.toml alembic.ini /bot/

RUN poetry install

COPY src /bot/
