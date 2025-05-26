[![Build Status](https://travis-ci.com/katyaaa86/exchanger.svg?branch=main)](https://travis-ci.com/katyaaa86/exchanger)

# Платформа для обмена вещами (бартерная система)

Это монолитное веб-приложение на Django для организации
обмена вещами между пользователями. Пользователи могут размещать объявления о
товарах для обмена, просматривать чужие (и свои) объявления и отправлять предложения на
обмен. 
Приложение имеет удобный веб-интерфейс и REST API для работы с объявлениями и обменными предложениями.
## Стек технологий

- Python 3.10
- Django 4.2
- Django REST Framework
- SQLite (по умолчанию)
- Pytest

---

## Установка и запуск (локально)

### 1. Клонирование репозитория

```bash
git clone https://github.com/katyaaa86/exchanger.git
```

### 2. Создание и активация виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Настройка переменных окружения (опционально)
Если используется .env, добавьте его в корень проекта (в проекте есть пример .env.example):

```ini
DEBUG=True
SECRET_KEY=ваш_секретный_ключ
```

### 5. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Создание суперпользователя
```bash
python manage.py createsuperuser
```
### 7. Запуск локального сервера
```bash
python manage.py runserver
```
Проект будет доступен по адресу: http://127.0.0.1:8000

## Запуск тестов
Для запуска тестов используется pytest:

```bash
pytest
```

Основная страница доступна по адресу: /ads

Авторизация через admin-панель
