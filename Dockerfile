FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .

ENV PYTHONPATH="${PYTHONPATH}:/app/src"
RUN apt-get update && apt-get upgrade -y

RUN pip install poetry

RUN poetry config virtualenvs.create false  \
    && poetry lock --no-update  \
    && poetry install --no-dev --no-root
COPY . .