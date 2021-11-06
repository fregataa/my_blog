from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from my_blog.users.api.views import UserViewSet, UserCreateViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("users-create", UserCreateViewSet, basename="usercreate")


app_name = "api"
urlpatterns = router.urls
