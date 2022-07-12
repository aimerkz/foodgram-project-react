from api.serializers import TagSerializer
from recipes.models import Tag

from rest_framework import viewsets, status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(responses={status.HTTP_200_OK: TagSerializer()})
class TagViewSet(viewsets.ViewSet):
    """Вьюсэт Тег"""
    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)
