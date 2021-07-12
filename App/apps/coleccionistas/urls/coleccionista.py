from django.urls import path
from apps.coleccionistas.api.api import *
urlpatterns = [
    path('coleccionista', ColeccionistaCreateAPIView.as_view()),
    path('coleccionista/<int:dni>',ColeccionistaRetriveUpdateDestroyAPIView.as_view()),
    path('coleccionista/',ColeccionistaListAPIView.as_view())
]