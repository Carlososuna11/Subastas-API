from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from database.conexion import conectar
from apps.products.api.serializers import *
from apps.products.models import Producto
from django.http import Http404

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = [Producto(**dato) for dato in cursor]
        return productos
    

class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer

class ProductRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
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
        cursor.execute("SELECT * FROM productos WHERE id=%s",(self.kwargs[self.lookup_field],))
        datos = cursor.fetchone()
        if datos:
            return Producto(**datos)
        else:
            raise Http404

    # def get(self, request, id):
    #     producto = self.get_object(id)
    #     serializer = ProductSerializer(producto)
    #     return Response(serializer.data)

    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s",(instance.id,))
        connection.commit()

    # def get(self, request, *args, **kwargs):
    #     res = super().get(request, *args, **kwargs)
    #     res.data['image'] = None if res.data['image'] is None else res.data['image'].replace('/core/Diary','')
    #     return res

