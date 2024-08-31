# Заметки REST API

Этот проект представляет собой REST API сервис для управления заметками пользователей. Сервис позволяет добавлять заметки и выводить список заметок, при этом проверяя орфографические ошибки с помощью сервиса Yandex Speller. Данные хранятся в формате JSON в текстовом файле.

## Требования

- Python 3.9 и выше
- Docker

## Установка и запуск

1. **Клонируйте репозиторий:**

   ```
   git clone git@github.com:Katerina-Alekseenko/note_service.git
   cd notes-api
   ```

2. Установите и активируйте виртуальное окружение:
    ```
    python -m venv venv
    source venv/Scripts/activate  - для Windows
    source venv/bin/activate - для Linux
    ```

3. Установите зависимости:
    ```
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Соберите и запустите Docker контейнеры:
    ```
    sudo docker-compose up --build
    ```
## Аутентификация
Пользователи имеют доступ только к своим заметкам. Предустановленный набор пользователей хранится в коде (hardcoded).

## Интеграция с Yandex Speller
При добавлении заметки происходит проверка орфографических ошибок с использованием сервиса Yandex Speller.

## Форматирование кода
Используется black для автоматизированного форматирования исходного кода.

## Тестирование
Для проверки работоспособности методов API можно использовать следующие curl запросы:

5. Примеры запросов:

Добавление заметки:

    ```sh
    curl -X POST "http://localhost:8000/notes/" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "user_id": 1, "content": "This is a test note"}' \
     --user user1:password1
    ```

Вывод списка заметок:

    ```sh
    curl "http://localhost:8000/notes/" \
     --user user1:password1
    ```

6. Запуск тестов с помощью pytest:
    ```
    pytest tests/
    ```
