from rest_framework import serializers

from users.api.serializers import UserSerializer
from ..models import Article, Comment, Recomment, Tag

comment_serializer_fields = ["pk", "writer", "content"]


class GenericRecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = comment_serializer_fields


class GenericCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = comment_serializer_fields


class RecommentSerializer(GenericRecommentSerializer):
    article = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="api:article-detail"
    )
    comment = GenericCommentSerializer(read_only=True)

    class Meta:
        model = Recomment
        fields = [*comment_serializer_fields, "article", "comment"]


class CommentSerializer(GenericCommentSerializer):
    article = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="api:article-detail"
    )
    recomments = GenericRecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [*comment_serializer_fields, "article", "recomments"]


article_serializer_fields = [
    "pk",
    "title",
    "writer",
    "content",
    "is_published",
    "url",
]


class GenericArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = article_serializer_fields
        read_only_fields = ["liking_users"]

        extra_kwargs = {"url": {"view_name": "api:article-detail"}}


class TinyArticleSerializer(GenericArticleSerializer):
    def to_representation(self, instance):
        """Since this serializer is used by TagSerializer,
        articles not published should not be returned.
        """

        if not instance.is_published:
            return None
        return super().to_representation(instance)


class TagSerializer(serializers.ModelSerializer):
    used_articles = TinyArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ["pk", "name", "used_articles"]


class ArticleSerializer(GenericArticleSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liking_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [*article_serializer_fields, "tags", "comments", "liking_users"]

        extra_kwargs = {"url": {"view_name": "api:article-detail"}}
