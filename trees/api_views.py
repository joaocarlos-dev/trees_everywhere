from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from trees.models import PlantedTree


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_planted_trees_api(request):
    """
    Returns:
        A JSON response containing all trees planted by the user.
    """
    user = request.user
    planted_trees = PlantedTree.objects.filter(user=user)
    data = [
        {
            "tree": tree.tree.name,
            "age": tree.age,
            "planted_at": tree.planted_at
        } for tree in planted_trees
    ]
    return Response(data)
