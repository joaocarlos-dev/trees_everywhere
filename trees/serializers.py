from rest_framework import serializers
from .models import PlantedTree


class PlantedTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = ['id', 'tree', 'age', 'planted_at', 'latitude', 'longitude']
        depth = 1
