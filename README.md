[![foodgram workflow](https://github.com/gubaevazat/foodgram-project-react/actions/workflows/foodgram_worflow.yml/badge.svg)](https://github.com/gubaevazat/foodgram-project-react/actions/workflows/foodgram_worflow.yml)





# Проект Foodgram-Продуктовый помощник.



Адрес: http://158.160.67.120/
Админ логин: admin
Админ пароль: foodgram2023
Админ email: admin@admin.com






На сервисе **Foodgram** пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.



После отправки изменений в репозиторий на GitHub, весь проект автоматически разворачивается на сервере, при этом проходит тестирование, отправка образа на DockerHub.







## Использованные технологии







- Python





- Django



- Django REST framework



- Docker


- React



## Установка и запуск проекта





**Установить на сервер приложение Docker и docker-compose последней версии,** для установки обратитесь к документации. Для операций с контейнерами и образами обратитесь к документации Docker.







Клонировать репозиторий: https://github.com/gubaevazat/foodgram-project-react.git







git clone https://github.com/gubaevazat/foodgram-project-react.git





В репозитории установить **secrets** (Settings->Secrets and variables -> Action -> New repository secret) со значениями:









    DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql

    DB_NAME=postgres # имя базы данных

    POSTGRES_USER=postgres # логин для подключения к базе данных

    POSTGRES_PASSWORD=gubaev # пароль для подключения к БД (установите свой)

    DB_HOST=db # название сервиса (контейнера)

    DB_PORT=5432 # порт для подключения к БД

    DEBUG=False # по умолчанию False, для отладки установите в True

    SECRET_KEY='your_secret_key' # ваш SECRET_KEY

    DOCKER_PASSWORD = '****' # ваш пароль на DockerHub

    DOCKER_USERNAME = '****' # имя пользователя на DockerHub

    HOST = <ip-адрес вашего сервера>

    PASSPHRASE = <пароль для подключения по SSH>

    SSH_KEY = <ssh ключ компьютера с доступом к серверу>


Создать на сервере папку foodgram.

    mkdir foodgram

Для запуска проекта нужно сделать commit и push в свой репозиторий, затем надо зайти на сервер в папку foodgram и выполнить команды :

    sudo docker compose exec backend python manage.py migrate
    sudo docker compose exec backend python manage.py collectstatic --no-input
    sudo docker compose exec backend backend manage.py createsuperuser
    sudo docker compose exec backend backend manage.py json_import

При последующих обновлениях проекта, указанные выше команды выполнять не нужно.




## Документация API:

    server_ip/api/docs/

  ## Административная панель:

    server_ip/admin/




Автор: Азат.