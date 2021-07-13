from django.urls import path
from apps.monedas.api.api import *
urlpatterns = [
    path('catalogo/moneda', Catalogo_Moneda_TiendaCreateAPIView.as_view()),
    path('catalogo/moneda/<int:nur>', Catalogo_Moneda_TiendaRetriveDestroyAPIView.as_view()),
    path('catalogo/moneda/', Catalogo_Moneda_TiendaListAPIView.as_view())
]