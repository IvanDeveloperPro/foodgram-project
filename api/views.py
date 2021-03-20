from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    FavoriteRecipe, Follow, Ingredient, PurchaseRecipe, Recipe)

from .serializers import IngredientSerializer

User = get_user_model()


class IngredientView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['$title', ]


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorites(request):
    recipe = get_object_or_404(
        Recipe,
        id=request.data.get('id')
    )
    if request.method == 'POST':
        FavoriteRecipe.objects.get_or_create(recipe=recipe, user=request.user)
    else:
        favor_recipe = get_object_or_404(
            FavoriteRecipe,
            recipe=recipe,
            user=request.user
        )
        favor_recipe.delete()
    return Response(data={'success': True})


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscriptions(request):
    author = get_object_or_404(
        User,
        id=request.data.get('id')
    )
    if request.method == 'POST':
        Follow.objects.get_or_create(author=author, user=request.user)
    else:
        follow = get_object_or_404(
            Follow,
            author=author,
            user=request.user
        )
        follow.delete()
    return Response(data={'success': True})


@api_view(['POST', 'DELETE'])
@permission_classes([AllowAny])
def purchases(request):
    recipe = get_object_or_404(
        Recipe,
        id=request.data.get('id')
    )
    if request.method == 'POST':
        PurchaseRecipe.objects.get_or_create(recipe=recipe, user=request.user)
    else:
        purchase_recipe = get_object_or_404(
            PurchaseRecipe,
            recipe=recipe,
            user=request.user
        )
        purchase_recipe.delete()
    return Response(data={'success': True})
