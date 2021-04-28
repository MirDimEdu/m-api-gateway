# m-api-proxy
Сервис для проксирования трафика в тестовую систему на основе микросервисов

# Установка
1) Создать и активировать venv 
2) Установить все зависимости из requirements.txt.

# Запуск
    uvicorn api-gateway:app

# Конфигурация
В файле config.yaml указать пути назначения для роутов.
Параметры 
- `auth_required` означает, что для доступа к ручке пользователь должен быть авторизован.
- `allow_methods` список разрешенных HTTP методов, если массив пустой - разрешены все методы.
- `prefix` префикс роута, если запрошенный путь начинается в этого префикса, данная запись будет использована для роутинга.
- `destination` адрес сервиса в который нужно направить трафик