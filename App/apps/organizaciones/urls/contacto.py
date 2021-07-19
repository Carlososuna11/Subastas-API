from django.urls import path
from apps.organizaciones.api.api import *
urlpatterns = [
    path('contacto', ContactoCreateAPIView.as_view()),
    path('contacto/<int:id>',ContactoRetriveUpdateDestroyAPIView.as_view()),
    path('contacto/',ContactoListAPIView.as_view()),
    path('contactos/<int:id>',ContactoOrganizacionListAPIView.as_view()),
]