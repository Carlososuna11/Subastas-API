from rest_framework import generics
from database.conexion import conectar
from apps.eventos.api.serializers.planificador import *
from apps.eventos.models import Planificador
from django.http import Http404

# class PlanificadorListAPIView(generics.ListAPIView):
#     serializer_class = PlanificadorSerializer

#     @conectar
#     def get_queryset(self,connection):
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM paises")
#         casas = [Planificador.model(**dato) for dato in cursor]
#         return casas
    

class PlanificadorCreateAPIView(generics.CreateAPIView):
    serializer_class = PlanificadorSerializer

class PlanificadorDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PlanificadorSerializer
    
    @conectar
    def get_object(self,connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM planificadores WHERE (id_organizacion,id_evento)=(%s,%s)",(self.kwargs.get('id_organizacion'),self.kwargs.get('id_evento')))
        datos = cursor.fetchone()
        if datos:
            return Planificador.model(**datos)
        else:
            raise Http404

    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM planificadores WHERE (id_organizacion,id_evento)=(%s,%s)",(instance.id_organizacion,instance.id_evento))
        connection.commit()
