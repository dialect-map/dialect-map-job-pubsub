APP_VERSION    = $(shell cat VERSION)
SCRIPTS_FOLDER = "scripts"
SOURCE_FOLDER  = "src"
TYPING_PARAMS  = "--allow-redefinition --ignore-missing-imports --cache-dir=/dev/null"


.PHONY: check
check:
	@echo "Checking code format"
	@black --check $(SOURCE_FOLDER)
	@echo "Checking type annotations"
	@mypy "$(TYPING_PARAMS)" $(SOURCE_FOLDER)


.PHONY: install-dev
install-dev:
	@echo "Installing Development packages"
	@sh "$(SCRIPTS_FOLDER)/0_install_jd.sh"
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt
	@pre-commit install
