.PHONY: install test lint format check clean build publish

# Colours
GREEN := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RESET := $(shell tput -Txterm sgr0)

.DEFAULT_GOAL := help

# 🧩 Development

install: ## Install dependencies
	@echo "$(GREEN)Installing dependencies...$(RESET)"
	pip install -e ".[dev]"

# 🧪 Testing

test: ## Run tests
	@echo "$(GREEN)Running tests...$(RESET)"
	pytest tests/ -v

test-cov: ## Run tests with coverage
	@echo "$(GREEN)Running tests with coverage...$(RESET)"
	pytest tests/ -v --cov=src/mailjunky --cov-report=term-missing --cov-report=html

# 🔍 Linting

lint: ## Run linters
	@echo "$(GREEN)Running ruff...$(RESET)"
	ruff check src tests
	@echo "$(GREEN)Running mypy...$(RESET)"
	mypy src

format: ## Format code
	@echo "$(GREEN)Formatting code...$(RESET)"
	ruff check --fix src tests
	ruff format src tests

# ✅ CI

check: lint test ## Run all checks
	@echo "$(GREEN)All checks passed!$(RESET)"

# 📦 Build

clean: ## Clean build artifacts
	@echo "$(GREEN)Cleaning...$(RESET)"
	rm -rf dist/ build/ *.egg-info src/*.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage

build: clean ## Build package
	@echo "$(GREEN)Building package...$(RESET)"
	python -m build

publish: build ## Publish to PyPI
	@echo "$(GREEN)Publishing to PyPI...$(RESET)"
	python -m twine upload dist/*

# 📖 Help

help: ## Show this help
	@echo "$(GREEN)mailjunky-python$(RESET) - Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}'
