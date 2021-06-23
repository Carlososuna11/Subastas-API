from django.urls import path
from apps.students.api.api import *

urlpatterns = [
    path('', StudentCreateAPIView.as_view(),name= 'create'),
    path('<int:pk>/',StudentRetriveUpdateDestroyAPIView.as_view(),name='RetrieveUpdateDestroy'),
    path('students',StudentListAPIView.as_view(),name='students'),
]
