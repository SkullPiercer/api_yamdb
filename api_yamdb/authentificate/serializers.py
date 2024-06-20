import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .utils import check_confirmation_code

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
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
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('Некорректное имя пользователя.')

        if value == 'me':
            raise serializers.ValidationError('Не используйте никнейм `me`!')
        return value


class TokenSerializer(serializers.ModelSerializer):
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
