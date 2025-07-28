from django.db import models

from accounts.models import Account
from trees_everywhere import settings


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    """
    Represents a tree planted by a user at a specific location.

    Fields:
        age (int): The age of the planted tree in years. Defaults to 0.
        planted_at (datetime): The timestamp when the tree was planted. Set automatically on creation.
        user (ForeignKey): Reference to the user who planted the tree.
        tree (ForeignKey): Reference to the type of tree planted.
        account (ForeignKey): Reference to the account associated with the planting.
        latitude (Decimal): Latitude coordinate of the planted tree's location.
        longitude (Decimal): Longitude coordinate of the planted tree's location.

    Properties:
        location (tuple): Returns a tuple (latitude, longitude) representing the tree's location.
        latitude_str (str): Returns the latitude as a string formatted to 6 decimal places.
        longitude_str (str): Returns the longitude as a string formatted to 6 decimal places.
    """
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
