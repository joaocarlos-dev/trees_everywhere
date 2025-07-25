from django.urls import path
from .views import my_trees, plant_tree

urlpatterns = [
    path('my-trees/', my_trees, name='my_trees'),
    path('plant-tree/', plant_tree, name='plant_tree'),
]
