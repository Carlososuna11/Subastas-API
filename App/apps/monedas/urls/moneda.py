from django.urls import path
from apps.monedas.api.api import *
urlpatterns = [
    path('moneda', MonedaCreateAPIView.as_view()),
    path('moneda/<int:id>', MonedaRetriveUpdateDestroyAPIView.as_view()),
    path('moneda/', MonedaListAPIView.as_view())
]