.PHONY: run test lint format clean

run:
	uv run run-app

test:
	uv run pytest tests/

lint:
	uv run ruff check .
	uv run mypy src/

format:
	uv run ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage .mypy_cache
