from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

urlpatterns = [
    path('', include('recipes.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('other/', include('django.contrib.flatpages.urls')),

]

urlpatterns += [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'foodgram.views.page_not_found' # noqa
handler500 = 'foodgram.views.server_error'  # noqa
