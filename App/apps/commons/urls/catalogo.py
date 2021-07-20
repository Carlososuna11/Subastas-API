from django.urls import path
from apps.commons.api.api import *
urlpatterns = [
    path('catalogo/coleccionista/<int:id>',CatalogoColeccionistaListAPIView.as_view()),
    path('catalogo/organizacion/<int:id>',CatalogoOrganizacionListAPIView.as_view()),
]