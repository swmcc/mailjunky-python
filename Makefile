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

# 📦 Build & Release

VERSION := $(shell grep 'version = ' pyproject.toml | head -1 | cut -d'"' -f2)

clean: ## Clean build artifacts
	@echo "$(GREEN)Cleaning...$(RESET)"
	rm -rf dist/ build/ *.egg-info src/*.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage

build: clean ## Build package
	@echo "$(GREEN)Building package...$(RESET)"
	python -m build

release: ## Tag and push release (triggers CI publish to PyPI)
	@echo "$(YELLOW)Creating release v$(VERSION)...$(RESET)"
	@if git rev-parse v$(VERSION) >/dev/null 2>&1; then \
		echo "$(YELLOW)Tag v$(VERSION) already exists!$(RESET)"; \
		exit 1; \
	fi
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)
	@echo "$(GREEN)Tag v$(VERSION) pushed! GitHub Actions will publish to PyPI.$(RESET)"
	@echo "  Watch: https://github.com/swmcc/mailjunky-python/actions"

# 📖 Help

help: ## Show this help
	@echo "$(GREEN)mailjunky-python$(RESET) - Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}'
