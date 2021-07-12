from django.urls import path
from apps.commons.api.api import *
urlpatterns = [
    path('divisa',DivisaCreateAPIView.as_view()),
    path('divisa/<int:id>',DivisaRetriveUpdateDestroyAPIView.as_view()),
    path('divisa/',DivisaListAPIView.as_view()),
]