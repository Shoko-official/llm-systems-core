PYTHON ?= python3

.PHONY: validate lint test schedule-kpis

validate:
	$(PYTHON) scripts/validate_repo.py validate

lint:
	$(PYTHON) scripts/validate_repo.py lint

test:
	$(PYTHON) scripts/validate_repo.py test

schedule-kpis:
	$(PYTHON) scripts/schedule_kpi_update.py
