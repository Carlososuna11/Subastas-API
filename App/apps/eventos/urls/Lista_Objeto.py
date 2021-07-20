from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('lista_objeto',Lista_ObjetoCreateAPIView.as_view(),),
    path('lista_objeto/get/<int:id>',Lista_ObjetoRetrieveUpdateDestroyAPIView.as_view()),
    path('lista_objeto/evento/<int:id_evento>',Lista_Objeto_Por_Evento_ListAPIView.as_view()),
    path('lista_objeto/',Lista_ObjetoListAPIView.as_view()),
    #path('lista_objeto/ordenlista/',Orden_ListaCreateAPIView.as_view(),),
]