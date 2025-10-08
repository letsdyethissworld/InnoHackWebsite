# --- Base image ---
FROM python:3.12-slim AS base_image

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /home/app
ENV WORKDIR=/home/app

RUN apt-get update && apt-get -y --no-install-recommends install \
      make git sudo curl wget build-essential openssh-client \
      libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
      python3 python3-pip python3-dev gcc tree libmagic-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10
RUN groupadd -g 1001 app && useradd -u 1001 -m app -g app -d ${WORKDIR}

# Install Poetry
ENV POETRY_VERSION=2.1.3
ENV POETRY_HOME=/home/app/poetry
RUN curl -sSL https://install.python-poetry.org \
      | POETRY_HOME=${POETRY_HOME} python - --version $POETRY_VERSION
ENV PATH=${POETRY_HOME}/bin:$PATH

# Never create virtualenvs inside the container
RUN poetry config virtualenvs.create false

# Allow pip to upgrade system packages if needed
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# --- Application image ---
FROM base_image AS blog_service

# Default to dev so local builds never need a GCP token
ARG ENVIRONMENT=dev
ARG GCP_POETRY_TOKEN=""
ARG AR_REGION=""

# Ensure our code is on PYTHONPATH
ENV PYTHONPATH=${WORKDIR}:${PYTHONPATH}

# Copy only dependency metadata, then install
COPY pyproject.toml poetry.lock* ./

RUN if [ "$ENVIRONMENT" = "staging" ] && [ -n "$GCP_POETRY_TOKEN" ]; then \
      echo "Staging build: using GCP Artifact Registry credentials"; \
      # (Re)generate lockfile or inject HTTP basic credentials here if have private deps… \
      poetry install --only main --no-root; \
    else \
      echo "Dev build: installing from public PyPI"; \
      poetry install --only main --no-root; \
    fi && \
    poetry cache clear . --all -n

# Copy the rest of source
COPY src ${WORKDIR}/src

# Fix permissions and switch to non-root
RUN chown -R app:app ${WORKDIR} && \
    mkdir -p ${WORKDIR}/static && \
    chown -R app:app ${WORKDIR}/static

USER app

EXPOSE 8080
CMD ["python", "src/api/webserver.py"]
