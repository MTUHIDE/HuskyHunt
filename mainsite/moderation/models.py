from django.db import models
from django.utils.translation import ugettext_lazy as _

from catalog.models import CatalogItem
from rideSharing.models import RideItem


class ModerationActionType:
    class Types(models.TextChoices):
        APPROVE = 'AP', _('Approve')
        DENY = 'DY', _('Deny')
        REMOVE = 'RM', _('Remove')

    @staticmethod
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
    reason = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.item_id.id)


class RideModerationActions(models.Model):
    ride_id = models.ForeignKey(RideItem, on_delete=models.CASCADE)
    date_action = models.DateField(auto_now=False, auto_now_add=True)
    action_type = ModerationActionType.moderationActionTypeField()
    reason = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.ride_id.id)


class InitialContactLog(models.Model):
    # Email that sends the message
    sender = models.TextField()
    # Email that receives it
    receiver = models.TextField()
    # The datetime it was sent
    date_sent = models.DateTimeField(auto_now=False, auto_now_add=True)
    # The actual content of the message
    message = models.TextField()

    @classmethod
    def create(cls, sender, receiver, date_sent, message):
        log = cls(sender=sender, receiver=receiver, date_sent=date_sent, message=message)
        log.save()
        return log

    def __str__(self):
        return f'[{self.date_sent}] {self.sender} -> {self.receiver}: {self.message}'
