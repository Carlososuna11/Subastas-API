from rest_framework import generics
from database.conexion import conectar
from apps.monedas.api.serializers.moneda_artista import *
from apps.monedas.models import Moneda_Artista
from django.http import Http404

# class Moneda_ArtistaListAPIView(generics.ListAPIView):
#     serializer_class = Moneda_ArtistaSerializer

#     @conectar
#     def get_queryset(self,connection):
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM paises")
#         casas = [Moneda_Artista.model(**dato) for dato in cursor]
#         return casas
    

class Moneda_ArtistaCreateAPIView(generics.CreateAPIView):
    serializer_class = Moneda_ArtistaSerializer

class Moneda_ArtistaDestroyAPIView(generics.DestroyAPIView):
    serializer_class = Moneda_ArtistaSerializer
    
    @conectar
    def get_object(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM M_A WHERE (id_moneda,id_artista)=(%s,%s)",(self.kwargs.get('id_moneda'),self.kwargs.get('id_artista')))
        datos = cursor.fetchone()
        if datos:
            return Moneda_Artista.model(**datos)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM M_A WHERE (id_moneda,id_artista)=(%s,%s)",(instance.id_moneda,instance.id_artista))
        connection.commit()
