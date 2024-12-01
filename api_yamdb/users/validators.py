import re

from django.core.exceptions import ValidationError

from api_yamdb.settings import RESERVED_NAME


def validate_username(username):
    if username == RESERVED_NAME:
        raise ValidationError(
            f'Нельзя использовать имя {RESERVED_NAME}')
    example = r'^[\w.@+-]+\Z'
    invalid_chars = ''
    for i in set(username):
        x = re.sub(example, '', i)
        invalid_chars += x
    if invalid_chars:
        raise ValidationError(
            f'Данные символы недопустимы: {invalid_chars}'
        )
    return username
