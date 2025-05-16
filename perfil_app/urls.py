from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('publicaciones/', views.publicaciones, name='publicaciones'),  # si ya la tienes
    path('tesis/', views.tesis, name='tesis'),  # si ya la tienes
    path('redes/', views.redes, name='redes'),  # si ya la tienes
    path('regresor/', views.regresor, name='regresor'),
    path('cnn/', views.cnn, name='cnn'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
