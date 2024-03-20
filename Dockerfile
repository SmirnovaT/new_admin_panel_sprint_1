FROM python:3.8.10-slim-buster

ENV \
  DEBIAN_FRONTEND=noninteractive \
  DEBCONF_NOWARNINGS=yes \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.1
WORKDIR /app/

RUN pip install poetry==$POETRY_VERSION

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false  && \
  poetry install --only main --no-interaction --no-ansi


COPY . /app/
