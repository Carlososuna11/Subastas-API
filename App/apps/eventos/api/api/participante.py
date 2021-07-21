from rest_framework import generics
from database.conexion import conectar
from apps.eventos.api.serializers import *
from apps.coleccionistas.api.serializers import *
from apps.organizaciones.api.serializers import * 
from apps.commons.models import Pais
from apps.organizaciones.models import *
from django.http import Http404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.conf import settings
import jwt, datetime
from apps.coleccionistas.api.serializers.cliente import *

class ParticipanteListAPIView(generics.ListAPIView):
    # serializer_class = ParticipanteSerializer
    serializer_class = ColeccionistaSerializer
    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        cliente = ['fechaIngreso','numeroExpedienteUnico','id_coleccionista','id_organizacion']
        participante = ['id_evento','fechaIngresoCliente','id_coleccionista_cliente','id_organizacion_cliente','id_pais']
        #query = self.request.query_params.get('id_pais',None)
        query_cliente = f"""SELECT 
                        {', '.join([f'caj_participantes.{i} as participante_{i}' for i in participante])},
                        {', '.join([f'caj_clientes.{i} as cliente_{i}' for i in cliente])},
                        {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM caj_participantes
                        INNER JOIN caj_clientes
                        ON (caj_participantes.id_coleccionista_cliente,caj_participantes.id_organizacion_cliente) = (caj_clientes.id_coleccionista,caj_clientes.id_organizacion)
                        INNER JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_clientes.id_organizacion
                        INNER JOIN caj_paises as organizacion_pais
                        ON organizacion_pais.id = caj_organizaciones.id_pais
                        INNER JOIN caj_coleccionistas
                        ON caj_coleccionistas.id = caj_clientes.id_coleccionista
                        INNER JOIN caj_paises as pais_nacio
                        ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
                        INNER JOIN caj_paises as pais_reside
                        ON pais_reside.id = caj_coleccionistas.id_pais_reside
                        """
        print(query_cliente)
        # if query:
        #     query_action = """SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
        #                     paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
        #                     FROM divisas 
        #                     INNER JOIN paises ON paises.id = divisas.id_pais
        #                     WHERE divisas.id_pais = %s
        #                     """
        #     cursor.execute(query_action,(query,))
        # else:
        cursor.execute(query_cliente)
        #print(pais_quey,id_pais_query)
        participantes = []
        for dato in cursor:
            participanteDato = {}
            clienteDato={}
            coleccionistaData = {}
            paisNacio = {}
            paisReside = {}
            organizacionData = {}
            paisResideOrganizacion = {}
            for i in participante:
                participanteDato[f'{i}'] = dato[f'participante_{i}']
            for i in cliente:
                clienteDato[f'{i}'] = dato[f'cliente_{i}']
            for i in organizacion:
                organizacionData[f'{i}'] = dato[f'organizacion_{i}']
            for i in pais:
                paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
            organizacionData['pais']= paisResideOrganizacion
            for i in coleccionista:
                coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
            for i in pais:
                paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
            coleccionistaData['pais_reside']= paisReside
            coleccionistaData['pais_nacio']=paisNacio
            clienteDato['coleccionista'] = coleccionistaData
            clienteDato['organizacion'] = organizacionData
            participanteDato['cliente'] = clienteDato
            organizacionData['pais']= paisReside
            participantes.append(participanteDato)
        organizaciones = [Participante.model(**dato) for dato in participantes]
        coleccionistas = list(set([participante.cliente.coleccionista for participante in organizaciones]))
        coleccionistas.sort(key=lambda x:x.id)
        organizaciones.sort(key=lambda x: x.fechaIngresoCliente)
        # return organizaciones
        return coleccionistas

class ParticipantePorEventoListAPIView(generics.ListAPIView):
    # serializer_class = ParticipanteSerializer
    serializer_class = ColeccionistaSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        cliente = ['fechaIngreso','numeroExpedienteUnico','id_coleccionista','id_organizacion']
        participante = ['id_evento','fechaIngresoCliente','id_coleccionista_cliente','id_organizacion_cliente','id_pais']
        #query = self.request.query_params.get('id_pais',None)
        query_cliente = f"""SELECT 
                        {', '.join([f'caj_participantes.{i} as participante_{i}' for i in participante])},
                        {', '.join([f'caj_clientes.{i} as cliente_{i}' for i in cliente])},
                        {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM caj_participantes
                        INNER JOIN caj_clientes
                        ON (caj_participantes.id_coleccionista_cliente,caj_participantes.id_organizacion_cliente) = (caj_clientes.id_coleccionista,caj_clientes.id_organizacion)
                        INNER JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_clientes.id_organizacion
                        INNER JOIN caj_paises as organizacion_pais
                        ON organizacion_pais.id = caj_organizaciones.id_pais
                        INNER JOIN caj_coleccionistas
                        ON caj_coleccionistas.id = caj_clientes.id_coleccionista
                        INNER JOIN caj_paises as pais_nacio
                        ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
                        INNER JOIN caj_paises as pais_reside
                        ON pais_reside.id = caj_coleccionistas.id_pais_reside
                        WHERE caj_participantes.id_evento = %s
                        """
        print(query_cliente)
        # if query:
        #     query_action = """SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
        #                     paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
        #                     FROM divisas 
        #                     INNER JOIN paises ON paises.id = divisas.id_pais
        #                     WHERE divisas.id_pais = %s
        #                     """
        #     cursor.execute(query_action,(query,))
        # else:
        cursor.execute(query_cliente,(self.kwargs.get('id'),))
        #print(pais_quey,id_pais_query)
        participantes = []
        for dato in cursor:
            participanteDato = {}
            clienteDato={}
            coleccionistaData = {}
            paisNacio = {}
            paisReside = {}
            organizacionData = {}
            paisResideOrganizacion = {}
            for i in participante:
                participanteDato[f'{i}'] = dato[f'participante_{i}']
            for i in cliente:
                clienteDato[f'{i}'] = dato[f'cliente_{i}']
            for i in organizacion:
                organizacionData[f'{i}'] = dato[f'organizacion_{i}']
            for i in pais:
                paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
            organizacionData['pais']= paisResideOrganizacion
            for i in coleccionista:
                coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
            for i in pais:
                paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
            coleccionistaData['pais_reside']= paisReside
            coleccionistaData['pais_nacio']=paisNacio
            clienteDato['coleccionista'] = coleccionistaData
            clienteDato['organizacion'] = organizacionData
            participanteDato['cliente'] = clienteDato
            organizacionData['pais']= paisReside
            participantes.append(participanteDato)
        #Nada más por probar
        organizaciones = [Participante.model(**dato) for dato in participantes]
        organizaciones.sort(key=lambda x: x.fechaIngresoCliente)
        coleccionistas = list(set([participante.cliente.coleccionista for participante in organizaciones]))
        coleccionistas.sort(key=lambda x:x.id)
        return coleccionistas

class ParticipanteCreateAPIView(generics.CreateAPIView):
    serializer_class = ParticipanteSerializer

# class ParticipanteRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

#     serializer_class = ParticipanteSerializer
    
#     @conectar
#     def get_object(self,connection):
#         pais = ['id','nombre','nacionalidad']
#         # organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
#         #                 'paginaWeb','emailCorporativo','id_pais']
#         evento = ['id','inscripcionCliente','inscripcionClienteNuevo','fecha','status',
#                 'tipo','tipoPuja','duracionHoras','lugar','id_pais']
#         # query_action = f"""SELECT * 
#         #                 FROM (SELECT {', '.join([f'{i} as organizacion_{i}' for i in organizacion])} FROM organizaciones) as `Participante`
#         #                 INNER JOIN (SELECT {', '.join([f'{i} as pais_{i}' for i in pais])} FROM paises) as `Pais`
#         #                 ON `Pais`.pais_id = `Participante`.organizacion_id_pais
#         #                 """
#         query_action =  f"""SELECT 
#                         {', '.join([f'eventos.{i} as evento_{i}' for i in evento])},
#                         {', '.join([f'paises.{i} as pais_{i}' for i in pais])}
#                         FROM eventos
#                         LEFT JOIN paises
#                         ON paises.id = eventos.id_pais
#                         WHERE eventos.id = %s
#                         """
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute(query_action,(self.kwargs.get('id'),))
#         dato = cursor.fetchone()
#         if dato:
#             organizacionData = {}
#             paisReside = {}
#             for i in evento:
#                 organizacionData[f'{i}'] = dato[f'evento_{i}']
#             for i in pais:
#                 paisReside[f'{i}'] = dato[f'pais_{i}']
#             organizacionData['pais']= paisReside
#             return Participante.model(**organizacionData)
#         else:
#             raise Http404
#     @conectar
#     def perform_destroy(self, instance,connection):
#         cursor = connection.cursor()
#         cursor.execute("DELETE FROM eventos WHERE id = %s",(instance.id,))
#         connection.commit()

class InscribirseView(APIView):

    @conectar
    def post(self, request,id_evento,connection):
        cursor = connection.cursor(dictionary=True)
        # tipo = request.data['tipo']
        token = request.META.get('HTTP_TOKEN')
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        if payload['tipo'] != 'coleccionista':
            raise AuthenticationFailed('No Autorizado!')
        mysql_query_get = """SELECT * from caj_coleccionistas WHERE id = %s"""
        cursor.execute(mysql_query_get,(payload['id'],))
        usuario  = cursor.fetchone()
        fechaNacimiento = usuario['fechaNacimiento']
        #validar mayor de edad
        print((datetime.date.today() - fechaNacimiento).days/365)
        if (datetime.date.today() - fechaNacimiento).days/365 < 21:
            raise ValidationError('No eres Mayor de Edad')
        mysql_query_get = """SELECT * FROM caj_eventos WHERE id = %s"""
        cursor.execute(mysql_query_get,(id_evento,))
        evento = cursor.fetchone()
        if not(evento):
            raise ValidationError('No existe el evento')
        if evento['fecha'] < datetime.date.today():
            raise ValidationError('El evento ya caducó')
        if evento['status'] == 'cancelado':
            raise ValidationError('El evento está cancelado')
        if evento['tipo'] == 'virtual':
            mysql_query_get = """SELECT id_organizacion FROM caj_planificadores WHERE id_evento = %s"""
            cursor.execute(mysql_query_get,(id_evento,))
            organizaciones = cursor.fetchall()
            for i in organizaciones:
                mysql_query_get = """SELECT * FROM caj_organizaciones WHERE id = %s"""
                cursor.execute(mysql_query_get,(i['id_organizacion'],))
                organizacion = cursor.fetchone()
                if organizacion['alcance'] == 'nacional':
                    if usuario['id_pais_reside'] != organizacion['id_pais']:
                        mysql_query_get = """SELECT * FROM caj_paises WHERE id = %s"""
                        cursor.execute(mysql_query_get,(organizacion['id_pais'],))
                        raise ValidationError(f"Los organizadores del evento virtual solo tienen alcance en {cursor.fetchone()['nombre']} para realizar sus envios, por ende no puedes participar en este evento")
        #---Paso validaciones -----
        response = Response()
        #response.set_cookie(key='x-token', value=token, httponly=True)
        #####Está inscrito en un evento ese dia
        mysql_query_eventos = """SELECT * FROM caj_eventos WHERE fecha = %s"""
        cursor.execute(mysql_query_eventos,(evento['fecha'],))
        eventos = cursor.fetchall()
        mysql_query_participando = """SELECT * FROM caj_participantes WHERE (id_coleccionista_cliente,id_evento) = (%s,%s)"""
        for i in eventos:
            cursor.execute(mysql_query_participando,(payload['id'],i['id']))
            if cursor.fetchone():
                if i['id'] == id_evento:
                    raise ValidationError('Ya participas en este evento')
                raise ValidationError('Ya participas en un evento para ese dia')
        mysql_query_get = """SELECT id_organizacion FROM caj_planificadores WHERE id_evento = %s"""
        cursor.execute(mysql_query_get,(id_evento,))
        organizaciones = cursor.fetchall()
        for organizacion in organizaciones:
            mysql_query_get = """SELECT * FROM caj_clientes WHERE id_organizacion = %s AND id_coleccionista = %s"""
            cursor.execute(mysql_query_get,(organizacion['id_organizacion'],usuario['id']))
            cliente  = cursor.fetchone()
            if not(cliente):
                if evento['inscripcionClienteNuevo'] == None:
                    raise ValidationError('El evento no admite nuevos clientes')
                data = {
                    'id_coleccionista':usuario['id'],
                    'id_organizacion':organizacion['id_organizacion']
                }
                serializer = ClienteSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            cursor.execute(mysql_query_get,(organizacion['id_organizacion'],usuario['id']))
            cliente  = cursor.fetchone()
            mysql_query_get = """SELECT * FROM caj_participantes WHERE 
                (id_coleccionista_cliente,id_organizacion_cliente,id_evento)=(%s,%s,%s)
                """
            print(cliente)
            cursor.execute(mysql_query_get,(usuario['id'],cliente['id_organizacion'],id_evento))
            participante = cursor.fetchone()
            if  participante:
                raise ValidationError('Ya participas en este evento')
            mysql_insert_query = """INSERT INTO caj_participantes
                (id_evento,fechaIngresoCliente,id_coleccionista_cliente,id_organizacion_cliente,id_pais)
                VALUES (%s, %s, %s, %s, %s)"""
            pais = None
            if evento['tipo'] == 'virtual':
                pais = usuario['id_pais_reside']
            cursor.execute(mysql_insert_query,(id_evento,cliente['fechaIngreso'],usuario['id'],cliente['id_organizacion'],pais))
        connection.commit()
        response.data = {
            'mensaje': 'Inscripcion exitosa'
        }
        return response