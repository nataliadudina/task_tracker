from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ExperienceValidator:
    """ Проверяет корректность ввода данных в графе 'стаж' """

    def __call__(self, value):
        if value < 0 or value > 70:
            raise ValidationError(_('Experience must be between 0 and 70.'), code='experience_error')


class NameValidator:
    """ Проверяет корректность ввода имени """

    def __call__(self, value):
        # Проверка, что значение содержит только буквы и дефисы
        if not all(c.isalpha() or c == '-' for c in value):
            raise ValidationError(_('Names must contain only letters and hyphens.'), code='name_error')

        # Проверка, что дефис не является первым или последним символом
        if value.startswith('-') or value.endswith('-'):
            raise ValidationError(_('Names cannot start or end with a hyphen.'), code='name_error')

        # Проверка, что в имени нет двух дефисов подряд
        if '--' in value:
            raise ValidationError(_('Names cannot contain consecutive hyphens.'), code='name_error')
