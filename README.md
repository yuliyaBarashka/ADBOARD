# AdBoard — Доска объявлений

Backend-часть для сайта объявлений: CRUD, отзывы, роли, JWT, поиск.

## Стек

- Python 3.12, Django 6.1.1, Django REST Framework 3.18.1
- PostgreSQL 15
- JWT (simplejwt), CORS, django-filter, drf-spectacular
- Docker, Docker Compose
- pytest, pytest-cov

## Установка

### Локально

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### Docker
```bash
cp .env.sample .env
docker compose up -d --build
```
### Эндпоинты

Метод	URL	Доступ
POST    /api/users/register/  аноним  
POST	/api/users/token/	аноним  
POST	/api/users/reset_password/	аноним  
GET	/api/ads/	все  
POST	/api/ads/	авторизованный  
GET	/api/ads/<id>/	все  
PUT/PATCH/DELETE	/api/ads/<id>/	автор или admin  
GET	/api/reviews/?ad=<id>	все  
POST	/api/reviews/	авторизованный  
GET	/api/docs/swagger/	все  

### Тесты
```bash
pytest --cov=users --cov=ads --cov-report=term-missing
```

## Структура проекта

```text
AdBoard/
├── ads/                    # объявления, отзывы, фильтры и права доступа
│   ├── migrations/         # миграции моделей объявлений и отзывов
│   ├── filters.py          # фильтрация по названию и цене
│   ├── models.py           # модели Ad и Review
│   ├── permissions.py      # права автора и администратора
│   ├── serializers.py      # сериализаторы API
│   ├── tests.py            # тесты объявлений и отзывов
│   └── views.py            # CRUD и фильтрация отзывов
├── users/                  # пользователи, регистрация и восстановление пароля
│   ├── migrations/         # миграции пользовательской модели
│   ├── models.py           # пользователь с авторизацией по email
│   ├── serializers.py      # регистрация и профиль
│   ├── tests.py            # тесты аутентификации и паролей
│   └── views.py            # профиль и восстановление пароля
├── config/                 # настройки, корневые URL, ASGI и WSGI
├── fixtures/               # тестовые данные
├── templates/emails/       # шаблон письма восстановления пароля
├── Dockerfile              # образ Django-приложения
├── docker-compose.yml      # приложение и PostgreSQL
├── requirements.txt        # зафиксированные зависимости
└── manage.py               # команды Django
```

### Автор:
Юлия Тихонова