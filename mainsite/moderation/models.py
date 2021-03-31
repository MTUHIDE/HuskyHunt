from django.db import models
from django.utils.translation import ugettext_lazy as _
from catalog.models import CatalogItem
from rideSharing.models import RideItem

class ModerationActionType:
    class Types(models.TextChoices):
        APPROVE = 'AP', _('Approve')
        DENY = 'DY', _('Deny')

    def moderationActionTypeField():
        return models.CharField(
            max_length=2,
            choices=ModerationActionType.Types.choices,
            default=ModerationActionType.Types.DENY
        )

# Create your models here.
class ItemModerationActions(models.Model):
  item_id = models.ForeignKey(CatalogItem, on_delete=models.CASCADE)
  date_action = models.DateField(auto_now=False, auto_now_add=True)
  action_type = ModerationActionType.moderationActionTypeField()
  reason = models.CharField(max_length=255, blank = False, null=False);

  def __str__(self):
        return self.item_id

class RideModerationActions(models.Model):
  ride_id = models.ForeignKey(RideItem, on_delete=models.CASCADE)
  date_action = models.DateField(auto_now=False, auto_now_add=True)
  action_type = ModerationActionType.moderationActionTypeField()
  reason = models.CharField(max_length=255, blank = False, null=False);

  def __str__(self):
        return self.ride_id






    #def myContent(archivedType):
    #    return (archivedType == ArchivedType.Types.HIDDEN) or (archivedType == ArchivedType.Types.REMOVED)
    #Q_myContent = Q(archived='False') | Q(archivedType=Types.HIDDEN) | Q(archivedType=Types.REMOVED)