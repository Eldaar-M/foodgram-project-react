![workflow](https://github.com/Eldaar-M/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Описание проекта Foodgram

Kittygram — сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Технологии

- Python 3.x
- node.js 9.x.x
- frontend: React
- backend: Django
- nginx
- gunicorn

## Клонирование проекта с GitHub на сервер:
```
git clone git@github.com:Eldaar-M/foodgram-project-react.git
```
 
## Автор 
- Backend и DevOps: Эльдар Магомедов

### Запуск проекта локально
- В директории /infra создайте файл .env, с переменными окружения:
```bash
SECRET_KEY=<ваш_секретный_ключ>
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD=<ваш_пароль>
DB_HOST='db'
DB_PORT=5432
```
- Сборка и развертывание контейнеров
```bash
docker-compose up -d --build
```
- Миграции, статика выполняются автоматически. Создайте суперпользователя
```bash
docker-compose exec backend python manage.py createsuperuser
```
- Наполните базу данных ингредиентами и тегами
```bash
docker-compose exec backend python manage.py load_ingredients_csv
docker-compose exec backend python manage.py load_tags_csv
```
- Стандартная админ-панель Django доступна по адресу [`http://localhost/admin/`](http://localhost/admin/)
- Документация к проекту доступна по адресу [`http://localhost/api/docs/`](`http://localhost/api/docs/`)

### Запуск API проекта в dev-режиме

- Клонирование удаленного репозитория (см. выше)
- Создание виртуального окружения и установка зависимостей
```bash
cd backend
python -m venv venv
. venv/Scripts/activate (windows)
. venv/bin/activate (linux)
pip install -r -requirements.txt
```
- Примените миграции и соберите статику
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```
- Наполнение базы данных ингредиентами
```bash
python manage.py load_ingredients_csv
```
- Запуск сервера
```bash
python manage.py runserver 
```
