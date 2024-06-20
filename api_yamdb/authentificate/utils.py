from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


def create_confirmation_code(user):
    token = default_token_generator.make_token(user)
    return token


def send_confirmation_email(user, confirmation_code):
    send_mail(
        'Код подтверждения',
        f'Ваш код: {confirmation_code}',
        'Yamdb@yandex.ru',
        [user.email],
        fail_silently=False,
    )
