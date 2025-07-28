import ast
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from trees.forms import MultiPlantingForm, PlantTreeForm
from trees.models import PlantedTree
from django.core.exceptions import PermissionDenied


@login_required
def my_trees(request):
    trees = PlantedTree.objects.filter(user=request.user)
    return render(request, 'trees/my_trees.html', {'trees': trees})


@login_required
def plant_tree_view(request):
    """
    Handles the planting of a new tree by the authenticated user.

    Returns:
        HttpResponse: The rendered template or a redirect to the 'my_trees' page.
    """
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
    """
    Handles the planting of multiple trees by a user via a form submission.

    Returns:
        HttpResponse: Renders the multi-planting form or redirects to "my_trees" on success.
    """
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


@login_required
def planted_tree_detail_view(request, pk):
    """
    View to display the details of a specific PlantedTree instance.

    Args:
        pk (int): Primary key of the PlantedTree to retrieve.

    Raises:
        PermissionDenied: If the current user does not own the requested PlantedTree.

    Returns:
        HttpResponse: Rendered detail page for the specified PlantedTree.
    """
    planted_tree = get_object_or_404(PlantedTree, pk=pk)
    if planted_tree.user != request.user:
        raise PermissionDenied
    return render(request, "trees/planted_tree_detail.html", {"planted_tree": planted_tree})


@login_required
def planted_trees_in_user_accounts_view(request):
    """
    View to display all planted trees associated with the accounts of the currently authenticated user.

    Returns:
        HttpResponse: Rendered HTML page displaying the planted trees in the user's accounts.
    """
    user = request.user
    accounts = user.accounts.all()

    planted_trees = PlantedTree.objects.filter(
        account__in=accounts).select_related('tree', 'user')

    context = {
        "planted_trees": planted_trees,
    }
    return render(request, "trees/trees_in_accounts.html", context)
