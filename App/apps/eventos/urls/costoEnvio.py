from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('costoEnvio',CostoEnvioCreateAPIView.as_view(),),
    path('costoEnvio/<int:id>',CostoEnvioRetriveUpdateDestroyAPIView.as_view()),
    path('costoEnvio/',CostoEnvioListAPIView.as_view()),
]