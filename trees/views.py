from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from trees.models import PlantedTree


@login_required
def my_trees(request):
    trees = PlantedTree.objects.filter(user=request.user)
    return render(request, 'trees/my_trees.html', {'trees': trees})
