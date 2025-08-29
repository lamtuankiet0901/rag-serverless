# Define variables
ENV_FILE := .env
BUILD_DIR := .aws-sam/build
FUNCTION_DIR := lambdas
LAYER_DIR := layers
ARTIFACTS_DIR := build_artifacts

# Python
PYTHON_VERSION := $(shell cat .python-version)
PYTHON := python$(PYTHON_VERSION)
VENV_DIR := venv

# Get all Lambda directories dynamically
LAMBDA_DIRS := $(shell find $(FUNCTION_DIR) -mindepth 1 -maxdepth 1 -type d)
LAYER_DIRS := $(shell find $(LAYER_DIR) -mindepth 1 -maxdepth 1 -type d)

# Setup the local environment
venv: clean-venv
	@echo "Creating virtual environment with $(PYTHON)..."
	$(PYTHON) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && $(PYTHON) -m pip install --upgrade pip wheel setuptools
	. $(VENV_DIR)/bin/activate && $(PYTHON) -m pip install poetry

install:
	@echo "Installing dependencies..."
	. $(VENV_DIR)/bin/activate && poetry lock
	. $(VENV_DIR)/bin/activate && poetry install

setup-pre-commit:
	@echo "Setting up pre-commit hooks..."
	. $(VENV_DIR)/bin/activate && poetry run pre-commit install

setup: venv install setup-pre-commit
	. $(VENV_DIR)/bin/activate && poetry show
	@echo "Setup [dev, layers] done. Run 'source $(VENV_DIR)/bin/activate' to activate the virtual environment."

# Format code & test
lint:
	ruff check $(FUNCTION_DIR)/ $(LAYER_DIR)/ tests/

fmt:
	@ruff format $(path)
	@isort $(path)

unit-test:
	poetry run pytest tests/$(LAYER_DIR)/ -v -s
	@for file in tests/lambdas/test_*.py; do \
		poetry run pytest $$file -v -s; \
	done

api-test:
	AWS_PROFILE=default sam local start-api --skip-pull-image

# Export dependencies for each Lambda
deps-lambdas:
	@echo "Export dependencies for Lambdas..."
	@poetry lock
	@for dir in $(LAMBDA_DIRS); do \
		lambda_name=$$(basename $$dir); \
		echo "Processing $$lambda_name..."; \
		if poetry show --with $$lambda_name > /dev/null 2>&1; then \
        	poetry export -f requirements.txt --with $$lambda_name --output $$dir/requirements.txt --without-hashes; \
		else \
			poetry export -f requirements.txt --output $$dir/requirements.txt --without-hashes; \
		fi \
	done

# Export dependencies for each layer
deps-layers:
	@echo "Export dependencies for layers..."
	@for dir in $(LAYER_DIRS); do \
		layer_name=$$(basename $$dir); \
		echo "Processing $$layer_name..."; \
		if poetry show --with $$layer_name > /dev/null 2>&1; then \
        	poetry export -f requirements.txt --with $$layer_name --output $$dir/requirements.txt --without-hashes; \
		else \
			poetry export -f requirements.txt --output $$dir/requirements.txt --without-hashes; \
		fi \
	done

# Export dependencies
deps: clean deps-lambdas deps-layers

# Build the SAM application
sam-build: deps
	sam validate --lint
	sam build --parallel --skip-pull-image

build: sam-build

# Package build artifacts into ZIP files
package: build
	@echo "Packaging build artifacts..."
	mkdir -p $(ARTIFACTS_DIR)
	@for dir in $(BUILD_DIR)/*/; do \
		artifact_name=$$(basename $$dir); \
		echo "Zipping $$artifact_name..."; \
		zip -r $(ARTIFACTS_DIR)/$$artifact_name.zip $$dir; \
	done

# Deploy
deploy:
	sam deploy --config-file samconfig.toml

apply: deploy clean

destroy:
	sam delete

# Clean build artifacts
clean:
	rm -rf .aws-sam .pytest_cache __pycache__ **/__pycache__ **/**/__pycache__ **/**/requirements.txt .mypy_cache .coverage $(ARTIFACTS_DIR)

clean-venv:
	rm -rf $(VENV_DIR)

# Show help information
help:
	@echo "Available commands:"
	@echo "  setup            - Setup the local environment with Poetry"
	@echo "  build            - Validate the SAM template and build the application"
	@echo "  package          - Package build artifacts into ZIP files"
	@echo "  lint             - Run linting on the codebase using ruff"
	@echo "  fmt path=...     - Format the codebase using ruff"
	@echo "  test             - Run unit tests using pytest"
	@echo "  clean            - Clean up build artifacts and cached files"
	@echo "  clean-venv       - Remove the virtual environment"
	@echo "  help             - Show this help information"

.PHONY: venv \
    install \
    setup \
    lint \
    fmt \
    test \
    deps-lambdas \
    deps-layers \
    deps \
    build \
    package \
    clean \
    clean-venv \
    help
