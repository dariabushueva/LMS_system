# Проект LMS система
В проекте на основе Django REST framework реализована платформа для онлайн-обучения, в которой каждый желающий может размещать свои полезные материалы или курсы. 

# Запуск LMS system
## 1. Клонирование репозитория
```commandline
git clone https://github.com/dariabushueva/LMS_system.git
```
## 2. Установка зависимостей
Создать виртуальное окружение:
```commandline
python -m venv venv
```
Активировать виртуальное окружение:
```commandline
venv\Scripts\activate.bat  для Windows
source venv/bin/activate  для Linux и MacOS
```
Установить зависимости:
```commandline
pip install -r requirements.txt
```

## 3. Установка и запуск Redis
Установка:
```commandline
sudo apt-get install redis-server
```
Запуск:
```commandline
sudo service redis-server start
```

## 4. Установка и настройка PostgreSQL
Установка:
```commandline
sudo apt-get install postgresql
```
Запуск:
```commandline
psql -U postgres
```
Создание базы данных, где lms_system - название базы данных, которое можно изменить в файле .env
```commandline
CREATE DATABASE lms_system;
```
Закрыть PostgreSQL:
```commandline
\q
```

## 5. Подключение Stripe
Подключить возможность оплаты курсов через:
Пройти простую регистрацию по адресу ниже и получить API-ключи, публичный и секретный
```commandline
https://dashboard.stripe.com/register
```

## 6. Настройка переменных окружения
В папке config/ создать файл .env, в который записать свои данные:
```commandline
SECRET_KEY=
PSQL_DB_NAME=lms_system
PSQL_USER=
PSQL_PASSWORD=
STRIPE_SECRET_KEY=
STRIPE_PUBLIC_KEY=
EMAIL_PORT=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

## 7. Применение миграций
```commandline
python manage.py migrate
```

## 8. Наполнение базы данных. Все данные предоставлены только в качестве примера.
```commandline
python manage.py loaddata data.json
```

## 9. Запуск сервера Django
```commandline
python manage.py runserver
```

## 10. Запуск сервиса периодических задач CELERY осуществляется в разных терминалах двумя командами
```commandline
python.exe -m celery -A config worker -l INFO -P eventlet 
celery -A config beat -l INFO -S django  
```

## 11. Запустить проект можно с помощью Docker, используя следующую команду:
```commandline
docker-compose build --no-cache && docker-compose up
```

