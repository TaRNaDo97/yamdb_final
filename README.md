![YaMDb workflow](https://github.com/TaRNaDo97/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg?branch=master)

# YaMDb
Проект доступен по адресу http://www.yatube.fun/admin/ или http://178.154.202.167/admin/
Проект **YaMDb** собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку

## Запуск приложения
Для запуска проекта используйте следующие команды:
```bash
# Запустить проект
docker-compose up

# Создать скрипты миграции
docker-compose exec web python manage.py makemigrations

# Выполнить миграцию в БД
docker-compose exec web python manage.py migrate
```
После запуска приложения необходимо создать суперпользователя командой:
```bash
docker-compose exec web python manage.py createsuperuser
```
Для загрузки тестовых данных используйте команду:
```bash
docker-compose exec web python manage.py loaddata fixtures.json
```
Для загрузки образа **YaMDb** используйте команду:
```bash
docker pull tarnado1997/yamdb:1.0.0
```

##Используемые технологии

- Язык программирования Python 3.8
- Web-фреймворк Django 3.1
- Контейнеризация Docker
- База данных PostgreSQL
- Веб-сервер Nginx в связке с Gunicorn

##О разработчиках

Александр Агафонов - подсистемы управления отзывами и комментариями, контейнеризация.
[Github](https://github.com/TaRNaDo97) / [Gitlab](https://gitlab.com/agafonovav) / [Email](tarnado97@yandex.ru)

Кирилл Поршнев - подсистема управления пользователями. [Github](https://github.com/RshaBatti)

Сергей Киркач - подсистемы управления категориями, жанрами и произведениями. [Github](https://github.com/di35e1)
