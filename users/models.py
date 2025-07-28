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
    def plant_tree(self, tree: Tree, location: tuple[Decimal, Decimal], account: Account, age: int = 0) -> PlantedTree:
        """
        Create a single planted tree associated with this user.

        Args:
            tree (Tree): The tree species to be planted.
            location (tuple[Decimal, Decimal]): Latitude and longitude coordinates.
            account (Account): The account to associate the planted tree with.
            age (int, optional): Age of the planted tree. Defaults to 0.

        Returns:
            PlantedTree: The created planted tree instance.
        """
        if account is None:
            account = self.accounts.first()
            if not account:
                raise ValueError("User doesn't have associeated account")

        latitude, longitude = location

        return PlantedTree.objects.create(
            user=self,
            tree=tree,
            account=account,
            latitude=latitude,
            longitude=longitude,
            age=age
        )

    def plant_trees(self, plants: list[tuple[Tree, tuple[Decimal, Decimal]]], account: Account,  age: int = 0) -> list[PlantedTree]:
        """
        Create multiple planted trees associated with this user.

        Args:
            plants (list[tuple[Tree, tuple[Decimal, Decimal]]]): List of tuples containing tree species and their locations.
            account (Account): The account to associate the planted trees with.
            age (int, optional): Age to set for all planted trees. Defaults to 0.

        Raises:
            ValueError: If the user has no associated account and none is provided.

        Returns:
            list[PlantedTree]: List of created planted tree instances.
        """
        if account is None:
            account = self.accounts.first()
            if not account:
                raise ValueError("User doesn't have associeated account")

        planted_trees = []
        for tree, location in plants:
            latitude, longitude = location
            planted = PlantedTree(
                user=self,
                tree=tree,
                account=account,
                latitude=latitude,
                longitude=longitude,
                age=age
            )
            planted_trees.append(planted)

        PlantedTree.objects.bulk_create(planted_trees)
        return planted_trees
