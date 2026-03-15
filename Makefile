# ─────────────────────────────────────────────────────────────────────────────
# Modular Entity System — developer Makefile
# Usage: make <target>
# ─────────────────────────────────────────────────────────────────────────────

PYTHON      := python3
MANAGE      := $(PYTHON) manage.py
PIP         := pip
SETTINGS    := modular_entity_system.settings.development
APPS        := vendor product course certification \
               vendor_product_mapping product_course_mapping course_certification_mapping

.PHONY: help install env migrate migrations superuser run shell \
        test test-cov lint clean logs

# ─── Help ─────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Modular Entity System — available commands"
	@echo ""
	@echo "  Setup"
	@echo "    make install        Install all dependencies"
	@echo "    make env            Copy .env.example → .env (edit before running)"
	@echo "    make migrations     Create new migration files for all apps"
	@echo "    make migrate        Apply all pending migrations"
	@echo "    make superuser      Create a Django superuser"
	@echo ""
	@echo "  Development"
	@echo "    make run            Start the development server"
	@echo "    make shell          Open the Django interactive shell"
	@echo "    make logs           Tail the application log"
	@echo ""
	@echo "  Quality"
	@echo "    make test           Run the full test suite"
	@echo "    make test-cov       Run tests with coverage report"
	@echo "    make lint           Run pyflakes over the project"
	@echo ""
	@echo "  Housekeeping"
	@echo "    make clean          Remove __pycache__ and .pyc files"
	@echo ""

# ─── Setup ────────────────────────────────────────────────────────────────────
install:
	$(PIP) install -r requirements.txt

env:
	@if [ -f .env ]; then \
		echo ".env already exists — not overwriting."; \
	else \
		cp .env.example .env; \
		echo ".env created. Please edit it before running the server."; \
	fi

migrations:
	@mkdir -p logs
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) makemigrations $(APPS)

migrate:
	@mkdir -p logs
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate

superuser:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) createsuperuser

# ─── Development ──────────────────────────────────────────────────────────────
run:
	@mkdir -p logs
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) runserver 0.0.0.0:8000

shell:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) shell

logs:
	@mkdir -p logs
	tail -f logs/app.log

# ─── Quality ──────────────────────────────────────────────────────────────────
test:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) pytest

test-cov:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) pytest --cov=. --cov-report=term-missing --cov-omit="*/migrations/*,manage.py,*/settings/*"

lint:
	$(PYTHON) -m pyflakes vendor product course certification \
	    vendor_product_mapping product_course_mapping course_certification_mapping core

# ─── Housekeeping ─────────────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	@echo "Cleaned."

# ─── Production (gunicorn) ────────────────────────────────────────────────────
serve:
	DJANGO_SETTINGS_MODULE=modular_entity_system.settings.production \
	gunicorn modular_entity_system.wsgi:application \
	    --workers 4 \
	    --bind 0.0.0.0:8000 \
	    --access-logfile logs/access.log \
	    --error-logfile logs/error.log \
	    --log-level info
