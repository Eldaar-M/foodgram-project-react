import re

from django.core.exceptions import ValidationError


def validate_username(value):
    invalid_characters = re.sub(r'^[\w.@+-]+|\Z', '', value)
    if invalid_characters:
        invalid_characters = set(invalid_characters)
        invalid_characters = list(invalid_characters)
        raise ValidationError(
            f'Введены недопустимые символы:: {invalid_characters}'
        )
