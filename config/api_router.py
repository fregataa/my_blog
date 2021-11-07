from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from my_blog.users.api.views import UserViewSet, UserCreateView
from my_blog.articles.api.views import (
    ArticleViewSet,
    CommentViewSet,
    RecommentViewSet,
    TagViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("articles", ArticleViewSet)
router.register("comments", CommentViewSet)
router.register("recomments", RecommentViewSet)
router.register("tags", TagViewSet)


app_name = "api"
urlpatterns = router.urls + [
    path("users-create", view=UserCreateView.as_view(), name="usercreate"),
]
