from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

from trees.models import Tree


class Profile(models.Model):
    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    def plant_tree(self, tree: Tree, location: tuple[Decimal, Decimal]):
        print("")

    def plant_trees(self, plants: list[tuple[Tree, tuple[Decimal, Decimal]]]):
        print("")
