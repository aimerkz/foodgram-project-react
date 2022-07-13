from api.pagination import CustomPagination
from djoser.views import UserViewSet
from users.serializers import CustomUserSerializer

from users.models import CustomUser


class CustomUserViewSet(UserViewSet):
    """Вьюсэт Юзер"""
    pagination_class = CustomPagination
