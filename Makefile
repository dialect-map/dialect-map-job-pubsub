APP_VERSION   = $(shell cat VERSION)
COV_CONFIG    = ".coveragerc"
SOURCE_FOLDER = "src"
TESTS_FOLDER  = "tests"
TESTS_PARAMS  = "-p no:cacheprovider"
TYPING_PARAMS = "--allow-redefinition --ignore-missing-imports --cache-dir=/dev/null"


.PHONY: check
check:
	@echo "Checking code format"
	@black --check $(SOURCE_FOLDER)
	@black --check $(TESTS_FOLDER)
	@echo "Checking type annotations"
	@mypy "$(TYPING_PARAMS)" $(SOURCE_FOLDER)
	@mypy "$(TYPING_PARAMS)" $(TESTS_FOLDER)


.PHONY: install-dev
install-dev:
	@echo "Installing Development packages"
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt
	@pre-commit install


.PHONY: run
run:
	@echo "Computing data diffs"
	@python3 $(SOURCE_FOLDER)/main.py diff
	@echo "Dispatching data changes"
	@python3 $(SOURCE_FOLDER)/main.py run


.PHONY: test
test:
	@echo "Testing code"
	@pytest --cov-config=$(COV_CONFIG) --cov=$(SOURCE_FOLDER) "$(TESTS_PARAMS)"
