# Nome do serviço no docker-compose.yml
SERVICE=app

# Comando para iniciar os serviços
up:
	docker-compose up -d

# Comando para rodar alembic upgrade head
upgrade:
	docker-compose run --rm $(SERVICE) alembic upgrade head

test:
	docker-compose run --rm $(SERVICE) pytest

# Comando para parar os serviços
down:
	docker-compose down

# Comando para reiniciar os serviços
restart: down up

# Limpar os volumes (útil para resetar os dados do MongoDB)
clean:
	docker-compose down --volumes
