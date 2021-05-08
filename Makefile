build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

uninstall:
	python3 -m pip uninstall hexlet-code

lint:
	poetry run flake8 page_loader/

test:
	poetry run pytest -vv tests/test.py

coverage:
	poetry run pytest --cov=page_loader tests/test.py --cov-report xml

cov-html:
	poetry run pytest --cov=page_loader tests/test.py --cov-report html

reinstall:
	rm dist -r
	python3 -m pip uninstall hexlet-code
	poetry build
	python3 -m pip install --user dist/*.whl