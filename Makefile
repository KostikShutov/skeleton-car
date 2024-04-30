##########
# Docker #
##########

.PHONY: d-up
d-up:
	docker compose up -d

.PHONY: d-down
d-down:
	docker compose down

.PHONY: d-restart
d-restart:
	docker compose restart

.PHONY: d-python
d-python:
	docker compose exec python-picar bash

##########
# Server #
##########

.PHONY: server
server:
	docker compose run --rm -p 2001:5000 -w /code python-picar python server.py

.PHONY: worker
worker:
	docker compose run --rm -w /code python-picar python -m celery -A executor worker --concurrency=1 -l INFO
