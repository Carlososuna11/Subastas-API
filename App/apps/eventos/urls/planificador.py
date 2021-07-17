from django.urls import path
from apps.eventos.api.api import *
urlpatterns = [
    path('planificador', PlanificadorCreateAPIView.as_view()),
    path('planificador/<int:id_evento>/<int:id_organizacion>', PlanificadorDestroyAPIView.as_view()),
]