from django.urls import path
from apps.commons.api.api import *
urlpatterns = [
    path('login/',LoginView.as_view()),
    # path('logout/',LogoutView.as_view()),
    path('getUser/',GETView.as_view()),
]