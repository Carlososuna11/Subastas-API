from django.urls import path
from apps.coleccionistas.api.api import *
urlpatterns = [
    path('cliente', ClienteCreateAPIView.as_view()),
    #path('cliente/<int:dni>',ColeccionistaRetriveUpdateDestroyAPIView.as_view()),
    path('cliente/',ClienteListAPIView.as_view())
]