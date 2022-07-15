from api.pagination import CustomPagination
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
    """Вьюсэт Юзер
    Получение списка юзеров / 
    конкретного юзера / 
    создание, обновление / 
    удаление конкретного юзера /
    изменение пароля /
    получение текущего юзера
    """
    pagination_class = CustomPagination
