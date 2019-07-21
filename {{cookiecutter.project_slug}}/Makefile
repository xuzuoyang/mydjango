lint:
	flake8 --format=pylint --count

test: clean lint
	pytest tests/

clean:
	- find . -iname "*__pycache__" | xargs rm -rf
	- find . -iname "*.pyc" | xargs rm -rf
	- rm -rf .pytest_cache

devserve:
	./manage.py runserver 0.0.0.0:8000

format:
	yapf -i --recursive .
	isort -rc .
