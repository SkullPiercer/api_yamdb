import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

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
