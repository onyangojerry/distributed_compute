SHELL := /bin/bash
.DEFAULT_GOAL := help

# Colors
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Variables
DOCKER_COMPOSE := docker compose
PYTHON := python3
NODE := npm

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Distributed File Storage System$(RESET)"
	@echo "$(BLUE)================================$(RESET)"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# Development
.PHONY: dev
dev: ## Start development environment
	@echo "$(BLUE)Starting development environment...$(RESET)"
	$(DOCKER_COMPOSE) up --build

.PHONY: dev-detached
dev-detached: ## Start development environment in background
	@echo "$(BLUE)Starting development environment in background...$(RESET)"
	$(DOCKER_COMPOSE) up -d --build

.PHONY: stop
stop: ## Stop all services
	@echo "$(BLUE)Stopping all services...$(RESET)"
	$(DOCKER_COMPOSE) down

.PHONY: restart
restart: stop dev-detached ## Restart all services

.PHONY: logs
logs: ## Show logs from all services
	$(DOCKER_COMPOSE) logs -f

.PHONY: status
status: ## Show status of all services
	$(DOCKER_COMPOSE) ps

# Testing
.PHONY: test
test: test-unit test-integration ## Run all tests

.PHONY: test-unit
test-unit: ## Run unit tests
	@echo "$(BLUE)Running unit tests...$(RESET)"
	$(PYTHON) -m pytest tests/unit/ -v --cov=controller --cov=nodes --cov=utils

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(RESET)"
	$(DOCKER_COMPOSE) up -d --build
	@sleep 10
	$(PYTHON) -m pytest tests/integration/ -v
	$(DOCKER_COMPOSE) down

.PHONY: test-performance
test-performance: ## Run performance tests
	@echo "$(BLUE)Running performance tests...$(RESET)"
	$(DOCKER_COMPOSE) up -d --build
	@sleep 10
	locust -f tests/load/upload_test.py --host=http://localhost:8000 --headless --users 10 --spawn-rate 2 --run-time 2m
	$(DOCKER_COMPOSE) down

.PHONY: test-security
test-security: ## Run security tests
	@echo "$(BLUE)Running security tests...$(RESET)"
	bandit -r controller/ nodes/ utils/
	safety check
	cd web-ui && npm audit

# Code Quality
.PHONY: format
format: ## Format code
	@echo "$(BLUE)Formatting Python code...$(RESET)"
	black controller/ nodes/ utils/ tests/
	@echo "$(BLUE)Formatting JavaScript code...$(RESET)"
	cd web-ui && $(NODE) run format

.PHONY: lint
lint: ## Lint code
	@echo "$(BLUE)Linting Python code...$(RESET)"
	flake8 controller/ nodes/ utils/ tests/ --max-line-length=88 --extend-ignore=E203,W503
	mypy controller/ nodes/ utils/ --ignore-missing-imports
	@echo "$(BLUE)Linting JavaScript code...$(RESET)"
	cd web-ui && $(NODE) run lint

.PHONY: check
check: format lint ## Run all code quality checks

# Build and Deploy
.PHONY: build
build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(RESET)"
	$(DOCKER_COMPOSE) build

.PHONY: build-prod
build-prod: ## Build production Docker images
	@echo "$(BLUE)Building production Docker images...$(RESET)"
	docker build -t distributed-storage-controller:latest ./controller
	docker build -t distributed-storage-node:latest ./nodes

.PHONY: push
push: build-prod ## Build and push Docker images
	@echo "$(BLUE)Pushing Docker images...$(RESET)"
	docker push distributed-storage-controller:latest
	docker push distributed-storage-node:latest

# Database and Storage
.PHONY: clean-data
clean-data: ## Clean all data volumes
	@echo "$(RED)WARNING: This will delete all stored files!$(RESET)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	$(DOCKER_COMPOSE) down -v
	docker volume prune -f

.PHONY: backup-data
backup-data: ## Backup all data
	@echo "$(BLUE)Creating data backup...$(RESET)"
	@mkdir -p backups/$(shell date +%Y%m%d_%H%M%S)
	docker run --rm -v distributed_compute_metadata_volume:/data -v $(PWD)/backups/$(shell date +%Y%m%d_%H%M%S):/backup alpine tar czf /backup/metadata.tar.gz -C /data .
	@echo "$(GREEN)Backup created in backups/$(shell date +%Y%m%d_%H%M%S)$(RESET)"

# Monitoring
.PHONY: health
health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(RESET)"
	@curl -s http://localhost:8000/health | jq . || echo "$(RED)Controller not responding$(RESET)"
	@curl -s http://localhost:9001/health | jq . || echo "$(RED)Node 1 not responding$(RESET)"
	@curl -s http://localhost:9002/health | jq . || echo "$(RED)Node 2 not responding$(RESET)"
	@curl -s http://localhost:9003/health | jq . || echo "$(RED)Node 3 not responding$(RESET)"

.PHONY: metrics
metrics: ## Show system metrics
	@echo "$(BLUE)System metrics:$(RESET)"
	@curl -s http://localhost:8000/status | jq .

.PHONY: monitor
monitor: ## Start monitoring dashboard
	@echo "$(BLUE)Starting monitoring dashboard...$(RESET)"
	@echo "Access dashboard at: http://localhost:8000/dashboard"
	@open http://localhost:8000/dashboard 2>/dev/null || true

# Scaling
.PHONY: scale-up
scale-up: ## Scale up storage nodes
	@echo "$(BLUE)Scaling up storage nodes...$(RESET)"
	$(DOCKER_COMPOSE) up -d --scale node1=2 --scale node2=2 --scale node3=2

.PHONY: scale-down
scale-down: ## Scale down storage nodes
	@echo "$(BLUE)Scaling down storage nodes...$(RESET)"
	$(DOCKER_COMPOSE) up -d --scale node1=1 --scale node2=1 --scale node3=1

# Documentation
.PHONY: docs
docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(RESET)"
	@mkdir -p docs
	@echo "Documentation generated in docs/"

.PHONY: api-docs
api-docs: dev-detached ## Generate API documentation
	@echo "$(BLUE)Generating API documentation...$(RESET)"
	@sleep 5
	@curl -s http://localhost:8000/openapi.json > docs/openapi.json
	@echo "$(GREEN)API documentation saved to docs/openapi.json$(RESET)"
	@echo "$(GREEN)View interactive docs at: http://localhost:8000/docs$(RESET)"

# Utilities
.PHONY: shell-controller
shell-controller: ## Open shell in controller container
	$(DOCKER_COMPOSE) exec controller bash

.PHONY: shell-node
shell-node: ## Open shell in node container
	$(DOCKER_COMPOSE) exec node1 bash

.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing Python development dependencies...$(RESET)"
	pip install -r requirements-dev.txt
	@echo "$(BLUE)Installing Node.js development dependencies...$(RESET)"
	cd web-ui && $(NODE) install

.PHONY: update-deps
update-deps: ## Update dependencies
	@echo "$(BLUE)Updating Python dependencies...$(RESET)"
	pip-compile requirements.in
	@echo "$(BLUE)Updating Node.js dependencies...$(RESET)"
	cd web-ui && $(NODE) update

.PHONY: clean
clean: ## Clean build artifacts and temporary files
	@echo "$(BLUE)Cleaning build artifacts...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/ 2>/dev/null || true
	cd web-ui && rm -rf node_modules/.cache dist/ .cache/ 2>/dev/null || true

.PHONY: reset
reset: stop clean-data clean ## Complete reset of the environment
	@echo "$(RED)Environment reset complete$(RESET)"