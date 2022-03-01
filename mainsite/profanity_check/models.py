from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


class ArchivedType:
    class Types(models.TextChoices):
        VISIBLE = 'VI', _('Visible')
        HIDDEN = 'HD', _('Hidden')  # means profanity filter needs mod review
        REMOVED = 'RE', _('Removed')  # Means a mod confirmed it's bad content
        ARCHIVED = 'AR', _('Archived')  # Means eg user deleted, etc

    @staticmethod
    def myContent(archivedType):
        return (archivedType == ArchivedType.Types.HIDDEN) or (archivedType == ArchivedType.Types.REMOVED)

    # Visible, Hidden, or Removed
    @staticmethod
    def archivedTypeField():
        return models.CharField(
            max_length=2,
            choices=ArchivedType.Types.choices,
            default=ArchivedType.Types.VISIBLE
        )

    Q_myContent = Q(archived='False') | Q(archivedType=Types.HIDDEN) | Q(archivedType=Types.REMOVED)
