## Финальный проект 15 спринт:  Проект YaMDb

Проект YaMDb собирает отзывы пользователей на различные произведения.
Вам понравился фильм, книга, хотите поделиться в печатлениями? Добро пожаловать на наш сайт! Здесь вы можите написать всё что вы думаете о любом произведении и поставить ему оценку.

### Использованный стек технологий:
- Python
- Django
- django-filter
- djangorestframework
- PyJWT
- pytest
- pytest-django
- pytest-pythonpath
- djangorestframework-simplejwt

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Karramb/api_yamdb.git

cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env

source env/bin/activate
```

По необходимости установить/обновить пакетный менеджер pip:

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

#### Загрузить данные из csv-файлов:
Разместите csv-файлы в каталоге "api_yamdb\static\data\" или измените путь "PATH_FOR_CSV" к каталогу в файле "api_yamdb\api_yamdb\settings.py"

В каталоге с файлом "manage.py" запустить скрипт командой:

```
python manage.py csv_loader
```
После загрузки выведется сообщение: "Загрузка завершена!"

Запустить проект:

```
python3 manage.py runserver
```
### Регистрация:
Для регистрации обратитесь к администратору. После подтверждения пользователь отправляет POST-запрос на получение кода подтвержденеия и получение JWT-токена (выполните запросы 1 и 2 из примеров ниже).

### Примеры запросов:
Полную документацию смотрите по ссылке: http://127.0.0.1:8000/redoc/

1. Пример POST-запроса на получение кода подтверждения на электронную почту:
   
POST .../api/v1/auth/signup/

```
{
"email": "user@example.com",
"username": "^w\\Z"
}
```

2. Получение JWT-токена в обмен на username и confirmation code.
   
POST .../api/v1/auth/token/

```
{
"username": "^w\\Z",
"confirmation_code": "string"
}
```
3. Пример просмотра информации о произведении.
   
Запрос:

GET .../api/v1/titles/41/

Пример ответа:

```
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
```
4. Пример добавления нового комментария для отзыва.
   
POST .../api/v1/titles/30/reviews/10/comments/

```
{
"text": "Книга очень понравилась, прочитал залпом. Всем советую!"
}

```

Пример ответа:

```
{
"id": 15,
"text": "Книга очень понравилась, прочитал залпом. Всем советую!",
"author": "username",
"pub_date": "2024-08-24T14:15:22Z"
}

```

### Команда разработки:
Самое ответственное лицо: [Анатолий Пономарев](https://github.com/Karramb) (управление пользователями)

[Кирилл Гизатулин](https://github.com/KirillGizatulin) (отзывы, комментарии, рейтинг произведений, csv импорт)

[Наталья Козарезенко](https://github.com/NatalyaKozarezenko/) (модели, view и эндпойнты для произведений, категорий, жанров, админка)
