from django.urls import path
from apps.pinturas.api.api import *
urlpatterns = [
    path('catalogo/pintura', PinturaCreateAPIView.as_view()),
    path('catalogo/pintura/<int:nur>', PinturaRetriveDestroyAPIView.as_view()),
    path('catalogo/pintura/', PinturaListAPIView.as_view())
]