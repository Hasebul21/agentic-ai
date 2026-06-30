PYTHON = .venv/bin/python
PYTHONPATH = PYTHONPATH=.

.PHONY: run stop seed reset logs

run:
	docker compose up -d
	@echo "Waiting for Postgres to be ready..."
	@until docker exec agentic_ai_db pg_isready -U agentic -q; do sleep 1; done
	@echo "Postgres is ready."
	$(PYTHONPATH) $(PYTHON) main.py

stop:
	docker compose down

seed:
	$(PYTHONPATH) $(PYTHON) db/seed.py

reset:
	docker compose down -v
	docker compose up -d
	@until docker exec agentic_ai_db pg_isready -U agentic -q; do sleep 1; done
	$(PYTHONPATH) .venv/bin/alembic upgrade head
	$(PYTHONPATH) $(PYTHON) db/seed.py

logs:
	docker compose logs -f
