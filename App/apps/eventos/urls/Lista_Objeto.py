from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('lista_objeto',Lista_ObjetoCreateAPIView.as_view(),),
    path('lista_objeto/<int:id>',Lista_ObjetoRetrieveUpdateDestroyAPIView.as_view()),
    path('lista_objeto/',Lista_ObjetoListAPIView.as_view()),
]