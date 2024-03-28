PYTHON_VERSION ?= 3.9

dist: clean-dist venv
	. venv/bin/activate && python3 -m build .

.PHONY: setup
setup: venv/setup.txt

venv:
	virtualenv venv --python=${PYTHON_VERSION}

venv/setup.txt: venv dev-requirements.txt
	. venv/bin/activate && \
	pip3 install --upgrade pip && \
	pip3 install --requirement dev-requirements.txt
	touch venv/setup.txt

.PHONY: clean
clean: clean-dist
	rm -rf venv

.PHONY: clean-dist
clean-dist:
	rm -rf build
	rm -rf src/json_normalize.egg-info
	rm -rf dist

.PHONY: test
test: setup
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -vv -rsx tests/ src/ --cov ./src/json_normalize/ --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8 src --exclude '#*,~*,.#*'
	@ . venv/bin/activate && black --check src/ tests/

.PHONY: test-focus
test-focus: setup
	@ . venv/bin/activate && PYTHONPATH=src/ pytest -vv -m focus -rsx tests/ src/ --cov ./src/json_normalize/ --no-cov-on-fail --cov-report term-missing --doctest-modules --doctest-continue-on-failure
	@ . venv/bin/activate && flake8 src --exclude '#*,~*,.#*'
	@ . venv/bin/activate && black --check src/ tests/

.PHONY: release
release: test dist
	. venv/bin/activate && twine upload dist/*

.PHONY: test-release
test-release: test dist
	. venv/bin/activate && twine upload -r testpypi dist/*
