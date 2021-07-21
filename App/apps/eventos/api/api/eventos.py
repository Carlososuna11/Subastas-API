from rest_framework import generics
from database.conexion import conectar
from apps.eventos.api.serializers import *
from apps.commons.models import Pais
from apps.organizaciones.models import *
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed, ValidationError
import jwt, datetime
from django.conf import settings
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class EventoListAPIView(generics.ListAPIView):
    serializer_class = EventoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        # print(self.request.COOKIES.get('TOKEN'))
        token = self.request.META.get('HTTP_TOKEN',None)
        if not token:
            token = self.request.COOKIES.get('TOKEN',None)
        self.request.data['jwt']= None
        if token:    
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('No Autorizado!')
            self.request.data['jwt'] = payload
        # if payload['tipo'] != 'coleccionista':
        #     raise AuthenticationFailed('No Autorizado!')
        
        #query = self.request.query_params.get('id_pais',None)
        pais = ['id','nombre','nacionalidad']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        planificador = ['id_organizacion','id_evento']
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
                        {', '.join([f'caj_eventos.{i} as evento_{i}' for i in evento])},
                        {', '.join([f'pais_evento.{i} as pais_evento_{i}' for i in pais])},
                        {', '.join([f'caj_planificadores.{i} as planificador_{i}' for i in planificador])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'caj_paises.{i} as pais_{i}' for i in pais])}
                        FROM caj_eventos
                        LEFT JOIN caj_paises as pais_evento
                        ON pais_evento.id = caj_eventos.id_pais
                        LEFT JOIN caj_planificadores
                        ON caj_planificadores.id_evento = caj_eventos.id
                        LEFT JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_planificadores.id_organizacion
                        LEFT JOIN caj_paises
                        ON caj_organizaciones.id_pais = caj_paises.id
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
        eventos ={}
        eventos_id = []
        for dato in cursor:
            organizacionData= {}
            paisO = {}
            if dato['evento_id'] not in eventos_id:
                eventoData = {}
                paisReside = {}
                for i in evento:
                    eventoData[f'{i}'] = dato[f'evento_{i}']
                for i in pais:
                    paisReside[f'{i}'] = dato[f'pais_evento_{i}']
                eventoData['pais']= paisReside
                eventoData['planificadores'] =[]
                eventos[dato['evento_id']] = eventoData
                eventos_id.append(dato['evento_id'])
            for i in pais:
                paisO[f'{i}'] = dato[f'pais_{i}']
            for i in organizacion:
                organizacionData[f'{i}'] = dato[f'organizacion_{i}']
            organizacionData['pais'] = paisO
            eventos[dato['evento_id']]['planificadores'].append(Organizacion.model(**organizacionData))
        organizaciones = [Evento.model(**dato) for dato in eventos.values()]
        organizaciones.sort(key=lambda x: x.fecha)
        return organizaciones
    
    @conectar
    def finalize_response(self, request, response,connection, *args, **kwargs):
        cursor = connection.cursor(dictionary=True)
        mysql_query_get = """SELECT * FROM caj_participantes WHERE id_coleccionista_cliente = %s AND id_evento = %s"""
        usuario = self.request.data['jwt']
        if usuario:
            if usuario['tipo'] == 'coleccionista':
                for evento in response.data:
                    cursor.execute(mysql_query_get,(usuario['id'],evento['id']))
                    inscrito = False
                    if cursor.fetchone():
                        inscrito = True
                    evento['inscrito'] = inscrito
        return super().finalize_response(request, response, *args, **kwargs)
class EventoPorOrganizacionListAPIView(generics.ListAPIView):
    serializer_class = EventoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        # token = 
        token = self.request.META.get('HTTP_TOKEN',None)
        if not token:
            token = self.request.COOKIES.get('TOKEN',None)
        self.request.data['jwt']= None
        if token:    
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('No Autorizado!')
            self.request.data['jwt'] = payload
        pais = ['id','nombre','nacionalidad']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        planificador = ['id_organizacion','id_evento']
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
                        {', '.join([f'caj_eventos.{i} as evento_{i}' for i in evento])},
                        {', '.join([f'pais_evento.{i} as pais_evento_{i}' for i in pais])},
                        {', '.join([f'caj_planificadores.{i} as planificador_{i}' for i in planificador])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'caj_paises.{i} as pais_{i}' for i in pais])}
                        FROM caj_eventos
                        LEFT JOIN caj_paises as pais_evento
                        ON pais_evento.id = caj_eventos.id_pais
                        LEFT JOIN caj_planificadores
                        ON caj_planificadores.id_evento = caj_eventos.id
                        LEFT JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_planificadores.id_organizacion
                        LEFT JOIN caj_paises
                        ON caj_organizaciones.id_pais = caj_paises.id
                        """
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
        id_organizacion = self.kwargs.get('id')
        print(id_organizacion)
        eventos ={}
        eventos_id = []
        for dato in cursor:
            organizacionData= {}
            paisO = {}
            if dato['evento_id'] not in eventos_id:
                eventoData = {}
                paisReside = {}
                for i in evento:
                    eventoData[f'{i}'] = dato[f'evento_{i}']
                for i in pais:
                    paisReside[f'{i}'] = dato[f'pais_evento_{i}']
                eventoData['pais']= paisReside
                eventoData['planificadores'] =[]
                eventos[dato['evento_id']] = eventoData
                eventos_id.append(dato['evento_id'])
            for i in pais:
                paisO[f'{i}'] = dato[f'pais_{i}']
            for i in organizacion:
                organizacionData[f'{i}'] = dato[f'organizacion_{i}']
            organizacionData['pais'] = paisO
            eventos[dato['evento_id']]['planificadores'].append(Organizacion.model(**organizacionData))
        final = []
        for i in eventos.values():
            for j in i['planificadores']:
                if id_organizacion == j.id:
                    final.append(i)
        organizaciones = [Evento.model(**dato) for dato in final]
        organizaciones.sort(key=lambda x: x.fecha)
        return organizaciones

    @conectar
    def finalize_response(self, request, response,connection, *args, **kwargs):
        cursor = connection.cursor(dictionary=True)
        mysql_query_get = """SELECT * FROM caj_participantes WHERE id_coleccionista_cliente = %s AND id_evento = %s"""
        usuario = self.request.data['jwt']
        if usuario:
            if usuario['tipo'] == 'coleccionista':
                for evento in response.data:
                    cursor.execute(mysql_query_get,(usuario['id'],evento['id']))
                    inscrito = False
                    if cursor.fetchone():
                        inscrito = True
                    evento['inscrito'] = inscrito
        return super().finalize_response(request, response, *args, **kwargs)
class EventoCreateAPIView(generics.CreateAPIView):
    serializer_class = EventoSerializer

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        if payload['tipo'] != 'organizacion':
            raise AuthenticationFailed('No Autorizado!')
        planificadores  = request.data.get('planificadores',[]).copy()
        planificadores.append(payload['id'])
        request.data['planificadores'] = planificadores
        return self.create(request, *args, **kwargs)
class EventoRetriveDestroyAPIView(generics.RetrieveDestroyAPIView):

    serializer_class = EventoSerializer
    
    @conectar
    def get_object(self,connection):
        pais = ['id','nombre','nacionalidad']
        # organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
        #                 'paginaWeb','emailCorporativo','id_pais']
        evento = ['id','inscripcionCliente','inscripcionClienteNuevo','fecha','status',
                'tipo','tipoPuja','duracionHoras','lugar','id_pais']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        planificador = ['id_organizacion','id_evento']
        # query_action = f"""SELECT * 
        #                 FROM (SELECT {', '.join([f'{i} as organizacion_{i}' for i in organizacion])} FROM organizaciones) as `Evento`
        #                 INNER JOIN (SELECT {', '.join([f'{i} as pais_{i}' for i in pais])} FROM paises) as `Pais`
        #                 ON `Pais`.pais_id = `Evento`.organizacion_id_pais
        #                 """
        query_action =  f"""SELECT 
                        {', '.join([f'caj_eventos.{i} as evento_{i}' for i in evento])},
                        {', '.join([f'pais_evento.{i} as pais_evento_{i}' for i in pais])},
                        {', '.join([f'caj_planificadores.{i} as planificador_{i}' for i in planificador])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'caj_paises.{i} as pais_{i}' for i in pais])}
                        FROM caj_eventos
                        LEFT JOIN caj_paises as pais_evento
                        ON pais_evento.id = caj_eventos.id_pais
                        LEFT JOIN caj_planificadores
                        ON caj_planificadores.id_evento = caj_eventos.id
                        LEFT JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_planificadores.id_organizacion
                        LEFT JOIN caj_paises
                        ON caj_organizaciones.id_pais = caj_paises.id
                        WHERE caj_eventos.id = %s
                        """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query_action,(self.kwargs.get('id'),))
        datos = cursor.fetchall()
        if datos:
            eventos =None
            eventos_id = []
            for dato in datos:
                organizacionData= {}
                paisO = {}
                if dato['evento_id'] not in eventos_id:
                    eventoData = {}
                    paisReside = {}
                    for i in evento:
                        eventoData[f'{i}'] = dato[f'evento_{i}']
                    for i in pais:
                        paisReside[f'{i}'] = dato[f'pais_evento_{i}']
                    eventoData['pais']= paisReside
                    eventoData['planificadores'] =[]
                    eventos_id.append(dato['evento_id'])
                    eventos = eventoData
                for i in pais:
                    paisO[f'{i}'] = dato[f'pais_{i}']
                for i in organizacion:
                    organizacionData[f'{i}'] = dato[f'organizacion_{i}']
                organizacionData['pais'] = paisO
                eventos['planificadores'].append(Organizacion.model(**organizacionData))   
            return Evento.model(**eventos)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM caj_eventos WHERE id = %s",(instance.id,))
        connection.commit()

class UpdatePricesView(APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            # 'id_evento': openapi.Schema(type=openapi.TYPE_INTEGER, description='id del evento'),
            'inscripcionCliente': openapi.Schema(type=openapi.TYPE_NUMBER, description='inscripcion cliente'),
            'inscripcionClienteNuevo': openapi.Schema(description='inscripcion cliente Nuevo',type=openapi.TYPE_NUMBER),
        }
    ))
    @conectar
    def post(self,request,id,connection):
        cursor = connection.cursor(dictionary=True)
        inscripcionCliente = request.data['inscripcionCliente']
        inscripcionClienteNuevo = request.data.get('inscripcionClienteNuevo',None)
        mysql_query_get = """SELECT * FROM caj_eventos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id,))
        evento = cursor.fetchone()
        if evento is None:
            raise ValidationError('El evento No existe')
        mysq_query_update = """UPDATE caj_eventos SET inscripcionCliente = %s, inscripcionClienteNuevo = %s WHERE id=%s"""
        cursor.execute(mysq_query_update,(inscripcionCliente,inscripcionClienteNuevo,id))
        connection.commit()
        response = Response()
        response.data = {
            'sucess': 'Se han actualizado los precios'
        }

        return response

class CancelEventView(APIView):

    @conectar
    def post(self,request,id,connection):
        cursor = connection.cursor(dictionary=True)
        mysql_query_get = """SELECT * FROM caj_eventos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id,))
        evento = cursor.fetchone()
        if evento is None:
            raise ValidationError('El evento No existe')
        mysq_query_update = """UPDATE caj_eventos SET status = %s WHERE id=%s"""
        cursor.execute(mysq_query_update,('cancelado',id))
        connection.commit()
        response = Response()
        response.data = {
            'sucess': 'Se cancelado el Evento'
        }
        return response