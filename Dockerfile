# Используем официальный образ Python в качестве базового образа
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/beeline
# Копируем файл requirements.txt внутрь контейнера
COPY requirements.txt ./
# Устанавливаем зависимости, описанные в файле requirements.txt
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/beeline