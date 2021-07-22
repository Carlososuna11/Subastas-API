from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('evento',EventoCreateAPIView.as_view(),),
    path('evento/<int:id>',EventoRetriveDestroyAPIView.as_view()),
    path('evento/eventos/<int:id>',EventoPorOrganizacionListAPIView.as_view()),
    path('evento/',EventoListAPIView.as_view()),
    path('evento/prices/<int:id>',UpdatePricesView.as_view()),
    path('evento/cancel/<int:id>',CancelEventView.as_view()),
    path('evento/comenzar/<int:id>',ComenzarEvento.as_view()),
    path('evento/pujadinamica/<int:id>',PujaDinamica.as_view()),
    path('evento/pujasobrecerrado/<int:id>',PujaSobreCerrado.as_view()),
    path('evento/actualizar/',ActualizarStatus.as_view()),
    path('evento/getbysubasta/<int:id>',getEventobySubasta.as_view()),
    path('evento/getpujadinamica/<int:id>',GetPujasDinamicaView.as_view()),
    path('evento/getpujasobrecerrado/<int:id>',GetPujasSobreCerradoView.as_view()),
]