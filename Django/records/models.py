from django.db import models

from user.models import User

class AbstractRecordBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class FoodRecord(AbstractRecordBase):
    pass

class UricacidRecord(AbstractRecordBase):
    pass

class FlareupRecord(AbstractRecordBase):
    pass