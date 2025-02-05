# Переменные
PROJECT_NAME = randomcoffee_bot

# Цели (targets)

# Собрать Docker-образ
build:
    docker-compose build

# Запустить контейнер в фоновом режиме
up:
    docker-compose up -d

# Остановить контейнер
down:
    docker-compose down

# Просмотреть логи контейнера
logs:
    docker logs $(PROJECT_NAME)

# Просмотреть статус контейнера
status:
    docker ps

# Пересобрать и перезапустить контейнер
rebuild: down build up

# Очистить все Docker-ресурсы (контейнеры, образы, сети)
clean:
    docker-compose down --rmi all --volumes --remove-orphans

# Помощь
help:
    @echo "Доступные команды:"
    @echo "  make build   - Собрать Docker-образ"
    @echo "  make up      - Запустить контейнер"
    @echo "  make down    - Остановить контейнер"
    @echo "  make logs    - Просмотреть логи"
    @echo "  make status  - Проверить статус контейнера"
    @echo "  make rebuild - Пересобрать и перезапустить контейнер"
    @echo "  make clean   - Очистить все Docker-ресурсы"
    @echo "  make help    - Показать эту справку"