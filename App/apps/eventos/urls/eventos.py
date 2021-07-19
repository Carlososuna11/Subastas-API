from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('evento',EventoCreateAPIView.as_view(),),
    path('evento/<int:id>',EventoRetriveUpdateDestroyAPIView.as_view()),
    path('evento/eventos/<int:id>',EventoPorOrganizacionListAPIView.as_view()),
    path('evento/',EventoListAPIView.as_view()),
]