# Template
### Образец (пустой бланк) для запуска приложения на FastApi.
Swagger: http://127.0.0.1:8000/docs
Админка: http://127.0.0.1:8000/admin
В данном образце при первом запуске приложения создается пользователь с ролью админ. Логин и пароль задается в .env в блоке ADMIN USER
### Стек:
* FastApi
* Alembic
* Postgres
* SQLAlchemy
* Sqladmin
### Для развертывания приложения необходимо:
1. Склонировать проект git clone github.com:ваш-аккаунт-на-гитхабе/Template.git
2. В директории src/configs создайте файл .env и заполните его, как .env.template
3. Запустите приложение и бд командой ```docker compose up --build```
