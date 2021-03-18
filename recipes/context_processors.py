from .models import PurchaseRecipe


def amount(request):
    if request.user.is_anonymous:
        return {'amount': 0}
    number = PurchaseRecipe.objects.filter(user=request.user).count()
    return {'amount': number}
