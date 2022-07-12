from rest_framework import routers

from django.urls import include, path

from api.views import TagViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
