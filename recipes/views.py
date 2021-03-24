import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Ingredient, PurchaseRecipe, Recipe, TagRecipe
from .utils import filter_recipes, get_ingredients_dict

User = get_user_model()


def index(request):
    all_tags = TagRecipe.objects.all()
    recipes = filter_recipes(request)
    paginator = Paginator(recipes, settings.PAGINATOR_NUMS)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return render(
        request,
        'recipes/index.html',
        {'page': page, 'paginator': paginator, 'tags': all_tags}
    )


def single_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(
        request,
        'recipes/single_recipe.html',
        {'recipe': recipe}
    )


@login_required(login_url='login')
def favorite(request):
    tags = TagRecipe.objects.all()
    recipes = filter_recipes(request)
    recipes = recipes.filter(favorites__user=request.user)
    paginator = Paginator(recipes, settings.PAGINATOR_NUMS)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return render(
        request,
        'recipes/index.html',
        {'page': page, 'paginator': paginator, 'tags': tags}
    )


@login_required
def follow(request):
    user = get_object_or_404(User, username=request.user.username)
    authors = user.followers.all()
    paginator = Paginator(authors, settings.PAGINATOR_NUMS)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return render(
        request,
        'recipes/myFollow.html',
        {'page': page, 'paginator': paginator}
    )


def author(request, author_name):
    tags = TagRecipe.objects.all()
    if not author_name:
        author_name = request.user.username
    author = get_object_or_404(User, username=author_name)
    recipes = filter_recipes(request)
    recipes = recipes.filter(author=author)
    paginator = Paginator(recipes, settings.PAGINATOR_NUMS)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return render(
        request,
        'recipes/index.html',
        {
            'page': page,
            'paginator': paginator,
            'author': author,
            'tags': tags
        }
    )


@login_required(login_url='login')
def purchase(request):
    recipes = Recipe.objects.filter(purchases__user=request.user)
    return render(
        request,
        'recipes/shopList.html',
        {'recipes': recipes}
    )


@login_required(login_url='login')
def new_recipe(request):
    ingredients = get_ingredients_dict(
        request,
        'nameIngredient',
        'valueIngredient'
    )
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        ingredients=ingredients
    )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        form.save_m2m()

        return redirect('single_recipe', recipe_id=form.instance.id)
    return render(
        request,
        'recipes/formRecipe.html',
        {'form': form}
    )


@login_required(login_url='login')
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author == request.user:
        ingredients = get_ingredients_dict(
            request,
            'nameIngredient',
            'valueIngredient'
        )
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
            ingredients=ingredients,
        )
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect(
                'single_recipe',
                recipe_id=form.instance.id
            )
        return render(
            request,
            'recipes/formRecipe.html',
            {'form': form}
        )
    return redirect('single_recipe', recipe_id=recipe_id)


def remove_purchase(request, recipe_id):
    purchase_recipe = get_object_or_404(
        PurchaseRecipe,
        user=request.user,
        recipe_id=recipe_id
    )
    purchase_recipe.delete()
    return redirect('purchase')


def to_pdf_file(request):
    if (PurchaseRecipe.objects
            .filter(user=request.user)
            .exists()):
        ingredients = (
            Ingredient.objects
            .filter(ingredient_recipes__recipes__purchases__user=request.user)
            .order_by('title')
            .distinct()
            .annotate(sum=Sum('ingredient_recipes__amount'))
        )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename="ingredients.csv"'
        )
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response)
        for ing in ingredients:
            writer.writerow([f'{ing} - {ing.sum} {ing.dimension}'])
        return response
    return redirect('purchase')
