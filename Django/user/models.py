from django.db import models

class User(models.Model):
    openid = models.CharField(max_length=255, unique=True)