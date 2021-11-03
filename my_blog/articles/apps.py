from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticlesConfig(AppConfig):
    name = "my_blog.articles"
    verbose_name = _("Articles")
