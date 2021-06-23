from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from database.conexion import conectar
from apps.students.api.serializers import *
from apps.students.models import Estudiante
from django.http import Http404

class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiantes")
        estudiantes = [Estudiante(**dato) for dato in cursor]
        return estudiantes
    

class StudentCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentSerializer

class StudentRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
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
        cursor.execute("SELECT * FROM estudiantes WHERE dni=%s",(self.kwargs[self.lookup_field],))
        datos = cursor.fetchone()
        if datos:
            return Estudiante(**datos)
        else:
            raise Http404

    # def get(self, request, id):
    #     producto = self.get_object(id)
    #     serializer = ProductSerializer(producto)
    #     return Response(serializer.data)

    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE dni = %s",(instance.dni,))
        connection.commit()

    # def get(self, request, *args, **kwargs):
    #     res = super().get(request, *args, **kwargs)
    #     res.data['image'] = None if res.data['image'] is None else res.data['image'].replace('/core/Diary','')
    #     return res

