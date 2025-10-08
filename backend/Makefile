SHELL := /bin/bash
.DEFAULT_GOAL := help

COMPOSE_LOCAL := docker-compose.local.yaml


help: ## Display this help text
	@grep -E '^[a-zA-Z_%-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "} {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

## --- Poetry ---

poetry_login_staging: ## Configure Poetry for STAGING (pre-release versions)
	@echo "Ensuring you are authenticated with gcloud: gcloud auth application-default login"
	@echo "Configuring Poetry for staging development (pre-release versions)..."
	@echo "Using GCP Project: $(GCP_STAGING_PROJECT_ID)"
	poetry config keyring.enabled false
	ENV=staging AR_REGION=$(GCP_REGION) ./scripts/poetry-bootstrap.sh
	poetry config --local http-basic.staging-python-packages _ $$(gcloud auth print-access-token)

install: ## Install Python dependencies with Poetry
	poetry install

format: ## Auto-format code with Black & isort
	poetry run black .
	poetry run isort .

lint: ## Run linters (Black, isort check, Pylint)
	poetry run black --check .
	poetry run isort --check-only .
	poetry run pylint src

test: ## Run all pytest tests
	poetry run pytest -v --cov=src --cov-report=term-missing

## --- Docker ---

build: ## Build local Docker images
	docker-compose -f $(COMPOSE_LOCAL) build

up: ## Start local services in background
	docker-compose -f $(COMPOSE_LOCAL) up -d

down: ## Stop & remove local services
	docker-compose -f $(COMPOSE_LOCAL) down

restart: ## Rebuild & restart local services
	$(MAKE) down
	$(MAKE) build
	$(MAKE) up

logs: ## Tail logs for all local services
	docker-compose -f $(COMPOSE_LOCAL) logs -f

## --- Database and Migrations ---

migrate: ## Run all pending migrations locally
	docker-compose -f $(COMPOSE_LOCAL) run --rm migrations

rollback: ## Roll back the most recent migration locally
	docker-compose -f $(COMPOSE_LOCAL) run --rm migrations down

dbshell: ## Open a psql shell to the local Postgres
	docker-compose -f $(COMPOSE_LOCAL) exec postgres psql -U postgres


