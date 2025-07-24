from decimal import Decimal
from django.db import models

from accounts.models import Account
from users.models import User

# Create your models here.


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)


class PlantedTree(models.Model):
    age = models.IntegerField
    planted_at = models.DateTimeField(auto_created=True)
    user = User
    tree = Tree
    account = Account
    location = tuple[models.DecimalField, models.DecimalField]
