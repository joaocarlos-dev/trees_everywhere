from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

from accounts.models import Account
from trees.models import PlantedTree, Tree
from trees_everywhere import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    def plant_tree(self, tree: Tree, location: tuple[Decimal, Decimal], account: Account) -> PlantedTree:
        if account is None:
            account = self.accounts.first()
            if not account:
                raise ValueError("Usuário não possui nenhuma conta associada.")

        latitude, longitude = location

        return PlantedTree.objects.create(
            user=self,
            tree=tree,
            account=account,
            latitude=latitude,
            longitude=longitude,
            age=0
        )

    def plant_trees(self, plants: list[tuple[Tree, tuple[Decimal, Decimal]]], account: Account) -> list[PlantedTree]:
        if account is None:
            account = self.accounts.first()
            if not account:
                raise ValueError("Usuário não possui nenhuma conta associada.")

        planted_trees = []
        for tree, location in plants:
            latitude, longitude = location
            planted = PlantedTree(
                user=self,
                tree=tree,
                account=account,
                latitude=latitude,
                longitude=longitude,
                age=0
            )
            planted_trees.append(planted)

        PlantedTree.objects.bulk_create(planted_trees)
        return planted_trees
