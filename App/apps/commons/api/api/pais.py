from rest_framework import generics
from database.conexion import conectar
from apps.commons.api.serializers.pais import *
from apps.commons.models import Pais
from django.http import Http404

class PaisListAPIView(generics.ListAPIView):
    serializer_class = PaisSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM paises")
        casas = [Pais.model(**dato) for dato in cursor]
        return casas
    

class PaisCreateAPIView(generics.CreateAPIView):
    serializer_class = PaisSerializer

class PaisRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaisSerializer
    
    @conectar
    def get_object(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM paises WHERE id=%s",(self.kwargs[self.lookup_field],))
        datos = cursor.fetchone()
        if datos:
            return Pais.model(**datos)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM paises WHERE id = %s",(instance.id,))
        connection.commit()
