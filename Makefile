
dist: clean-dist
	python3 setup.py sdist

setup: venv

venv: requirements.txt
	virtualenv venv --python=${PYTHON_VERSION}
	. venv/bin/activate; pip3 install \
	-r requirements.txt

.PHONY: test
test: venv
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -rsx -s --flake8 tests/ src/ --cov ./src/json_normalize/ --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8  src --exclude '#*,~*,.#*'

.PHONY: clean
clean: clean-dist
	rm -rf venv

.PHONY: clean-dist
clean-dist:
	rm -rf build
	rm -rf src/json_normalize.egg-info
	rm -rf dist
