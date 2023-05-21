VENV = source .venv/bin/activate

all: deps format lint test

deps:
	poetry install

format:
	@$(VENV) && (black . && isort .)

lint:
	@$(VENV) && ( \
	flake8 --config=./pyproject.toml ./**/*.py && \
	black ./ --check && \
	isort ./ --check-only \
	)

test:
	@$(VENV) && (pytest --cov=./app --cov-report=term)

run:
	@$(VENV) && python -m app.main

docker-build:
	docker-compose build app

docker-run: docker-build
	docker-compose up app
