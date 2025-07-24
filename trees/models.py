from decimal import Decimal
from django.db import models

from accounts.models import Account
from users.models import User

# Create your models here.


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)


class PlantedTree(models.Model):
    age = models.IntegerField()
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='planted_trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    latitude = models.DecimalField()
    longitude = models.DecimalField()

    @property
    def location(self):
        return (self.latitude, self.longitude)
