from django.urls import path
from .views import my_trees

urlpatterns = [
    path('my-trees/', my_trees, name='my_trees'),

]
