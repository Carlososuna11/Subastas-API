from rest_framework import generics
from database.conexion import conectar
from apps.pinturas.api.serializers.pintura_artista import *
from apps.pinturas.models import Pintura_Artista
from django.http import Http404

# class Pintura_ArtistaListAPIView(generics.ListAPIView):
#     serializer_class = Pintura_ArtistaSerializer

#     @conectar
#     def get_queryset(self,connection):
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM paises")
#         casas = [Pintura_Artista.model(**dato) for dato in cursor]
#         return casas
    

class Pintura_ArtistaCreateAPIView(generics.CreateAPIView):
    serializer_class = Pintura_ArtistaSerializer

class Pintura_ArtistaDestroyAPIView(generics.DestroyAPIView):
    serializer_class = Pintura_ArtistaSerializer
    
    @conectar
    def get_object(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM caj_P_A WHERE (id_pintura,id_artista)=(%s,%s)",(self.kwargs.get('id_pintura'),self.kwargs.get('id_artista')))
        datos = cursor.fetchone()
        if datos:
            return Pintura_Artista.model(**datos)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM caj_P_A WHERE (id_pintura,id_artista)=(%s,%s)",(instance.id_pintura,instance.id_artista))
        connection.commit()
