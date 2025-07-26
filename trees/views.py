import ast
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from trees.forms import MultiPlantingForm, PlantTreeForm
from trees.models import PlantedTree


@login_required
def my_trees(request):
    trees = PlantedTree.objects.filter(user=request.user)
    return render(request, 'trees/my_trees.html', {'trees': trees})


@login_required
def plant_tree_view(request):
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


@login_required
def multi_plant_view(request):
    if request.method == "POST":
        form = MultiPlantingForm(request.POST)
        if form.is_valid():
            tree = form.cleaned_data['tree']
            coordinates_str = form.cleaned_data['coordinates']

            try:
                coordinates_list = ast.literal_eval(coordinates_str)
                if not isinstance(coordinates_list, list) or not all(
                    isinstance(t, tuple) and len(t) == 2 for t in coordinates_list
                ):
                    raise ValueError("Invalid coordinates format.")

                tree_locations = [
                    (tree, (Decimal(str(lat)), Decimal(str(lon))))
                    for lat, lon in coordinates_list
                ]

                account = request.user.accounts.first()
                if not account:
                    return HttpResponse("User does not have an associated account.", status=400)

                request.user.plant_trees(tree_locations, account)
                return redirect("my_trees")

            except (SyntaxError, ValueError) as e:
                form.add_error(
                    'coordinates', f"Error parsing coordinates: {e}")

    else:
        form = MultiPlantingForm()

    return render(request, "trees/multi_plant.html", {"form": form})
