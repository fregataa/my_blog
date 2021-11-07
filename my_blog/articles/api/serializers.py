from rest_framework import serializers

from ..models import Article, Comment, Recomment, Tag

comment_serializer_fields = ["pk", "article", "writer", "content"]


class GenericCommentSerializer(serializers.ModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="api:article-detail"
    )

    class Meta:
        model = Comment
        fields = comment_serializer_fields


class RecommentSerializer(serializers.ModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="api:article-detail"
    )
    comment = GenericCommentSerializer(read_only=True)

    class Meta:
        model = Recomment
        fields = [*comment_serializer_fields, "comment"]


class CommentSerializer(GenericCommentSerializer):
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["pk", "article", "writer", "content", "recomments"]


article_serializer_fields = [
    "pk",
    "title",
    "writer",
    "content",
    "is_published",
    "liking_users",
    "comments",
    "url",
]


class GenericArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = article_serializer_fields
        read_only_fields = ["pk", "liking_users"]

        extra_kwargs = {"url": {"view_name": "api:article-detail"}}


class TagSerializer(serializers.ModelSerializer):
    used_articles = GenericArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ["pk", "name", "used_articles"]


class ArticleSerializer(GenericArticleSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [*article_serializer_fields, "tags"]
        read_only_fields = ["pk", "liking_users"]

        extra_kwargs = {"url": {"view_name": "api:article-detail"}}