## Сервис авторизации

### Запуск во внутренней сети
```bash
docker network create mysibsau # создание сети, если еще не создана
docker compose up -d
```

### Запуск во внешней сети
```bash
docker compose -f docker-compose.local.yml up -d
```