from django.db import models

from trees_everywhere import settings


class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_created=True)
    active = models.BooleanField(default=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='accounts')
