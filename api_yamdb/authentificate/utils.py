import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


User = get_user_model()


def create_confirmation_code(user):
    """Создание кода подтверждения."""
    return default_token_generator.make_token(user)


def send_confirmation_email(user, confirmation_code):
    """Отправка кода подтверждения."""
    send_mail(
        'Код подтверждения',
        f'Ваш код: {confirmation_code}',
        settings.DOMAIN_NAME,
        [user.email],
        fail_silently=False,
    )


def check_confirmation_code(user, token):
    """Проверка кода подтверждения."""
    return default_token_generator.check_token(user, token)


def validate_username(value):
    """Проверка username на валидность."""
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError("Некорректное имя пользователя!")
    if value == 'me':
        raise ValidationError('Не используйте никнейм `me`!')
    return value
