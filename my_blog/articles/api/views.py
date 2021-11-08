from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status, serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    ArticleSerializer,
    CommentSerializer,
    RecommentSerializer,
    TagSerializer,
)
from ..models import Article, Comment, Recomment, Tag
from .permissions import IsWriterOrReadOnly, ReadOnly


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsWriterOrReadOnly]

    def get_queryset(self):
        """Returns user's articles or all published articles."""

        return self.queryset.filter(Q(writer=self.request.user) | Q(is_published=True))

    def perform_create(self, serializer):
        """Patches writer field and tags field of created article."""

        article = serializer.save(writer=self.request.user)
        tags = self.request.data.get("tags")
        tag_list = []
        if tags is not None and len(tags) > 0:
            tag_list = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
            article.tags.add(*tag_list)

    @action(detail=True, methods=["PATCH"])
    def publish(self, request, pk):
        """Patches is_published field to True.
        Do nothing if the article has already been published.
        """

        _ = request
        article = self.queryset.get(pk=pk)
        if article.is_published:
            return Response(status=status.HTTP_204_NO_CONTENT)
        article.is_published = True
        article.save(update_fields=["is_published"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["PUT"])
    def like(self, request, pk):
        """Adds like field of article.
        Only authenticated users can ``like`` any articles.
        """

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        article = self.queryset.get(pk=pk)
        article.liking_users.add(request.user)
        serializer = ArticleSerializer(article, context={"request": request})
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsWriterOrReadOnly]

    def perform_create(self, serializer):
        """Patches article field of created comment."""

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
        """Patches comment field of created recomment."""

        data = self.request.data
        if "comment" not in data:
            raise serializers.ValidationError("`comment` field is required.")
        serializer.save(
            comment=Comment.objects.get(id=data["comment"]), writer=self.request.user
        )


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [ReadOnly]

    def list(self, request):
        serializer = TagSerializer(
            self.queryset, context={"request": request}, many=True
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        tag = get_object_or_404(self.queryset, pk=pk)
        serializer = TagSerializer(tag, context={"request": request})
        return Response(serializer.data)
