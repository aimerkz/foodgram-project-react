# Foodgram Project

![example workflow](https://github.com/aimerkz/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Stack Overflow](https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)


Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

## _Запуск_:
 - Клонируйте репозиторий на свою локальную машину:
```sh
https://github.com/aimerkz/foodgram-project-react.git
cd infra
```
 - Cоздайте в папке /infra файл .env и заполните его переменными окружения:
```sh
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем c postgresql

DB_NAME=postgres # имя базы данных

POSTGRES_USER=postgres # логин для подключения к базе данных

POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)

DB_HOST=db # название сервиса (контейнера)

DB_PORT=5432 # порт для подключения к БД

SECRET_KEY=ваш секретный ключ
```
- Находясь в папке /infra, запустите сборку образа Docker:
```sh
docker-compose up -d
```
- Выполните миграции:
```sh
docker-compose exec backend python manage.py migrate
```

- Создайте суперпользователя:
```sh
docker-compose exec backend python manage.py createsuperuser
```
- Выполните команду collectstatic:
```sh
docker-compose exec backend python manage.py collectstatic --no-input
```
- Заполните базу тестовыми данными:
```sh
docker-compose exec backend python manage.py loaddata fixtures.json
```
- Перейдите по адресу:
```sh
http://158.160.0.181/
```
