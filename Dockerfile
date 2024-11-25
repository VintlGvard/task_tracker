FROM python:3.12

RUN mkdir /task_tracker

WORKDIR /task_tracker

RUN poetry install

RUN poetry run python manage.py runserver
