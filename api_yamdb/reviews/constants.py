from reviews.models import (Category, Comments, Genre, TitleGenre,
                            Review, Title)
from users.models import CustomUser

MODELS_DICT = {
    'category': Category,
    'comments': Comments,
    'genre_title': TitleGenre,
    'genre': Genre,
    'reviews': Review,
    'title': Title,
    'user': CustomUser,
}
