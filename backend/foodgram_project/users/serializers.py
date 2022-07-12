from rest_framework.serializers import SerializerMethodField
from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import User
from recipes.models import Follow


class CustomUserSerializer(UserSerializer):
    """Сериализатор для получения списка юзеров и конкретного юзера"""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = ('id', 'is_subscribed')
    
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания юзера"""

    class Meta(UserCreateSerializer):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
    
    write_only_fields = ('password',)
    read_only_fields = ('id',)
