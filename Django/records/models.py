import datetime

from django.db import models

from user.models import User
from food.models import Food

class AbstractRecordBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record_date = models.DateField(default=datetime.date.today)

    class Meta:
        abstract = True

class FoodRecord(AbstractRecordBase):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField()

class UricacidRecord(AbstractRecordBase):
    quantity = models.FloatField()

class FlareupRecord(AbstractRecordBase):
    symptom = models.CharField(max_length=500)
    intense_level = models.IntegerField(choices=(
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ))
    trigger = models.CharField(max_length=500)