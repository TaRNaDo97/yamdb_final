import datetime

from django.core.exceptions import ValidationError


def validate_year(value):

    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(f'{value} has not yet arrived')
    if value < 1:
        raise ValidationError(f'Year must be positive! ({value})')
