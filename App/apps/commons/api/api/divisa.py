from rest_framework import generics
from database.conexion import conectar
from apps.commons.api.serializers.divisa import *
from apps.commons.models import Divisa
from django.http import Http404
import inspect

class DivisaListAPIView(generics.ListAPIView):
    """
    Este endpoint cuenta con un query param, que es id_pais, lo que hace es filtrar
    las divisas según el pais ejemplo: http://127.0.0.1:8000/commons/divisa/?id_pais=2
    """
    serializer_class = DivisaSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
                            paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
                        FROM divisas 
                        INNER JOIN paises ON paises.id = divisas.id_pais"""
        if query:
            query_action = """SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
                            paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
                            FROM divisas 
                            INNER JOIN paises ON paises.id = divisas.id_pais
                            WHERE divisas.id_pais = %s
                            """
            cursor.execute(query_action,(query,))
        else:
            cursor.execute(query_action)
        #print(pais_quey,id_pais_query)
        divisas = []
        for dato in cursor:
            divisa = {}
            pais = {}
            ########divisas##########
            divisa['id'] = dato['divisa_id']
            divisa['nombre'] = dato['divisa_nombre']
            divisa['id_pais'] = dato['divisa_id_pais']
            #######paises###########
            pais['id'] = dato['pais_id']
            pais['nombre'] = dato['pais_nombre']
            pais['nacionalidad'] = dato['pais_nacionalidad']
            #####combinacion######
            divisa['pais'] = pais
            divisas.append(divisa)
        divisas = [Divisa.model(**divisa) for divisa in divisas]
        divisas.sort(key=lambda x: x.id)
        return divisas
    

class DivisaCreateAPIView(generics.CreateAPIView):
    serializer_class = DivisaSerializer

class DivisaRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    El unico atributo que se puede modificar es el atributo nombre de divisa, así que utilizar patch para
    solo modificar eso
    """
    serializer_class = DivisaSerializer
    
    @conectar
    def get_object(self,connection):
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
        paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad FROM divisas INNER JOIN paises ON paises.id = divisas.id_pais WHERE divisas.id=%s""",(self.kwargs.get('id'),))
        dato = cursor.fetchone()
        if dato:
            divisa = {}
            pais = {}
            ########divisas##########
            divisa['id'] = dato['divisa_id']
            divisa['nombre'] = dato['divisa_nombre']
            divisa['id_pais'] = dato['divisa_id_pais']
            #######paises###########
            pais['id'] = dato['pais_id']
            pais['nombre'] = dato['pais_nombre']
            pais['nacionalidad'] = dato['pais_nacionalidad']
            #####combinacion######
            divisa['pais'] = pais
            return Divisa.model(**divisa)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM divisas WHERE id = %s",(instance.id,))
        connection.commit()

