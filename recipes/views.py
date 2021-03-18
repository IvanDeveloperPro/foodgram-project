from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Follow, IngredientAmount, PurchaseRecipe, Recipe, TagFood
from .utils import filter_tags, get_ingredients, save_recipe

User = get_user_model()


def index(request):
    all_tags = TagFood.objects.all()
    recipes = Recipe.objects\
        .select_related('author',)\
        .prefetch_related('ingredient', 'tagfood')\
        .filter(tagfood__title__in=filter_tags(request)).distinct()
    paginator = Paginator(recipes, 6)
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
    tags = TagFood.objects.all()
    recipes = Recipe.objects \
        .select_related('author', ) \
        .prefetch_related('ingredient', 'tagfood') \
        .filter(
            tagfood__title__in=filter_tags(request),
            favorites__user=request.user
        ).distinct()
    paginator = Paginator(recipes, 6)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return render(
        request,
        'recipes/index.html',
        {'page': page, 'paginator': paginator, 'tags': tags}
    )


@login_required
def follow(request):
    authors = Follow.objects.filter(user=request.user)
    paginator = Paginator(authors, 3)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return render(
        request,
        'recipes/myFollow.html',
        {'page': page, 'paginator': paginator}
    )


def author(request, author_name):
    tags = TagFood.objects.all()
    if author_name is None or author_name == '':
        author_name = request.user.username
    author = get_object_or_404(User, username=author_name)
    recipes = Recipe.objects \
        .select_related('author') \
        .prefetch_related('ingredient', 'tagfood') \
        .filter(author=author, tagfood__title__in=filter_tags(request))\
        .distinct()
    paginator = Paginator(recipes, 6)
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
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        ingres = get_ingredients(request, 'nameIngredient', 'valueIngredient')
        if form.is_valid():
            recipe = save_recipe(request, form, ingres)
            return redirect('single_recipe', recipe_id=recipe.id)
    return render(
        request,
        'recipes/formRecipe.html',
        {'form': form}
    )


@login_required(login_url='login')
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author == request.user:
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
        if request.method == 'POST':
            ingres = get_ingredients(
                request,
                'nameIngredient',
                'valueIngredient'
            )
            if form.is_valid():
                recipe = save_recipe(request, form, ingres)
                return redirect(
                    'single_recipe',
                    recipe_id=recipe.id
                )
        return render(
            request,
            'recipes/formRecipe.html',
            {'form': form}
        )

    return redirect('single_recipe', recipe_id=recipe_id)


def remove_purchase(request, recipe_id):
    PurchaseRecipe.objects.get(user=request.user, recipe_id=recipe_id).delete()
    return redirect('purchase')


def to_pdf_file(request):
    if IngredientAmount.objects\
            .filter(recipes__purchases__user=request.user)\
            .exists():
        ingredients = IngredientAmount.objects\
            .filter(recipes__purchases__user=request.user)\
            .annotate(sum=Sum('amount'))\
            .distinct()

        filename = 'purchases.txt'
        with open(filename, 'w') as file:
            for ingredient in ingredients:
                file.write(f'{ingredient} - {ingredient.sum} {ingredient.ingredient.dimension}\n')
        return FileResponse(
            open(filename, 'rb'),
            as_attachment=True,
        )
    return redirect('purchase')


def page_not_found(request, exception): # noqa
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
