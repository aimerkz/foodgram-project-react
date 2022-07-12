from rest_framework import serializers

from recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тег"""
    class Meta:
        model = Tag
        fields = '__all__'