from rest_framework import generics
from database.conexion import conectar
from apps.eventos.api.serializers import *
from apps.commons.models import Pais
from apps.organizaciones.models import *
from django.http import Http404


class EventoListAPIView(generics.ListAPIView):
    serializer_class = EventoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        pais = ['id','nombre','nacionalidad']
        # organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
        #                 'paginaWeb','emailCorporativo','id_pais']
        evento = ['id','inscripcionCliente','inscripcionClienteNuevo','fecha','status',
                'tipo','tipoPuja','duracionHoras','lugar','id_pais']
        # query_action = f"""SELECT * 
        #                 FROM (SELECT {', '.join([f'{i} as organizacion_{i}' for i in organizacion])} FROM organizaciones) as `Evento`
        #                 INNER JOIN (SELECT {', '.join([f'{i} as pais_{i}' for i in pais])} FROM paises) as `Pais`
        #                 ON `Pais`.pais_id = `Evento`.organizacion_id_pais
        #                 """
        query_action =  f"""SELECT 
                        {', '.join([f'eventos.{i} as evento_{i}' for i in evento])},
                        {', '.join([f'paises.{i} as pais_{i}' for i in pais])}
                        FROM eventos
                        LEFT JOIN paises
                        ON paises.id = eventos.id_pais
                        """
        print(query_action)
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
        organizaciones = []
        for dato in cursor:
            organizacionData = {}
            paisReside = {}
            for i in evento:
                organizacionData[f'{i}'] = dato[f'evento_{i}']
            for i in pais:
                paisReside[f'{i}'] = dato[f'pais_{i}']
            organizacionData['pais']= paisReside
            organizaciones.append(organizacionData)
        organizaciones = [Evento.model(**dato) for dato in organizaciones]
        organizaciones.sort(key=lambda x: x.fecha)
        return organizaciones
    

class EventoCreateAPIView(generics.CreateAPIView):
    serializer_class = EventoSerializer

class EventoRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = EventoSerializer
    
    @conectar
    def get_object(self,connection):
        pais = ['id','nombre','nacionalidad']
        # organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
        #                 'paginaWeb','emailCorporativo','id_pais']
        evento = ['id','inscripcionCliente','inscripcionClienteNuevo','fecha','status',
                'tipo','tipoPuja','duracionHoras','lugar','id_pais']
        # query_action = f"""SELECT * 
        #                 FROM (SELECT {', '.join([f'{i} as organizacion_{i}' for i in organizacion])} FROM organizaciones) as `Evento`
        #                 INNER JOIN (SELECT {', '.join([f'{i} as pais_{i}' for i in pais])} FROM paises) as `Pais`
        #                 ON `Pais`.pais_id = `Evento`.organizacion_id_pais
        #                 """
        query_action =  f"""SELECT 
                        {', '.join([f'eventos.{i} as evento_{i}' for i in evento])},
                        {', '.join([f'paises.{i} as pais_{i}' for i in pais])}
                        FROM eventos
                        LEFT JOIN paises
                        ON paises.id = eventos.id_pais
                        WHERE eventos.id = %s
                        """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query_action,(self.kwargs.get('id'),))
        dato = cursor.fetchone()
        if dato:
            organizacionData = {}
            paisReside = {}
            for i in evento:
                organizacionData[f'{i}'] = dato[f'evento_{i}']
            for i in pais:
                paisReside[f'{i}'] = dato[f'pais_{i}']
            organizacionData['pais']= paisReside
            return Evento.model(**organizacionData)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM eventos WHERE id = %s",(instance.id,))
        connection.commit()

