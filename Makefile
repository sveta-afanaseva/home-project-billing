VENV = source .venv/bin/activate

all: deps format lint test

deps:
	poetry install

format:
	@$(VENV) && (black . && isort .)

lint:
	@$(VENV) && ( \
	pylint --rcfile=./pyproject.toml ./**/*.py && \
	black ./ --check && \
	isort ./ --check-only \
	)

test:
	@$(VENV) && (pytest --cov=./app --cov-report=term)

run:
	@$(VENV) && python -m app.main
