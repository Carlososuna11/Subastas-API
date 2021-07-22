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
import json
class EventoListAPIView(generics.ListAPIView):
    serializer_class = EventoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        # print(self.request.COOKIES.get('TOKEN'))
        token = self.request.META.get('HTTP_TOKEN',None)
        if token == 'false':
            token = None
        if not token:
            token = self.request.COOKIES.get('TOKEN',None)
        self.request.data['jwt']= None
        if token:    
            try:
                print(token)
                payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('No Autorizado!')
            self.request.data['jwt'] = payload
        # if payload['tipo'] != 'coleccionista':
        #     raise AuthenticationFailed('No Autorizado!')
        msyql_get_eventos = """SELECT * FROM caj_eventos"""
        cursor.execute(msyql_get_eventos)
        eventos = cursor.fetchall()
        if eventos:
            for i in eventos:
                if i['fecha'] < datetime.date.today():
                    if i['status'] == 'pendiente':
                        i['status'] = 'cancelado'
                        mysql_update_evento = """UPDATE caj_eventos SET status = 'cancelado' WHERE id = %s"""
                        cursor.execute(mysql_update_evento,(i['id'],))
            connection.commit()
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
                    evento['esHoy'] = False
                    if evento['fecha'] == datetime.date.today().strftime('%d-%m-%Y'):
                        evento['esHoy'] = True
            else:
                mysql_query_get = """SELECT * FROM caj_planificadores WHERE id_organizacion = %s AND id_evento = %s"""
                for evento in response.data:
                    cursor.execute(mysql_query_get,(usuario['id'],evento['id']))
                    inscrito = False
                    if cursor.fetchone():
                        inscrito = True
                    evento['planificador'] = inscrito
                    evento['esHoy'] = False
                    evento['planificador'] = inscrito
                    if evento['fecha'] == datetime.date.today().strftime('%d-%m-%Y'):
                        evento['esHoy'] = True
        return super().finalize_response(request, response, *args, **kwargs)
class EventoPorOrganizacionListAPIView(generics.ListAPIView):
    serializer_class = EventoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        # token = 
        token = self.request.META.get('HTTP_TOKEN',None)
        if token == 'false':
            token = None
        if not token:
            token = self.request.COOKIES.get('TOKEN',None)
        self.request.data['jwt']= None
        if token:    
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('No Autorizado!')
            self.request.data['jwt'] = payload
        msyql_get_eventos = """SELECT * FROM caj_eventos"""
        cursor.execute(msyql_get_eventos)
        eventos = cursor.fetchall()
        if eventos:
            for i in eventos:
                if i['fecha'] < datetime.date.today():
                    if i['status'] == 'pendiente':
                        i['status'] = 'cancelado'
                        mysql_update_evento = """UPDATE caj_eventos SET status = 'cancelado' WHERE id = %s"""
                        cursor.execute(mysql_update_evento,(i['id'],))
            connection.commit()
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
                    evento['esHoy'] = False
                    if evento['fecha'] == datetime.date.today().strftime('%d-%m-%Y'):
                        evento['esHoy'] = True
            else:
                mysql_query_get = """SELECT * FROM caj_planificadores WHERE id_organizacion = %s AND id_evento = %s"""
                for evento in response.data:
                    cursor.execute(mysql_query_get,(usuario['id'],evento['id']))
                    inscrito = False
                    if cursor.fetchone():
                        inscrito = True
                    evento['esHoy'] = False
                    evento['planificador'] = inscrito
                    if evento['fecha'] == datetime.date.today().strftime('%d-%m-%Y'):
                        evento['esHoy'] = True
        return super().finalize_response(request, response, *args, **kwargs)
class EventoCreateAPIView(generics.CreateAPIView):
    serializer_class = EventoSerializer

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN',None)
        if token == 'false':
            token = None
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
        token = self.request.META.get('HTTP_TOKEN',None)
        if token == 'false':
            token = None
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

    @conectar
    def finalize_response(self, request, response,connection, *args, **kwargs):
        cursor = connection.cursor(dictionary=True)
        mysql_query_get = """SELECT * FROM caj_participantes WHERE id_coleccionista_cliente = %s AND id_evento = %s"""
        usuario = self.request.data['jwt']
        evento = response.data
        if usuario:
            if usuario['tipo'] == 'coleccionista':
                cursor.execute(mysql_query_get,(usuario['id'],evento['id']))
                inscrito = False
                if cursor.fetchone():
                    inscrito = True
                evento['inscrito'] = inscrito
            else:
                mysql_query_get = """SELECT * FROM caj_planificadores WHERE id_organizacion = %s AND id_evento = %s"""
                cursor.execute(mysql_query_get,(usuario['id'],evento['id']))
                inscrito = False
                if cursor.fetchone():
                    inscrito = True
                evento['planificador'] = inscrito
        evento['esHoy'] = False
        if evento['fecha'] == datetime.date.today().strftime('%d-%m-%Y'):
            evento['esHoy'] = True
        return super().finalize_response(request, response, *args, **kwargs)
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

class ComenzarEvento(APIView):

    @conectar
    def post(self,request,id,connection):
        cursor = connection.cursor(dictionary=True)
        mysql_query_get = """SELECT * FROM caj_eventos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id,))
        evento = cursor.fetchone()
        if evento is None:
            raise ValidationError('El evento No existe')
        
        if evento['status']== 'cancelado':
            raise ValidationError('El evento ya esta cancelado')
        if evento['status']=='realizado':
            raise ValidationError('El evento ya esta finalizado')
        if evento['status']=='progreso':
            raise ValidationError('El evento ya esta en progreso')
        mysq_query_update = """UPDATE caj_eventos SET status = %s WHERE id=%s"""
        cursor.execute(mysq_query_update,('progreso',id))
        mysql_lista_Objetos = """SELECT * FROM caj_Lista_Objetos where id_evento = %s"""
        cursor.execute(mysql_lista_Objetos,(id,))
        objetos = cursor.fetchall()
        if objetos is None:
            raise ValidationError('No hay objetos para el evento')
        mysql_insert_subasta_activa = """INSERT INTO caj_Subastas_Activas (id_evento,id_objeto,hora_inicio,hora_fin,cierre) VALUES (%s,%s,%s,%s,%s)"""
        hora_inicio = datetime.datetime.now()
        horax_inicio = datetime.datetime.now()
        # hora_fin = hora_inicio + timedelta(minutes=30)
        hora_fin = hora_inicio
        for objeto in objetos:
            if evento['tipo'] == 'virtual':
                hora_fin = horax_inicio+ datetime.timedelta(minutes=float(objeto['duracionmin']))
            else:
                print(objeto['duracionmin'])
                hora_fin = hora_fin +  datetime.timedelta(minutes=float(objeto['duracionmin']))
            cursor.execute(mysql_insert_subasta_activa,(id,objeto['id'],hora_inicio,hora_fin,False))
            if evento['tipo'] != 'virtual':
                hora_inicio = hora_fin
        connection.commit()
        response = Response()
        response.data = {
            'sucess': 'Se ha Activado El evento'
        }
        return response

class PujaDinamica(APIView):
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'precio': openapi.Schema(type=openapi.TYPE_NUMBER, description='precio a pujar'),
        }
    ))
    @conectar
    #necesito el token
    def post(self,request,id,connection):
        cursor = connection.cursor(dictionary=True)
        precio = float(request.data['precio'])
        token =request.META.get('HTTP_TOKEN',None)
        if token == 'false':
            token = None
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        if payload['tipo'] == 'organizacion':
            raise AuthenticationFailed('No Autorizado!')
        #-----Es participante------
        mysql_query_get = """SELECT * FROM caj_Lista_Objetos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id,))
        objeto = cursor.fetchone()
        mysql_participante_get = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente,id_evento)= (%s,%s)"""
        cursor.execute(mysql_participante_get,(payload['id'],objeto['id_evento']))
        if cursor.fetchone() is None:
            raise AuthenticationFailed('No Participas a este Evento')
        mysql_query_subastaActiva = """SELECT * FROM caj_Subastas_Activas WHERE id_objeto = %s"""
        cursor.execute(mysql_query_subastaActiva,(id,))
        subastaActiva = cursor.fetchone()
        tiempoActual = datetime.datetime.now()
        if subastaActiva['hora_inicio'] <tiempoActual and tiempoActual < subastaActiva['hora_fin']:
            if precio <= objeto['precioAlcanzado']:
                raise ValidationError('No se puede pujar menos')
            else:
                mysql_cantidad_get = """SELECT * FROM caj_Logs_Subastas_Activas WHERE id_subasta_activa = %s"""
                cursor.execute(mysql_cantidad_get,(subastaActiva['id'],))
                precios = [float(i['precio']) for i in cursor.fetchall()] 
                mysql_query_update_precio = """UPDATE caj_Lista_Objetos SET precioAlcanzado = %s WHERE id=%s"""
                cursor.execute(mysql_query_update_precio,(precio,id))
                mysql_query_update = """UPDATE caj_Lista_Objetos SET bid = %s WHERE id=%s"""
                cursor.execute(mysql_query_update,((sum(precios)+precio)/(len(precios)+1),id))
                mysql_insert_log = """INSERT INTO caj_Logs_Subastas_Activas (id_subasta_activa,id_coleccionista,precio,hora) VALUES (%s,%s,%s,%s)"""
                cursor.execute(mysql_insert_log,(subastaActiva['id'],payload['id'],precio,tiempoActual))
                connection.commit()
        else:
            raise ValidationError('No se puede pujar')
        response = Response()
        response.data = {
            'sucess': 'Se ha pujado Exitosamente'
        }
        return response

class PujaSobreCerrado(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            # 'kid_evento': openapi.Schema(type=openapi.TYPE_INTEGER, description='id del evento'),
            'precio': openapi.Schema(type=openapi.TYPE_NUMBER, description='precio a pujar')
        }
    ))
    @conectar
    #necesito el token
    def post(self,request,id,connection):
        cursor = connection.cursor(dictionary=True)
        precio = float(request.data['precio'])
        token = request.META.get('HTTP_TOKEN')
        if token == 'false':
            token = None
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        if payload['tipo'] == 'organizacion':
            raise AuthenticationFailed('No Autorizado!')
        mysql_query_get = """SELECT * FROM caj_Lista_Objetos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id,))
        objeto = cursor.fetchone()
        mysql_participante_get = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente,id_evento)= (%s,%s)"""
        cursor.execute(mysql_participante_get,(payload['id'],objeto['id_evento']))
        if cursor.fetchone() is None:
            raise AuthenticationFailed('No Participas a este Evento')
        mysql_query_subastaActiva = """SELECT * FROM caj_Subastas_Activas WHERE id_objeto = %s"""
        cursor.execute(mysql_query_subastaActiva,(id,))
        subastaActiva = cursor.fetchone()
        tiempoActual = datetime.datetime.now()
        if subastaActiva['hora_inicio'] <tiempoActual and tiempoActual < subastaActiva['hora_fin']:
                mysql_log_get = """SELECT * FROM caj_Logs_Subastas_Activas WHERE (id_subasta_activa,id_coleccionista) = (%s,%s)"""
                cursor.execute(mysql_log_get,(subastaActiva['id'],payload['id']))
                if cursor.fetchone():
                    raise ValidationError('Ya ha pujado')
                if precio > objeto['precioAlcanzado']:
                    mysql_query_update = """UPDATE caj_Lista_Objetos SET precioAlcanzado = %s WHERE id=%s"""
                    cursor.execute(mysql_query_update,(precio,id))
                mysql_cantidad_get = """SELECT * FROM caj_Logs_Subastas_Activas WHERE id_subasta_activa = %s"""
                cursor.execute(mysql_cantidad_get,(subastaActiva['id'],))
                precios = [float(i['precio']) for i in cursor.fetchall()] 
                mysql_query_update = """UPDATE caj_Lista_Objetos SET bid = %s WHERE id=%s"""
                cursor.execute(mysql_query_update,((sum(precios)+precio)/(len(precios)+1),id))
                mysql_insert_log = """INSERT INTO caj_Logs_Subastas_Activas (id_subasta_activa,id_coleccionista,precio,hora) VALUES (%s,%s,%s,%s)"""
                cursor.execute(mysql_insert_log,(subastaActiva['id'],payload['id'],precio,tiempoActual))
                connection.commit()
        else:
            raise ValidationError('No se puede pujar')
        response = Response()
        response.data = {
            'sucess': 'Se ha pujado Exitosamente'
        }
        return response


class ActualizarStatus(APIView):
    @conectar
    def post(self,request,connection):
        cursor = connection.cursor(dictionary=True)
        mysql_query_get = """SELECT * FROM caj_Subastas_Activas WHERE cierre = %s"""
        cursor.execute(mysql_query_get,(False,))
        subastasActivas = cursor.fetchall()
        for subastaActiva in subastasActivas:
            if subastaActiva['hora_fin'] < datetime.datetime.now():
                mysql_query_get_evento = """SELECT * FROM caj_eventos WHERE id = %s"""
                cursor.execute(mysql_query_get_evento,(subastaActiva['id_evento'],))
                evento = cursor.fetchone()
                if evento['status'] == 'progreso':
                    mysql_query_get = """SELECT * FROM caj_Logs_Subastas_Activas WHERE id_subasta_activa=%s"""
                    cursor.execute(mysql_query_get,(subastaActiva['id'],))
                    logs = cursor.fetchall()
                    if logs:
                        mysql_query_get_lista = """SELECT * FROM caj_Lista_Objetos WHERE id = %s"""
                        cursor.execute(mysql_query_get_lista,(subastaActiva['id_objeto'],))
                        objeto = cursor.fetchone()
                        objeto['precioAlcanzado'] = float(objeto['precioAlcanzado'])
                        objeto['bid'] = float(objeto['bid'])
                        objeto['ask'] = float(objeto['ask'])
                        if objeto['precioAlcanzado'] < objeto['ask']:
                            mysql_query_update = """UPDATE caj_Lista_Objetos SET razonNoVenta = %s WHERE id = %s"""
                            cursor.execute(mysql_query_update,('inferior al ask',objeto['id']))
                            connection.commit()
                            continue
                        logs = sorted(logs, key=lambda x: (-x['precio'], x['hora']))[0]
                        # mysql_get_organizacion = """SELECT * FROM caj_Lista_O WHERE id = %s""")
                        organizacion = None
                        if objeto['nur_moneda']:
                            mysql_query_get_moneda = """SELECT * FROM caj_Catalogo_Moneda_Tienda WHERE nur = %s"""
                            cursor.execute(mysql_query_get_moneda,(objeto['nur_moneda'],))
                            organizacion = cursor.fetchone()['id_organizacion']
                        else:
                            mysql_query_get_moneda = """SELECT * FROM caj_Catalogo_Pintura_Tienda WHERE nur = %s"""
                            cursor.execute(mysql_query_get_moneda,(objeto['id_pintura'],))
                            organizacion = cursor.fetchone()['id_organizacion']
                        mysql_query_participante = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente, id_organizacion_cliente,id_evento) = (%s,%s,%s)"""
                        cursor.execute(mysql_query_participante,(logs['id_coleccionista'],organizacion,evento['id']))
                        participante = cursor.fetchone()
                        mysql_update_objeto = """UPDATE caj_Lista_Objetos SET id_eventoParticipante= %s,fechaIngresoParticipante=%s,
                        id_coleccionistaParticipante=%s,id_organizacionParticipante=%s WHERE id = %s"""
                        cursor.execute(mysql_update_objeto,(participante['id_evento'],participante['fechaIngresoCliente'],participante['id_coleccionista_cliente'],organizacion,objeto['id']))
                        connection.commit()
                    else:
                        mysql_query_update = """UPDATE caj_Lista_Objetos SET razonNoVenta = %s WHERE id = %s"""
                        cursor.execute(mysql_query_update,('sin ofertas',subastaActiva['id_objeto']))
                        connection.commit()
                    mysql_query_update = """UPDATE caj_Subastas_Activas SET cierre = %s WHERE id = %s"""
                    cursor.execute(mysql_query_update,(True,subastaActiva['id']))
                connection.commit()
        mysql_evento_get = """SELECT * FROM caj_eventos WHERE status = 'progreso'"""
        cursor.execute(mysql_evento_get)
        eventos = cursor.fetchall()
        for evento in eventos:
            mysql_query_subastas_activas = """SELECT * FROM caj_Subastas_Activas WHERE id_evento = %s AND cierre = %s"""
            cursor.execute(mysql_query_subastas_activas,(evento['id'],False))
            if not cursor.fetchall():
                facturas = {} #uso id organizacion y eventop de participante como clave
                #------Generar Facturas y actualizar status ----------
                mysql_query_lista_objetos = """SELECT * FROM caj_Lista_Objetos WHERE id_evento = %s"""
                cursor.execute(mysql_query_lista_objetos,(evento['id'],))
                lista_objetos = cursor.fetchall()
                for objeto in lista_objetos:
                    if objeto['id_coleccionistaParticipante']:
                        if not(facturas.get(objeto['id_eventoParticipante'],None)):
                            facturas[objeto['id_eventoParticipante']] = []
                        facturas[objeto['id_eventoParticipante']].append(objeto)
                        if objeto['nur_moneda']:
                            mysql_update_query = """UPDATE caj_Catalogo_Moneda_Tienda SET id_coleccionista =%s, id_organizacion=%s WHERE nur = %s"""
                            cursor.execute(mysql_update_query,(objeto['id_coleccionistaParticipante'],None,objeto['nur_moneda']))
                    connection.commit()
                for key,value in facturas.items():
                    fatcs = {}
                    total = {}
                    for objeto in value:
                        if not fatcs.get((objeto['id_organizacionParticipante'],objeto['id_coleccionistaParticipante']),None):
                            fatcs[(objeto['id_organizacionParticipante'],objeto['id_coleccionistaParticipante'])] = [] 
                        if not total.get((objeto['id_organizacionParticipante'],objeto['id_coleccionistaParticipante']),None):
                            total[(objeto['id_organizacionParticipante'],objeto['id_coleccionistaParticipante'])] = 0
                        total[(objeto['id_organizacionParticipante'],objeto['id_coleccionistaParticipante'])] += objeto['precioAlcanzado']
                        fatcs[(objeto['id_organizacionParticipante'],objeto['id_coleccionistaParticipante'])].append(objeto)
                        mysql_participante = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente,id_organizacion_cliente,id_evento) =( %s,%s,%s)"""
                        cursor.execute(mysql_participante,(objeto['id_coleccionistaParticipante'],objeto['id_organizacionParticipante'],evento['id']))
                        participante = cursor.fetchone()
                        if evento['tipo'] == 'virtual':
                            mysql_costo_envio = """SELECT * FROM caj_costoEnvios WHERE (id_evento,id_pais)=(%s,%s)"""
                            cursor.execute(mysql_costo_envio,(evento['id'],participante['id_pais']))
                            costo_envio = cursor.fetchone()
                            if costo_envio:
                                total[(objeto['id_organizacionParticipante'],objeto['id_coleccionistaParticipante'])] += costo_envio['costoExtra']
                    for key2,value2 in fatcs.items():
                        mysql_participante = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente,id_organizacion_cliente,id_evento) =( %s,%s,%s)"""
                        cursor.execute(mysql_participante,(key2[1],key2[0],evento['id']))
                        participante = cursor.fetchone()
                        mysql_query_factura = """INSERT INTO caj_facturas (id_evento,fechaIngresoParticipante,fechaEmision,total,id_coleccionistaParticipante,id_organizacionParticipante) VALUES (%s,%s,%s,%s,%s,%s)"""
                        cursor.execute(mysql_query_factura,(evento['id'],participante['fechaIngresoCliente'],datetime.date.today(),total[key2],key2[1],key2[0]))
                        connection.commit()
                        id_Factura = cursor.lastrowid
                        for objeto in value2:
                            mysql_insert_det_fact = """INSERT INTO caj_detFacturas (id_evento,id_objeto,numeroFactura,precio) VALUES (%s,%s,%s,%s)"""
                            cursor.execute(mysql_insert_det_fact,(evento['id'],objeto['id'],id_Factura,objeto['precioAlcanzado']))
                        mysql_query_update = """UPDATE caj_eventos SET status = %s WHERE id = %s"""
                        cursor.execute(mysql_query_update,('realizado',evento['id']))
            connection.commit()
        connection.commit()
        response = Response()
        response.data = {
            'sucess': 'Se ha actualizado los registros'
        }
        return response

class GetPujasDinamicaView(APIView):
    @conectar
    def get(self, request,id,connection):
# def validate(request,connection):
        cursor = connection.cursor(dictionary=True)
        token = request.META.get('HTTP_TOKEN',None)
        if token == 'false':
            token = None
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        mysql_query_get = ""
        if payload['tipo'] == 'coleccionista':
            mysql_query_get = """SELECT * from caj_coleccionistas WHERE id = %s"""
        elif payload['tipo']=='organizacion':
            mysql_query_get = """SELECT * from caj_organizaciones WHERE id = %s"""
        cursor.execute(mysql_query_get,(payload['id'],))
        usuario = cursor.fetchone()
        data = {}
        if payload['tipo'] == 'coleccionista':
            mysql_query_get = """SELECT * from caj_Lista_Objetos WHERE id = %s"""
            cursor.execute(mysql_query_get,(id,))
            lista_objetos = cursor.fetchone()
            mysql_query_get = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente,id_evento) = (%s,%s)"""
            cursor.execute(mysql_query_get,(usuario['id'],lista_objetos['id_evento']))
            participante = cursor.fetchone()
            data['participante'] = False
            if participante:
                data['participante']=True
            mysql_query_get = """SELECT * FROM caj_Subastas_Activas WHERE id_objeto = %s"""
            cursor.execute(mysql_query_get,(lista_objetos['id'],))
            subastaActiva = cursor.fetchone()
            mysql_query_get = """SELECT caj_Logs_Subastas_Activas.precio,caj_Logs_Subastas_Activas.hora,
            caj_coleccionistas.nombre,caj_coleccionistas.apellido
            FROM caj_Logs_Subastas_Activas INNER JOIN caj_coleccionistas ON 
            caj_coleccionistas.id = caj_Logs_Subastas_Activas.id_coleccionista
            WHERE caj_Logs_Subastas_Activas.id_subasta_activa = %s"""
            cursor.execute(mysql_query_get,(subastaActiva['id'],))
            logs = cursor.fetchall()
            data['hora_inicio'] = subastaActiva['hora_inicio']
            data['hora_fin'] = subastaActiva['hora_fin']
            data['activa'] = subastaActiva['hora_fin'] > datetime.datetime.now()
            data['comenzo'] = subastaActiva['hora_inicio'] < datetime.datetime.now() 
            data['logs'] = logs
            data['ask'] = lista_objetos['ask']
            data['bid'] = lista_objetos['bid']
            data['precio'] = lista_objetos['precioAlcanzado']
            return Response(data)
        mysql_query_get = """SELECT * from caj_Lista_Objetos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id,))
        lista_objetos = cursor.fetchone()
        mysql_query_get = """SELECT * FROM caj_planificadores WHERE (id_organizacion,id_evento) = (%s,%s)"""
        cursor.execute(mysql_query_get,(usuario['id'],lista_objetos['id_evento']))
        participante = cursor.fetchone()
        data['planificador'] = False
        if participante:
            data['planificador']=True
        mysql_query_get = """SELECT * FROM caj_Subastas_Activas WHERE id_objeto = %s"""
        cursor.execute(mysql_query_get,(lista_objetos['id'],))
        subastaActiva = cursor.fetchone()
        mysql_query_get = """SELECT caj_Logs_Subastas_Activas.precio,caj_Logs_Subastas_Activas.hora,
        caj_coleccionistas.nombre,caj_coleccionistas.apellido
        FROM caj_Logs_Subastas_Activas INNER JOIN caj_coleccionistas ON 
        caj_coleccionistas.id = caj_Logs_Subastas_Activas.id_coleccionista
        WHERE caj_Logs_Subastas_Activas.id_subasta_activa = %s"""
        cursor.execute(mysql_query_get,(subastaActiva['id'],))
        logs = cursor.fetchall()
        data['hora_inicio'] = subastaActiva['hora_inicio']
        data['hora_fin'] = subastaActiva['hora_fin']
        data['activa'] = subastaActiva['hora_fin'] > datetime.datetime.now()
        data['comenzo'] = subastaActiva['hora_inicio'] < datetime.datetime.now() 
        data['logs'] = logs
        data['ask'] = lista_objetos['ask']
        data['bid'] = lista_objetos['bid']
        data['precio'] = lista_objetos['precioAlcanzado']
        return Response(data)

class getEventobySubasta(APIView):

    @conectar
    def get(self, request,id,connection):
        cursor = connection.cursor(dictionary=True)
        mysql_get_evento = """SELECT * FROM caj_Lista_Objetos WHERE id = %s"""
        cursor.execute(mysql_get_evento,(id,))
        lista_objetos = cursor.fetchone()
        mysql_get_evento = """SELECT * FROM caj_eventos WHERE id =%s """
        cursor.execute(mysql_get_evento,(lista_objetos['id_evento'],))
        evento = cursor.fetchone()
        data = {'evento':evento}
        return Response(data)
class GetPujasSobreCerradoView(APIView):
    @conectar
    def get(self, request,id,connection):
# def validate(request,connection):
        cursor = connection.cursor(dictionary=True)
        token = request.META.get('HTTP_TOKEN',None)
        if token == 'false':
            token = None
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        mysql_query_get = ""
        if payload['tipo'] == 'coleccionista':
            mysql_query_get = """SELECT * from caj_coleccionistas WHERE id = %s"""
        elif payload['tipo']=='organizacion':
            mysql_query_get = """SELECT * from caj_organizaciones WHERE id = %s"""
        cursor.execute(mysql_query_get,(payload['id'],))
        usuario = cursor.fetchone()
        data = {}
        if payload['tipo'] == 'coleccionista':
            mysql_query_get = """SELECT * from caj_Lista_Objetos WHERE id = %s"""
            cursor.execute(mysql_query_get,(id,))
            lista_objetos = cursor.fetchone()
            mysql_query_get = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente,id_evento) = (%s,%s)"""
            cursor.execute(mysql_query_get,(usuario['id'],lista_objetos['id_evento']))
            participante = cursor.fetchone()
            data['participante'] = False
            if participante:
                data['participante']=True
            mysql_query_get = """SELECT * FROM caj_Subastas_Activas WHERE id_objeto = %s"""
            cursor.execute(mysql_query_get,(lista_objetos['id'],))
            subastaActiva = cursor.fetchone()
            mysql_query_get = """SELECT * FROM caj_Logs_Subastas_Activas WHERE (id_subasta_activa,id_coleccionista) = (%s,%s)"""
            cursor.execute(mysql_query_get,(subastaActiva['id'],usuario['id']))
            puja = cursor.fetchone()
            data['hora_inicio'] = subastaActiva['hora_inicio']
            data['hora_fin'] = subastaActiva['hora_fin']
            data['comenzo'] = subastaActiva['hora_inicio'] < datetime.datetime.now() 
            data['activa'] = subastaActiva['hora_fin'] > datetime.datetime.now()
            data['pujo'] = False
            if puja:
                data['pujo']=True
                data['pujo_precio'] = puja['precio']
            return Response(data)
        mysql_query_get = """SELECT * from caj_Lista_Objetos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id,))
        lista_objetos = cursor.fetchone()
        mysql_query_get = """SELECT * FROM caj_planificadores WHERE (id_organizacion,id_evento) = (%s,%s)"""
        cursor.execute(mysql_query_get,(usuario['id'],lista_objetos['id_evento']))
        participante = cursor.fetchone()
        data['planificador'] = False
        if participante:
            data['planificador']=True
        mysql_query_get = """SELECT * FROM caj_Subastas_Activas WHERE id_objeto = %s"""
        cursor.execute(mysql_query_get,(lista_objetos['id'],))
        subastaActiva = cursor.fetchone()
        mysql_query_get = """SELECT caj_Logs_Subastas_Activas.precio,caj_Logs_Subastas_Activas.hora,
        caj_coleccionistas.nombre,caj_coleccionistas.apellido
        FROM caj_Logs_Subastas_Activas INNER JOIN caj_coleccionistas ON 
        caj_coleccionistas.id = caj_Logs_Subastas_Activas.id_coleccionista
        WHERE caj_Logs_Subastas_Activas.id_subasta_activa = %s"""
        cursor.execute(mysql_query_get,(subastaActiva['id'],))
        logs = cursor.fetchall()
        data['hora_inicio'] = subastaActiva['hora_inicio']
        data['hora_fin'] = subastaActiva['hora_fin']
        data['comenzo'] = subastaActiva['hora_inicio'] < datetime.datetime.now() 
        data['activa'] = subastaActiva['hora_fin'] > datetime.datetime.now()
        data['logs'] = logs
        data['ask'] = lista_objetos['ask']
        data['bid'] = lista_objetos['bid']
        data['precio'] = lista_objetos['precioAlcanzado']
        return Response(data)


class GETFacturaView(APIView):
    @conectar
    def get(self, request,id,connection):
# def validate(request,connection):
        cursor = connection.cursor(dictionary=True)
        mysql_query_get = """SELECT * from caj_facturas WHERE numeroFactura = %s"""
        cursor.execute(mysql_query_get,(id,))
        factura = cursor.fetchone()
        mysql_query_get_det_factura = """SELECT * FROM caj_detFacturas WHERE numeroFactura = %s"""
        cursor.execute(mysql_query_get_det_factura,(id,))
        det_factura = cursor.fetchall()
        data = {'factura':factura}
        mysql_query_get_id_objeto = """SELECT * FROM caj_Lista_Objetos WHERE id = %s"""
        mysql_query_get_moneda = """SELECT * FROM caj_Catalogo_Moneda_Tienda WHERE nur = %s"""
        mysql_query_get_moneda_obk = """SELECT * FROM caj_Catalogo_Moneda_Tienda WHERE id = %s"""
        mysql_query_get_moneda = """SELECT * FROM caj_Catalogo_Pintura_Tienda WHERE nur = %s"""
        detallelista = []
        for detalle in det_factura:
            det = {'detalle':detalle}
            cursor.execute(mysql_query_get_id_objeto,(detalle['id_objeto'],))
            objeto = cursor.fetchone()
            if objeto['nur_moneda']:
                det['objeto'] = 'moneda'
                cursor.execute(mysql_query_get_moneda,(objeto['nur_moneda'],))
                catMoneda = cursor.fetchone()
                cursor.execute(mysql_query_get_moneda_obk,(catMoneda['id_moneda'],))
                moneda = cursor.fetchone()
                det['moneda'] = {'catalogo':catMoneda,'moneda':moneda}
            else:
                det['objeto'] = 'pintura'
                cursor.execute(mysql_query_get_moneda,(objeto['id_pintura'],))
                catPintura = cursor.fetchone()
                det['pintura'] = {'catalogo':catPintura}
            detallelista.append(det)
        data['detalle'] = detallelista
        return Response(data)
        # if usuario:
        #     return Response({'tipo':payload['tipo'],'user':usuario})
        # raise AuthenticationFailed('No existe El usuario')

# class TerminarSubasta(APIView):

#     @conectar
#     def post(self,request,id,connection):
#         cursor = connection.cursor(dictionary=True)
#         token = request.META.get('HTTP_TOKEN')
#         if not token:
#             token = request.COOKIES.get('TOKEN')
#         if not token:
#             raise AuthenticationFailed('No Autorizado')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('No Autorizado!')
#         if payload['tipo'] != 'organizacion':
#             raise AuthenticationFailed('No Autorizado!')
        