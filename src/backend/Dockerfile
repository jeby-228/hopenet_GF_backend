# syntax=docker/dockerfile:1.13.0


ARG SRC=./src
ARG APP=backend
ARG _UV_ENV=/opt/venv


FROM python:3.12.8-bookworm AS base
ENV PYTHONPYCACHEPREFIX=/tmp/.pycache


FROM base AS uv
ARG _UV_ENV
ENV VIRTUAL_ENV=${_UV_ENV}
ENV UV_PROJECT_ENVIRONMENT=${_UV_ENV}
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="${_UV_ENV}/bin:$PATH"
# https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /bin/uv
RUN uv venv ${_UV_ENV}


FROM uv AS deps
ARG SRC
ARG APP
WORKDIR /srv/${APP}
COPY \
    ${SRC}/${APP}/pyproject.toml \
    ${SRC}/${APP}/uv.lock \
    ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project


FROM uv as runner
ARG SRC
ARG APP
ARG _UV_ENV
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /srv/${APP}
COPY --from=deps ${_UV_ENV} ${_UV_ENV}


FROM runner
ARG SRC
ARG APP
COPY ./${SRC}/${APP}/ /srv/${APP}/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD [ "uvicorn", "--host=0.0.0.0", "--workers=4", "app.main:app" ]
