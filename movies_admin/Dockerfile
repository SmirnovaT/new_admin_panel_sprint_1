FROM python:3.8-slim-buster

ENV \
  DJANGO_SETTINGS_MODULE='config.settings' \
  DEBIAN_FRONTEND=noninteractive \
  DEBCONF_NOWARNINGS=yes \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.1

WORKDIR /app

COPY run_uwsgi.sh run_uwsgi.sh

RUN groupadd -r web && useradd -d /app -r -g web web \
    && chown web:web -R /app


RUN pip install poetry==$POETRY_VERSION && \
apt update && apt install -y libxmlsec1-dev \
&& apt install -y gcc && apt -y autoremove

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY . .

COPY .env /app/.env

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

USER web

ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]