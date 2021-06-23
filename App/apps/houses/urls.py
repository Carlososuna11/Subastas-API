from django.urls import path
from apps.houses.api.api import *
urlpatterns = [
    path('',HouseCreateAPIView.as_view(),name= 'create'),
    path('<int:pk>/',HouseRetriveUpdateDestroyAPIView.as_view(),name='RetrieveUpdateDestroy'),
    path('houses',HouseListAPIView.as_view(),name='houses'),
]
