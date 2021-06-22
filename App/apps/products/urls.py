from django.urls import path
from apps.products.api.api import *
urlpatterns = [
    path('',ProductCreateAPIView.as_view(),name= 'create'),
    path('<int:pk>/',ProductRetriveUpdateDestroyAPIView.as_view(),name='RetrieveUpdateDestroy'),
    path('products',ProductListAPIView.as_view(),name='products'),
]
