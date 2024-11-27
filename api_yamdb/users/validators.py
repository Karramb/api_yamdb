import re

from django.core.exceptions import ValidationError
from itertools import groupby

from users.constants import ME


def username_validate(username):
    if username == ME:
        raise ValidationError(
            'Нельзя использовать имя me')
    example = r'^[\w.@+-]+\Z'
    invalid_chars = re.sub(example, '', username)
    if invalid_chars:
        invalid_chars = ''.join(k for k, g in groupby(invalid_chars))
        raise ValidationError(
            f'Подобные символы недопустимы: {invalid_chars}'
        )
    return username
