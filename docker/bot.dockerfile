FROM python:slim

WORKDIR /bot/

RUN pip install --upgrade pip && pip install poetry

COPY poetry.lock pyproject.toml /bot/

RUN poetry install

COPY src /bot/
