from api.pagination import CustomPagination
from rest_framework import viewsets
from users.serializers import CustomUserSerializer

from users.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсэт Юзер"""
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination
    serializer_class = CustomUserSerializer
