from django.urls import path
from apps.monedas.api.api import *
urlpatterns = [
    path('moneda_artista', Moneda_ArtistaCreateAPIView.as_view()),
    path('moneda_artista/<int:id_moneda>/<int:id_artista>', Moneda_ArtistaDestroyAPIView.as_view()),
]