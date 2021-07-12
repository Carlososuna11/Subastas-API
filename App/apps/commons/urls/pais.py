from django.urls import path
from apps.commons.api.api import *
urlpatterns = [
    path('pais',PaisCreateAPIView.as_view(),),
    path('pais/<int:pk>',PaisRetriveUpdateDestroyAPIView.as_view()),
    path('pais/',PaisListAPIView.as_view()),
]