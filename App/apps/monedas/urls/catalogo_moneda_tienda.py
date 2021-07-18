from django.urls import path
from apps.monedas.api.api import *
urlpatterns = [
    path('catalogo/moneda', Catalogo_Moneda_TiendaCreateAPIView.as_view()),
    path('catalogo/moneda/obj/<int:nur>', Catalogo_Moneda_TiendaRetriveDestroyAPIView.as_view()),
    path('catalogo/moneda/', Catalogo_Moneda_TiendaListAPIView.as_view()),
    path('catalogo/moneda/<int:id>', Catalogo_Moneda_TiendaOrganizacionListAPIView.as_view())
]