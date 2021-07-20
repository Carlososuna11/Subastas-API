from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('participante',ParticipanteCreateAPIView.as_view()),
    path('participante/inscripcion/<int:id_evento>',InscribirseView.as_view()),
    path('participante/',ParticipanteListAPIView.as_view()),
    path('participante/evento/<int:id>',ParticipantePorEventoListAPIView.as_view()),
]