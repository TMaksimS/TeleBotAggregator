up_db:
	docker compose -f docker-compose-local.yaml up -d
depends: up_db
	python3 depends.py
up_local: depends
	python3 main.py
down_local:
	docker compose -f docker-compose-local.yaml down --remove-orphans

up_ci:
	docker compose -f docker-compose-ci.yaml up -d
down_ci:
	docker compose -f docker-compose-ci.yaml down --remove-orphans && docker rmi teleapp
