FROM python:3.11.0-slim-bullseye AS build

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install "poetry==$POETRY_VERSION"

COPY ./docker/celery/* ./celery/
RUN sed -i 's/\r$//g' celery/*.sh
RUN chmod +x ./celery/*.sh

ARG SRC=/src

WORKDIR ${SRC}
COPY poetry.lock pyproject.toml ./

RUN touch requirements.txt
RUN poetry export --with dev -f requirements.txt --output requirements.txt
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r requirements.txt && rm -rf $POETRY_CACHE_DIR

FROM build AS finally

ARG BUILD_ENVIRONMENT=dev
WORKDIR ${SRC}
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    procps

COPY --from=build /usr/src/app/wheels  /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./docker/django.sh /django.sh
RUN sed -i 's/\r$//g' /django.sh && chmod +x /django.sh

COPY ./docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

COPY . /src

ENTRYPOINT ["/entrypoint.sh"]
