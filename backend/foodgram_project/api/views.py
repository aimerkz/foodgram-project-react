from api.serializers import TagSerializer
from api.pagination import CustomPagination
from recipes.models import Tag

from rest_framework import viewsets, status

from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(responses={status.HTTP_200_OK: TagSerializer()})
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсэт Тег"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination
