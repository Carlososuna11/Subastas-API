from rest_framework import generics
from database.conexion import conectar
from apps.eventos.api.serializers.costoEnvio import *
from apps.eventos.models import CostoEnvio
from django.http import Http404
import inspect

class CostoEnvioListAPIView(generics.ListAPIView):
    # """
    # Este endpoint cuenta con un query param, que es id_pais, lo que hace es filtrar
    # las divisas según el pais ejemplo: http://127.0.0.1:8000/commons/divisa/?id_pais=2
    # """
    serializer_class = CostoEnvioSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        pais = ['id','nombre','nacionalidad']
        costoEnvio = ['id','id_evento','costoExtra','id_pais']
        query_action = f"""SELECT 
                    {', '.join([f'paises.{i} as pais_{i}' for i in pais])},
                    {', '.join([f'costoEnvios.{i} as costoEnvio_{i}' for i in costoEnvio])}
                    FROM costoEnvios
                    INNER JOIN paises 
                    ON paises.id = costoEnvios.id_pais
                    """
        # query = self.request.query_params.get('id_pais',None)
        # query_action = f"""SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
        #                     paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
        #                 FROM divisas 
        #                 INNER JOIN paises ON paises.id = divisas.id_pais"""
        # if query:
        #     query_action = """SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
        #                     paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
        #                     FROM divisas 
        #                     INNER JOIN paises ON paises.id = divisas.id_pais
        #                     WHERE divisas.id_pais = %s
        #                     """
        #     cursor.execute(query_action,(query,))
        # else:
        cursor.execute(query_action)
        #print(pais_quey,id_pais_query)
        costosEnvios = []
        for dato in cursor:
            costoData = {}
            paisData = {}
            for i in costoEnvio:
                costoData[f'{i}'] = dato[f'costoEnvio_{i}']
            for i in pais:
                paisData[f'{i}'] = dato[f'pais_{i}']
            costoData['pais'] = paisData
            costosEnvios.append(costoData)
        divisas = [CostoEnvio.model(**costo) for costo in costosEnvios]
        divisas.sort(key=lambda x: x.id)
        return divisas
    

class CostoEnvioCreateAPIView(generics.CreateAPIView):
    serializer_class = CostoEnvioSerializer

class CostoEnvioRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    El unico atributo que se puede modificar es el atributo nombre de divisa, así que utilizar patch para
    solo modificar eso
    """
    serializer_class = CostoEnvioSerializer
    
    @conectar
    def get_object(self,connection):
        
        cursor = connection.cursor(dictionary=True)
        pais = ['id','nombre','nacionalidad']
        costoEnvio = ['id','id_evento','costoExtra','id_pais']
        query_action = f"""SELECT 
                    {', '.join([f'paises.{i} as pais_{i}' for i in pais])},
                    {', '.join([f'costoEnvios.{i} as costoEnvio_{i}' for i in costoEnvio])}
                    FROM costoEnvios
                    INNER JOIN paises 
                    ON paises.id = costoEnvios.id_pais
                    WHERE costoEnvios.id = %s
                    """
        cursor.execute(query_action,(self.kwargs.get('id'),))
        dato = cursor.fetchone()
        if dato:
            costoData = {}
            paisData = {}
            for i in costoEnvio:
                costoData[f'{i}'] = dato[f'costoEnvio_{i}']
            for i in pais:
                paisData[f'{i}'] = dato[f'pais_{i}']
            costoData['pais'] = paisData
            return CostoEnvio.model(**costoData)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM costoEnvios WHERE id = %s",(instance.id,))
        connection.commit()

