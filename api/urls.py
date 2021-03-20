from django.urls import path

from .views import IngredientView, favorites, purchases, subscriptions

urlpatterns = [
    path('ingredients/', IngredientView.as_view(), name='ingredients'),
    path('favorites/', favorites, name='favorites'),
    path('purchases/', purchases, name='purchases'),
    path('subscriptions/', subscriptions, name='subscriptions')
]
