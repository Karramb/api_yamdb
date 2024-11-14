## Финальный проект 15 спринт:

Проект YaMDb собирает отзывы пользователей на различные произведения.
Вам понравился фильм, книга, хотите поделиться в печатлениями? Добро пожаловать на наш сайт! Здесь вы можите написать всё что вы думае о любом произведение и поставить ему оценку.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Karramb/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Регистрация:
Для регистрации обратитесь к администратору. После подтверждения
Пользователь отправляет POST-запрос на добавление нового регистрации выполните запросы 1 и 2 из примеров ниже.

### Примеры запросов:
1. Пример POST-запроса на получение кода подтверждения на электронную почту:
POST .../api/v1/auth/signup/
...
{
"email": "user@example.com",
"username": "^w\\Z"
}
...

2. Получение JWT-токена в обмен на username и confirmation code.
POST .../api/v1/auth/token/
...
{
"username": "^w\\Z",
"confirmation_code": "string"
}
...
3. Пример просмотра информации о произведении.
Запрос:

GET .../api/v1/titles/41/

Пример ответа:
...
{
    "id": 41,
    "name": "Очень хороший фильм",
    "year": 2020,
    "rating": 10,
    "description": "Фильм снят самым известным режиссёром самой известной студией. Снимались самые известнве актёры. Смотрите всёй семьёй.",
    "genre": [
        {
        "name": "для семейного просмотра",
        "slug": "forfamile"}
        ],
    "category": {
        "name": "фильм",
        "slug": "film"
        }
}

4. Пример добавления нового комментария для отзыва.
POST .../api/v1/titles/30/reviews/10/comments/

...
{
"text": "Книга очень понравилась, прочитал залпом. Всем советую!"
}
...

Пример ответа:
...
{
"id": 15,
"text": "Книга очень понравилась, прочитал залпом. Всем советую!",
"author": "username",
"pub_date": "2024-08-24T14:15:22Z"
}
...

### Команда разработки:
Самое ответсвенное лицо: Анатолий Пономарев (управление пользователями)
Кирилл Гизатулин (отзывы, комментарии, рейтинг произведений)
Наталья Козарезенко (модели, view и эндпойнты для произведений,категорий, жанров)