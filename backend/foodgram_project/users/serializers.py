from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers

from users.models import CustomUser
from recipes.models import Follow


class CustomUserSerializer(serializers.ModelSerializer):
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
        user = self.context.get('request')
        return Follow.objects.filter(user=user, author=obj.id).exists()
