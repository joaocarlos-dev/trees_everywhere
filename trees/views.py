from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from trees.models import PlantTreeForm, PlantedTree


@login_required
def my_trees(request):
    trees = PlantedTree.objects.filter(user=request.user)
    return render(request, 'trees/my_trees.html', {'trees': trees})


@login_required
def plant_tree(request):
    if request.method == 'POST':
        form = PlantTreeForm(request.user, request.POST)
        if form.is_valid():
            tree = form.cleaned_data['tree']
            location = (form.cleaned_data['latitude'],
                        form.cleaned_data['longitude'])
            account = form.cleaned_data['account']
            age = form.cleaned_data['age']

            planted_tree = request.user.plant_tree(
                tree=tree, location=location, account=account)
            planted_tree.age = age
            planted_tree.save()

            return redirect('my_trees')
    else:
        form = PlantTreeForm(request.user)
    return render(request, 'trees/plant_tree.html', {'form': form})
