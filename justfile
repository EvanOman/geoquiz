set dotenv-load

default:
    @just --list

# Run the development server
dev:
    uv run uvicorn geoquiz.app:app --reload --host 0.0.0.0 --port ${PORT:-9100}

# Run tests
test *args:
    uv run pytest {{args}}

# Lint and format
lint:
    uv run ruff check src/ tests/
    uv run ruff format --check src/ tests/

# Fix lint issues
fix:
    uv run ruff check --fix src/ tests/
    uv run ruff format src/ tests/

# Install dependencies
install:
    uv sync
