from api.pagination import CustomPagination
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
    """Вьюсэт Юзер"""
    pagination_class = CustomPagination
