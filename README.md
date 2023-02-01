# FoodGram ![work's status](https://github.com/nentron/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)
Foodgram - это проект созданный для публикации рецептов, система подписок на авторов, добавльнение рецептов в избранное и для покупок. Он создан на REST API с использованием фронтенда на базе React. 

## ТЕХНОЛОГИИ
- Python 3.7.9
- Django 3.2.16
- DRF 3.14
- Gunicore 20.1.0
- PostgreSQL
- Nginx
- React

## Развертывание проекта из DockerHub:
- 1.Открыть в браузере https://github.com/nentron/foodgram-project-react/
- 2.Скопировать на локальный компьютер, директорию infra и перейдите в нее
- 3.Создать .env и заполнить по образцу:
    ```
       DB_ENGINE=django.db.backends.postgresql
       DB_NAME=postgres
       POSTGRES_USER=postgres
       POSTGRES_PASSWORD=<придумайте пароль>
       DB_HOST=db
       DB_PORT=5432
       SECRET_KEY=<ключ в одинарных ковычках>
    ```
- 4.Запуск проекта командой ```docker-compose up -d```
- 5. Создать суперпользователя ```docker-compose exec web python manage.py createsuperuser``` или использовать (email:sergo@mail.ru, password:dog234)
    
- 6.Сайт-админ http://foodreactor.ddns.net/admin/

## Полезные ссылки:

Ссылка на развернутый проект: [foodgram]

[foodgram]: <http://foodreactor.ddns.net/>
## Авторы проекта
- Nentron

