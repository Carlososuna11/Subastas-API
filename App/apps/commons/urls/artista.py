
from django.urls import path
from apps.commons.api.api import *
urlpatterns = [
    path('artista',ArtistaCreateAPIView.as_view()),
    path('artista/<int:pk>',ArtistaRetriveUpdateDestroyAPIView.as_view()),
    path('artista/',ArtistaListAPIView.as_view()),
]