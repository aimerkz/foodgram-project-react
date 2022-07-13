from rest_framework.serializers import SerializerMethodField
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import CustomUser
from recipes.models import Follow


class CustomUserSerializer(UserSerializer):
    """Сериализатор для получения списка юзеров и конкретного юзера"""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        read_only_fields = ('id', 'is_subscribed')
        extra_kwargs = {"password": {'write_only': True}}
    
    def get_is_subscribed(self, obj):
        """Метод для проверки подписки пользователя"""
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return Follow.objects.filter(id=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания юзера"""
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
