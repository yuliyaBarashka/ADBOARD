# AdBoard — Доска объявлений

Backend-часть для сайта объявлений: CRUD, отзывы, роли, JWT, поиск.

## Стек

- Python 3.12, Django 5, DRF
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

### Автор:
Юлия Тихонова