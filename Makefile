PYTHON=$(shell which python3 )
VERSION=`cat ums/VERSION`

ifeq (, $(PYTHON))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.10
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'from sys import version_info as v; v_min=int("".join("$(PYTHON_VERSION_MIN)".split("."))); print(0) if int(str(v.major)+str(v.minor)) >= v_min else print(1)')
PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )

PIP=$(PYTHON) -m pip
PYDOC=pydoc3

ifeq ($(PYTHON_VERSION_OK),1)
  $(error "Requires Python >= $(PYTHON_VERSION_MIN) - Installed: $(PYTHON_VERSION)")
endif

help: ## Print help for each target
	$(info Things3 low-level Python API.)
	$(info =============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

.PHONY: install
install: ## Installs dependencies.
	pip3 install poetry && poetry install

.PHONY: seed
seed: ## Add admin credentials to DB.
	PYTHONPATH="." $(PYTHON) scripts/seed.py

.PHONY: data
data: ## Add dummy login creds to DB.
	PYTHONPATH="." $(PYTHON) scripts/data.py

.PHONY: run
run: ## Run the ums server.
	poetry run $(PYTHON) -m ums

.PHONY: test
test: ## Run ums tests
	poetry run pytest -vv --cov="ums" .

.PHONY: clean
clean: ## remove the python binary files.
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -rf build dist *.egg-info .pytest_cache cov_html .coverage .mypy_cache .trunk

.PHONY: lint
lint: ## Lint the code
	flake8

doc: ## Document the code
	@$(PYDOC) ums
