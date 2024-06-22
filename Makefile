DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = app
STORAGES_FILE = docker_compose/storages.yaml
DB_CONTAINER = database
WORKERS_FILE = docker_compose/workers.yaml
WORKER_CONTAINER = celery-worker
MONGO = docker_compose/mongo.yaml
MONGO_EXPRESS = docker_compose/mongo-express.yaml


.PHONY: mongo
mongo:
	${DC} -f ${MONGO} ${ENV} up -d --build

.PHONY: ui
ui:
	${DC} -f ${MONGO_EXPRESS} ${ENV} up --build -d

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down


.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: all
all:
	${DC} -f ${APP_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} -f ${WORKERS_FILE} ${ENV} up --build -d

.PHONY: workers
workers:
	${DC} -f ${WORKERS_FILE} ${ENV} up --build -d


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: worker-logs
worker-logs:
	${LOGS} ${WORKER_CONTAINER} -f

.PHONY: down
down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${WORKERS_FILE} down --remove-orphans

.PHONY: db-logs
db-logs:
	${DC} -f ${STORAGES_FILE} logs -f

.PHONY: clear
clear:
	docker images --filter "dangling=true" -q | xargs docker rmi


.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONY: tests
tests:
	${EXEC} ${APP_CONTAINER} pytest