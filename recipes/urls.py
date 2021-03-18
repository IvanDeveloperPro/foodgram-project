from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('purchase/', views.purchase, name='purchase'),
    path('follow/', views.follow, name='follow'),
    path('author/<str:author_name>/', views.author, name='author'),
    path('recipe/<int:recipe_id>/', views.single_recipe, name='single_recipe'),
    path('new_recipe/', views.new_recipe, name='new_recipe'),
    path(
         'edit_recipe/<int:recipe_id>/',
         views.edit_recipe,
         name='edit_recipe'
     ),
    path('download_purchases/', views.to_pdf_file, name='to_pdf_file'),
    path(
        'remove_purchase/<int:recipe_id>/',
        views.remove_purchase,
        name='remove_purchase'
     ),

]
