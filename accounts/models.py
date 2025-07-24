from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_created=True)
    active = models.BooleanField(default=True)
