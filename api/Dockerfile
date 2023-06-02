# Установка базового образа Python
FROM python:3.8-alpine

ENV PYTHONPATH=${PYTHONPATH}:/app

# Рабочая папка
WORKDIR /app
# скачиваем всен необходимое для пострегса
RUN apk update \
        && apk add --no-cache gcc make libc-dev \
        postgresql-dev python3-dev build-base \
        linux-headers pcre-dev jpeg-dev zlib-dev \
        freetype-dev lcms2-dev openjpeg-dev tiff-dev \
        tk-dev tcl-dev curl musl-dev libffi-dev openssl-dev cargo

ENV PYTHONUNBUFFERED 1


# Установка зависимостей проекта
COPY requirements.txt /app/
RUN pip install -r requirements.txt


# Копирование кода проекта в контейнер
COPY . /app/

# Запуск команды для миграции базы данных и запуска приложения
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]