from django.forms.models import modelformset_factory
from decimal import Decimal
from django.db import models
from django import forms

from accounts.models import Account
from trees_everywhere import settings


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    age = models.IntegerField(default=0)
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='planted_trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    @property
    def location(self):
        return (self.latitude, self.longitude)

    @property
    def latitude_str(self):
        return f"{self.latitude:.6f}"

    @property
    def longitude_str(self):
        return f"{self.longitude:.6f}"
