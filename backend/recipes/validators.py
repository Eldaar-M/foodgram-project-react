import re

from rest_framework.validators import ValidationError


def validate_username(value):
    invalid_characters = ''
    invalid_characters.join(re.split(r'[\w]|[.]|[@]|[+]|[-]+$', value))

    if len(invalid_characters) != 0:
        raise ValidationError(
            f"Введены недопустимые символы: {invalid_characters}"
        )
