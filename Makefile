.PHONY: run test lint check clean install

install:
	uv sync

run:
	uv run agent-app

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .
	uv run ruff format .

check:
	uv run ruff check .
	uv run ruff format . --check
	uv run mypy src/

clean:
	rm -rf `find . -name __pycache__`
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
