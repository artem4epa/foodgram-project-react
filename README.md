# Проект Foodgram  

Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.  

## Технологии:  
Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL, Yandex Cloud, Continuous Integration, Continuous Deployment

## Разворачивание проекта на удаленном сервере:  
* Клонировать репозиторий:  
```
git clone git@github.com:artem4epa/foodgram-project-react.git
```
* Установить на сервер Docker, Docker Compose:
```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
``` 
* Скопировать на сервер файлы docker_compose.yml, nginx из директории infra:

```
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
# IP - публичный IP сервера
```  

* Добавить переменные окружения в раздел Secrets>Actions:
```
 SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```
* Создать и запустить контейнеры Docker:
```
sudo docker compose up -d
```
* После сборки выполнить миграции создать суперпользователя, собрать статику, наполнить базу данных из файла ingredients.json:
```
sudo docker exec -it app bash # зайти в контейнер
python manage.py migrate # выполнить миграции
python manage.py collectstatic --noinput # собрать статику
python manage.py loaddata ingredients.json
```

## После обновления репозитория в ветку master будет происходить:
* Проверка кода на соответствие стандарту PEP 8
* Сборка и доставка докер образов на Docker HUB
* Разворачивание проекта на удаленном сервере
* Отправка сообщения в Telegram в случае успешного завершения операции



### Автор бэкенда: 
@artem4epa

Данные для тестирования

host: http://62.84.118.248
login: admin
password: admin
