from django.urls import path
from .views import multi_plant_view, my_trees, plant_tree_view, planted_tree_detail_view, planted_trees_in_user_accounts_view

urlpatterns = [
    path('my-trees/', my_trees, name='my_trees'),
    path('plant-tree/', plant_tree_view, name='plant_tree'),
    path('plant-trees/', multi_plant_view, name='multi_plant'),
    path("trees/<int:pk>/", planted_tree_detail_view, name="planted_tree_detail"),
    path("trees/in-accounts/", planted_trees_in_user_accounts_view,
         name="trees_in_accounts"),
]
