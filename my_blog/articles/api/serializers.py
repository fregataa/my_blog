from rest_framework import serializers

from ..models import Article, Comment, Recomment, Tag


class GenericCommentSerializer(serializers.ModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="api:article-detail"
    )

    class Meta:
        model = Comment
        fields = ["pk", "article", "writer", "content"]


class RecommentSerializer(serializers.ModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="api:article-detail"
    )
    comment = GenericCommentSerializer(read_only=True)

    class Meta:
        model = Recomment
        fields = ["pk", "writer", "content", "article", "comment"]


class CommentSerializer(GenericCommentSerializer):
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["pk", "article", "writer", "content", "recomments"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "pk",
            "title",
            "writer",
            "content",
            "is_published",
            "liking_users",
            "comments",
            "tags",
            "url",
        ]
        read_only_fields = ["pk", "liking_users"]

        extra_kwargs = {"url": {"view_name": "api:article-detail"}}
