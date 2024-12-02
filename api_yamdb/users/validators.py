import re

from django.core.exceptions import ValidationError

from api_yamdb.settings import RESERVED_NAME
from users.constants import EXAMPLE


def validate_username(username):
    if username == RESERVED_NAME:
        raise ValidationError(
            f'Нельзя использовать имя {RESERVED_NAME}')
    invalid_chars = re.findall(EXAMPLE, username)
    if invalid_chars:
        raise ValidationError(
            f'Данные символы недопустимы: {invalid_chars}'
        )
    return username
