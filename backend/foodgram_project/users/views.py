from api.pagination import CustomPagination
from djoser.views import UserViewSet

from drf_yasg.utils import swagger_auto_schema


class CustomUserViewSet(UserViewSet):
    """Вьюсэт Юзер"""#
    paginations_class = CustomPagination


    #@swagger_auto_schema(responses={status.HTTP_200_OK: UserGetSerializer()},
    #                    operation_summary='Получение списка юзеров')
    #def list(self, request):
    #    queryset = User.objects.all()
    #    serializer = UserGetSerializer(queryset, many=True)
    #    return Response(serializer.data)
#
    #@swagger_auto_schema(responses={status.HTTP_200_OK: UserGetSerializer()},
    #                                operation_summary='Получение юзера по id')
    #def retrieve(self, request, pk=None):
    #    queryset = User.objects.all()
    #    user = get_object_or_404(queryset, pk=pk)
     #   serializer = UserGetSerializer(user)
    #    return Response(serializer.data)
#
   # @swagger_auto_schema(request_body=UserSignUpSerializer(),
    #                    operation_summary='Создание юзера')
    #def create(self, request):
     #   serializer = UserSignUpSerializer(data=request.data)
     #   if serializer.is_valid(raise_exception=True):
     #       serializer.save()
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
