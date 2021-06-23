from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from database.conexion import conectar
from apps.houses.api.serializers import *
from apps.houses.models import Casa
from django.http import Http404

class HouseListAPIView(generics.ListAPIView):
    serializer_class = HouseSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM casas")
        casas = [Casa(**dato) for dato in cursor]
        return casas
    

class HouseCreateAPIView(generics.CreateAPIView):
    serializer_class = HouseSerializer

class HouseRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HouseSerializer
    # @conectar
    # def get_queryset(self,connection):
    #     cursor = connection.cursor(dictionary=True)
    #     cursor.execute("SELECT * FROM productos");
    #     productos = [Producto(**dato) for dato in cursor]
    #     #print(productos)
    #     return productos
    @conectar
    def get_object(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM casas WHERE id=%s",(self.kwargs[self.lookup_field],))
        datos = cursor.fetchone()
        if datos:
            return Casa(**datos)
        else:
            raise Http404

    # def get(self, request, id):
    #     producto = self.get_object(id)
    #     serializer = ProductSerializer(producto)
    #     return Response(serializer.data)

    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM casas WHERE id = %s",(instance.id,))
        connection.commit()

    # def get(self, request, *args, **kwargs):
    #     res = super().get(request, *args, **kwargs)
    #     res.data['image'] = None if res.data['image'] is None else res.data['image'].replace('/core/Diary','')
    #     return res

