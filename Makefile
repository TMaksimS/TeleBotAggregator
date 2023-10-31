up_db:
	docker compose -f docker-compose-local.yaml up -d
depends: up_db
	python3 depends.py
down_local:
	docker compose -f docker-compose-local.yaml down --remove-orphans