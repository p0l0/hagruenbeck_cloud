all:
	@echo
	@echo "Available targets"
	@echo ""
	@echo "develop	       -- start Home Assistant Instance for Development"
	@echo ""
	@echo "test_setup      -- setup env for testing"
	@echo ""
	@echo "pre-commit      -- run pre-commit tests"
	@echo ""
	@echo "pylint          -- run pylint tests"
	@echo ""
	@echo "lint            -- run all linting tests"

develop:
	@pip install -r requirements/development.txt
	@bash scripts/develop

test_setup:
	@pip install -r requirements/testing.txt

pre-commit: test_setup
	@pre-commit run --all-files

lint: pre-commit

