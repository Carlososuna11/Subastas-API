from django.urls import path
from apps.pinturas.api.api import *
urlpatterns = [
    path('pintura_artista', Pintura_ArtistaCreateAPIView.as_view()),
    path('pintura_artista/<int:id_pintura>/<int:id_artista>', Pintura_ArtistaDestroyAPIView.as_view()),
]