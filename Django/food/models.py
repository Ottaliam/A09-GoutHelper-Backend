from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ms_unit = models.CharField(max_length=50)
    purine_per_unit = models.FloatField()
    health_tip = models.CharField(max_length=500)
    image = models.ImageField(upload_to='food')