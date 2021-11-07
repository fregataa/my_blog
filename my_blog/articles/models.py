from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Article(TimeStampedModel):
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(_("Text content of Article"))
    is_published = models.BooleanField(default=False)
    liking_users = models.ManyToManyField(User, related_name="likes")
    tags = models.ManyToManyField(Tag, related_name="used_articles")


class Comment(TimeStampedModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    writer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="comments",
    )
    content = models.CharField(_("Text content of Comment"), max_length=255)


class Recomment(TimeStampedModel):
    comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recomments",
    )
    writer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recomments",
    )
    content = models.CharField(_("Text content of Re-Comment"), max_length=255)
