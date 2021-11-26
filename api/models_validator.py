from datetime import datetime

from django.core.exceptions import ValidationError


def year_validator(value: int):
    if value < 1900 or value > datetime.now().year:
        raise ValidationError(
            f'{value} is not a correct year'
        )


def username_validator(value: str):
    if value == 'me':
        raise ValidationError(
            f'username cant be {value} '
        )
