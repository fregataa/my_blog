from django.db.models import Q
from rest_framework import status, generics, serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import (
    ArticleSerializer,
    CommentSerializer,
    RecommentSerializer,
    TagSerializer,
)
from ..models import Article, Comment, Recomment, Tag
from .permissions import IsWriterOrReadOnly


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsWriterOrReadOnly]

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
    permission_classes = [IsWriterOrReadOnly]

    def perform_create(self, serializer):
        data = self.request.data
        if "article" not in data:
            raise serializers.ValidationError("`article` field is required.")
        serializer.save(
            article=Article.objects.get(id=data["article"]), writer=self.request.user
        )


class RecommentViewSet(ModelViewSet):
    serializer_class = RecommentSerializer
    queryset = Recomment.objects.all()
    permission_classes = [IsWriterOrReadOnly]

    def perform_create(self, serializer):
        data = self.request.data
        if "comment" not in data:
            raise serializers.ValidationError("`comment` field is required.")
        serializer.save(
            comment=Comment.objects.get(id=data["comment"]), writer=self.request.user
        )


class TagView(generics.RetrieveAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
