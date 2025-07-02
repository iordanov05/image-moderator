.PHONY: dev install lint format fix type test pre-commit docker build compose-up compose-down

PYTHON := python


install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --env-file .env

lint:
	ruff check .

format:
	ruff format .

fix:
	ruff check --fix .

type:
	mypy app

test:
	pytest -q

pre-commit:
	$(MAKE) format lint type test


docker:
	docker build -t image-moderator .

run:
	docker run --env-file .env -p 8000:8000 image-moderator

compose-up:
	docker compose up --build -d

compose-down:
	docker compose down
