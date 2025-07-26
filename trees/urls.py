from django.urls import path
from .views import multi_plant_view, my_trees, plant_tree_view

urlpatterns = [
    path('my-trees/', my_trees, name='my_trees'),
    path('plant-tree/', plant_tree_view, name='plant_tree'),
    path('plant-trees/', multi_plant_view, name='multi_plant'),
]
