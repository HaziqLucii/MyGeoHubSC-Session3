build :
	docker compose up --build -d

dev:
	docker compose up -d

down:
	docker compose down

seed:
	docker compose exec app python app/seed.py

# untuk debug
path:
	docker compose exec app python -c "import sys; print(sys.path)"

pwd :
	docker compose exec app pwd
