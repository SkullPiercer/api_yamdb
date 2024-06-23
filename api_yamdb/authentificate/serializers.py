from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .utils import check_confirmation_code, validate_username


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя при регистрации."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = User.objects.filter(username=data['username']).exists()
        email = User.objects.filter(email=data['email']).exists()

        if username and not email:
            raise serializers.ValidationError('Неверно введена почта')

        elif not username and email:
            raise serializers.ValidationError('Username занят')

        return data

    def validate_username(self, value):
        validate_username(value)
        return value


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор проверки кода подтверждения."""
    confirmation_code = serializers.CharField(max_length=250, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not check_confirmation_code(user, code):
            raise serializers.ValidationError('Неверный код подтверждения')

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя при работа админа."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        request = self.context.get('request', None)
        user = self.instance
        if request and request.method == 'PATCH':
            username = data.get('username', user.username)
            email = data.get('email', user.email)
        else:
            username = data.get('username', '')
            email = data.get('email', '')

        validate_username(username)

        if (User.objects.filter(username=username).exists() 
                and self.instance.username != username):
            raise serializers.ValidationError('Имя пользователя занято')

        if (User.objects.filter(email=email).exists() 
                and self.instance.email != email):
            raise serializers.ValidationError('Email занят')

        return data


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя при получении
    данных о своем аккаунте."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        validate_username(value)
