from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('participante',ParticipanteCreateAPIView.as_view(),),
    path('participante/',ParticipanteListAPIView.as_view()),
]