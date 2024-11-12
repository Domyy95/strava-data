# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help
FILE=VERSION
VERSION=`cat $(FILE)`
COMMIT_MSG_HOOK = '\#!/bin/bash\nMSG_FILE=$$1\ncz check --allow-abort --commit-msg-file $$MSG_FILE'

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo Commands available:
	@echo 	- make install-pip-tools: install pip-tools
	@echo 	- make requirements-dev.txt: create requirements-dev.txt from requirements-dev.in
	@echo 	- make requirements.txt: create requirements.txt from requirements.in
	@echo 	- make install-dev: install development dependencies from requirements-dev.txt
	@echo 	- make install: install dependencies from requirements.txt
	@echo 	- make setup-dev-env: run make install-dev + add git hook for commits syntax checking
	@echo   - make build: run python setup.py build
	@echo 	- make test: run the test suite
	@echo 	- make test-report: run the test suite and generate a .xml report
	@echo 	- make clean: remove __pycache__ directories and other garbage
	@echo   Versioning commands:
	@echo 	- make echo-version: print out the project version
	@echo   - make bump: update version and changelog + tag and commit
	@echo   - make bump-version-minor: release as minor
	@echo   - make bump-version-major: release as major
	@echo   - make bump-version-patch: release as patch
	@echo   - make run: run the streamlit app
	@echo "------------------------------------"


install-pip-tools:
	pip install --upgrade pip
	pip install --upgrade pip-tools

requirements-dev.txt: requirements-dev.in install-pip-tools
	pip-compile --upgrade --resolver backtracking --output-file=$@ requirements-dev.in

requirements.txt: requirements.in install-pip-tools
	pip-compile --upgrade --resolver backtracking --output-file=$@ requirements.in

install-dev: requirements-dev.txt
	pip install  -r requirements-dev.txt

install: requirements.txt
	pip install  -r requirements.txt

setup-dev-env: install-dev
	pre-commit install
	echo $(COMMIT_MSG_HOOK) > .git/hooks/commit-msg
	chmod +x .git/hooks/commit-msg

build:
	python setup.py build

test: install-dev install
	python -m py.test ./tests

test-report: install-dev install
	pytest --junitxml=report.xml ./tests

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;
	find . -type d -name .hypothesis -prune -exec rm -rf {} \;
	find . -type d -name .ipynb_checkpoints -prune -exec rm -rf {} \;
	find . -type d -name .pytest_cache -prune -exec rm -rf {} \;
	find . -type d -name .mypy_cache -prune -exec rm -rf {} \;

ndef = $(if $(value $(1)),,$(error $(1) not set, provide $(1), e.g. make $(1)=<value> <target>))

echo-version:
	$(call ndef,VERSION)
	@echo $(VERSION)

# this will update the version, changelog, tag and commit
bump: fetch-tags setup-dev-env
	cz bump

bump-version-minor: fetch-tags setup-dev-env
	cz bump --increment MINOR

bump-version-major: fetch-tags setup-dev-env
	cz bump --increment MAJOR

bump-version-patch: fetch-tags setup-dev-env
	cz bump --increment PATCH

run:
	python -m streamlit run src/main.py
