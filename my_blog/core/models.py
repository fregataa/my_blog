from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """An abstract base class model that provides
    self-updating ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(
        _("Created DateTime"), auto_now_add=True, null=True, blank=True
    )
    modified = models.DateTimeField(
        _("Modified DateTime"), auto_now=True, null=True, blank=True
    )

    class Meta:
        abstract = True
