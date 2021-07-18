from django.urls import path
from apps.coleccionistas.api.api import *
urlpatterns = [
    path('coleccionista', ColeccionistaCreateAPIView.as_view()),
    path('coleccionista/<int:id>',ColeccionistaRetriveUpdateDestroyAPIView.as_view()),
    path('coleccionista/',ColeccionistaListAPIView.as_view())
]