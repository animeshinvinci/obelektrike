clean:
	find apps -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find apps -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1
	rm -f .coverage
	rm -rf htmlcov

start:
	python manage.py runserver

isort:
	isort -rc apps

lint:
	flake8 --show-source apps
	isort --check-only -rc apps --diff

test:
	pytest apps/tests

all: clean lint test
