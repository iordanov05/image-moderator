.PHONY: dev install lint format type test pre-commit

PYTHON := python

install:           
	$(PYTHON) -m pip install -r requirements.txt 

dev:        
	uvicorn app.main:app --reload --env-file .env

lint:               
	ruff check .

format:          
	ruff format .

type:              
	mypy app

test:             
	pytest -q

pre-commit:       
	$(MAKE) format lint type test
