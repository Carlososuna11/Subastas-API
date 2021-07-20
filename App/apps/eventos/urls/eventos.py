from django.urls import path
from apps.eventos.api.api import *

urlpatterns = [
    path('evento',EventoCreateAPIView.as_view(),),
    path('evento/<int:id>',EventoRetriveDestroyAPIView.as_view()),
    path('evento/eventos/<int:id>',EventoPorOrganizacionListAPIView.as_view()),
    path('evento/',EventoListAPIView.as_view()),
    path('evento/prices/<int:id>',UpdatePricesView.as_view()),
    path('evento/cancel/<int:id>',CancelEventView.as_view()),
]