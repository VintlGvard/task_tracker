# Приложение для управления задачами

TaskTracker — это мощная система управления задачами, разработанная для упрощения управления проектами и командного взаимодействия. Приложение предлагает расширенные функции, такие как уведомления в реальном времени, поддержка приоритета задач, фильтрация, сортировка и многое многое другое.

---

## Особенности

### 1. **Управление задачами**
- Создание, обновление и удаление задач.
- Назначение задач конкретным пользователям.
- Добавление и обновление проектов к которым прикреплены задачи

### 2. **Приоритизация задач**
- Назначение уровней приоритета задачам (например, Высокий, Средний, Низкий).
- Сортировка задач по приоритету.

### 3. **Фильтрация и сортировка**
- Фильтрация задач и проектов по пользователю, категории или приоритету.
- Сортировка задач и проектов по сроку выполнения, дате создания или приоритету.

### 4. **Уведомления в реальном времени**
- Мгновенные уведомления об обновлениях задач с использованием WebSocket.
- Будьте в курсе обновлений задач, назначений, завершений и изменений статуса в реальном времени.

### 5. **RESTful API**
- Надежный API для интеграции с сторонними приложениями.
- Конечные точки API для создания, обновления и получения задач.

### 6. **Аутентификация пользователей**
- Безопасный вход и регистрация.
- Контроль доступа на основе ролей.

### 7. **Email уведомления о новых ваших проектах**
- Мгновенные Email-оповещения на почту зарегистрированного пользователя.

---

## Используемые технологии

- **Backend**: Django 5.1.3
- **API Framework**: Django REST Framework
- **База данных**: PostgreSQL (настраиваемая на SQLite или MySQL)
- **Административный интерфейс**: Django Admin
- **Версия Python**: Python 3.12.6

## Структура проекта

```
task_tracker/
├── manage.py
├── task_manager/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── models.py
│   ├── routing.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
├── user/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── projects/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
├── README.md
├── docker.env
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
```

## Начало работы

Следуйте этим шагам, чтобы настроить проект на своем локальном компьютере:

## Начало работы
### 1. Docker

1. Запустите проект в Docker
   ```bash
   docker compose build
   docker compose up
   ```

Перейдите по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).
### 2. Развертывание из исходного кода
##### Предварительные требования
Перед запуском приложения убедитесь, что у вас установлены следующие компоненты:

* Python 3.12.6
* Poetry
* PostgreSQL

##### Установка

1. Установите [Poetry](https://python-poetry.org/docs/#installation)
2. Создайте виртуальное окружение

   ```bash
   poetry install
   ```

#### Использование
### Запуск приложения

Чтобы запустить приложение Django локально, используйте следующую команду:

```bash
cd task_tracker
poetry run python manage.py runserver
```