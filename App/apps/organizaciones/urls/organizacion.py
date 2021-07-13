from django.urls import path
from apps.organizaciones.api.api import *
urlpatterns = [
    path('organizacion', OrganizacionCreateAPIView.as_view()),
    path('organizacion/<int:id>',OrganizacionRetriveUpdateDestroyAPIView.as_view()),
    path('organizacion/',OrganizacionListAPIView.as_view())
]