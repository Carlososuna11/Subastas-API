from rest_framework import generics
from database.conexion import conectar
from apps.commons.api.serializers.artista import *
from apps.commons.models import Artista
from django.http import Http404

class ArtistaListAPIView(generics.ListAPIView):
    serializer_class = ArtistaSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM caj_artistas")
        casas = [Artista.model(**dato) for dato in cursor]
        return casas
    

class ArtistaCreateAPIView(generics.CreateAPIView):
    serializer_class = ArtistaSerializer

class ArtistaRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtistaSerializer
    
    @conectar
    def get_object(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM caj_artistas WHERE id=%s",(self.kwargs[self.lookup_field],))
        datos = cursor.fetchone()
        if datos:
            return Artista(**datos)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM caj_artistas WHERE id = %s",(instance.id,))
        connection.commit()
