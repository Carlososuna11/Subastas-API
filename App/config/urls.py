from django.urls.conf import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Test API",
      default_version='v1',
      description="Test API Lista de endpoints",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="carlosalvaroosuna1@gmail.com"),
      license=openapi.License(name="GNU GENERAL PUBLIC LICENSE"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('',include('apps.commons.urls.divisa')),
    path('',include('apps.commons.urls.pais')),
    path('',include('apps.commons.urls.artista')),
    path('',include('apps.monedas.urls.moneda')),
    path('',include('apps.monedas.urls.catalogo_moneda_tienda')),
    path('',include('apps.monedas.urls.moneda_artista')),
    path('',include('apps.coleccionistas.urls.coleccionista')),
    path('',include('apps.organizaciones.urls.organizacion')),
    path('',include('apps.organizaciones.urls.contacto')),
    # path('houses/',include('apps.houses.urls')),
    # path('students/',include('apps.students.urls'))
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)