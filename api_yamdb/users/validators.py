import re
from django.core.exceptions import ValidationError


def username_validate(username):
    if username == "me":
        raise ValidationError(
            "Нельзя использовать имя me")
    example = r'^[\w.@+-]+\Z'
    if not re.match(example, username):
        invalid_chars = re.sub(example, '', username)
        raise ValidationError(
            'Введите корректный ник. '
            f'Подобные символы недопустимы: {invalid_chars}'
        )
