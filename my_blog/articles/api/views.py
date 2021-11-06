from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ArticleSerializer, CommentSerializer, RecommentSerializer
from ..models import Article, Comment, Recomment, Tag


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        return self.queryset.filter(Q(writer=self.request.user) | Q(is_published=True))

    def perform_create(self, serializer):
        tags = self.request.data.get("tags")
        tag_list = []
        if tags is not None and len(tags) > 0:
            tag_list = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
        article = serializer.save(writer=self.request.user)
        article.tags.add(*tag_list)

    @action(detail=True, methods=["PATCH"])
    def publish(self, request, pk):
        _ = request
        article = self.queryset.get(pk=pk)
        article.is_published = True
        article.save(update_fields=["is_published"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class RecommentViewSet(ModelViewSet):
    serializer_class = RecommentSerializer
    queryset = Recomment.objects.all()
