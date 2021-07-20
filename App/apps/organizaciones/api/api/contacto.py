from rest_framework import generics
from database.conexion import conectar
from apps.organizaciones.api.serializers.contacto import *
from apps.commons.models import Pais
from apps.organizaciones.models import *
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt, datetime
from rest_framework.response import Response
from rest_framework import status
class ContactoListAPIView(generics.ListAPIView):
    serializer_class = ContactoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        # pais = ['id','nombre','nacionalidad']
        contacto = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'cargo','id_organizacion']
        # if query:
        #     query_action = f"""SELECT * 
        #                 FROM caj_contactos 
        #                 where id_organizacion = %s
        #                 """
        #     cursor.execute(query_action,(query,))
        # else:
        query_action = f"""SELECT * 
                        FROM caj_contactos
                        """
        cursor.execute(query_action)
        # if query:
        #     query_action = """SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
        #                     paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
        #                     FROM divisas 
        #                     INNER JOIN paises ON paises.id = divisas.id_pais
        #                     WHERE divisas.id_pais = %s
        #                     """
        #     cursor.execute(query_action,(query,))
        # else:
        #print(pais_quey,id_pais_query)
        # coleccionistas = []
        # for dato in cursor:
        #     coleccionistaData = {}
        #     paisNacio = {}
        #     paisReside = {}
        #     for i in coleccionista:
        #         coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
        #     for i in pais:
        #         paisReside[f'{i}'] = dato[f'pais_reside_{i}']
        #         paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
        #     coleccionistaData['pais_reside']= paisReside
        #     coleccionistaData['pais_nacio']=paisNacio
        #     coleccionistas.append(coleccionistaData)
        contactos= [Contacto.model(**dato) for dato in cursor]
        contactos.sort(key=lambda x: x.id)
        return contactos
    
class ContactoOrganizacionListAPIView(generics.ListAPIView):
    serializer_class = ContactoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        # pais = ['id','nombre','nacionalidad']
        contacto = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'cargo','id_organizacion']
        # if query:
        query_action = f"""SELECT * 
                    FROM caj_contactos 
                    where id_organizacion = %s
                    """
        cursor.execute(query_action,(self.kwargs.get('id'),))
        # else:
        # query_action = f"""SELECT * 
        #                 FROM caj_contactos
        #                 """
        # cursor.execute(query_action)
        # if query:
        #     query_action = """SELECT divisas.id as divisa_id, divisas.id_pais as divisa_id_pais, divisas.nombre as divisa_nombre,
        #                     paises.id as pais_id, paises.nombre as pais_nombre, paises.nacionalidad as pais_nacionalidad 
        #                     FROM divisas 
        #                     INNER JOIN paises ON paises.id = divisas.id_pais
        #                     WHERE divisas.id_pais = %s
        #                     """
        #     cursor.execute(query_action,(query,))
        # else:
        #print(pais_quey,id_pais_query)
        # coleccionistas = []
        # for dato in cursor:
        #     coleccionistaData = {}
        #     paisNacio = {}
        #     paisReside = {}
        #     for i in coleccionista:
        #         coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
        #     for i in pais:
        #         paisReside[f'{i}'] = dato[f'pais_reside_{i}']
        #         paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
        #     coleccionistaData['pais_reside']= paisReside
        #     coleccionistaData['pais_nacio']=paisNacio
        #     coleccionistas.append(coleccionistaData)
        contactos= [Contacto.model(**dato) for dato in cursor]
        contactos.sort(key=lambda x: x.id)
        return contactos

class ContactoCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactoSerializer

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            token = request.COOKIES.get('TOKEN')
        if not token:
            if not(request.data.get('id_organizacion',None)):
                return Response({'error':'Debe ingresar el token'},status=status.HTTP_400_BAD_REQUEST)
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('No Autorizado!')
            if payload['tipo'] != 'organizacion':
                raise AuthenticationFailed('No Autorizado!')
            request.data['id_organizacion'] = payload['id']
        return self.create(request, *args, **kwargs)
class ContactoRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ContactoSerializer
    
    def put(self, request, *args, **kwargs):
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
        request.data['id_organizacion'] = payload['id']
        return self.update(request, *args, **kwargs)

    @conectar
    def get_object(self,connection):
        # pais = ['id','nombre','nacionalidad']
        # contacto = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
        #                 'fechaNacimiento','id_pais_nacio','id_pais_reside']
        # query_action = f"""SELECT * 
        #                 FROM (SELECT {', '.join([f'{i} as coleccionista_{i}' for i in coleccionista])} FROM coleccionistas) as `Contacto`
        #                 INNER JOIN (SELECT {', '.join([f'{i} as pais_nacio_{i}' for i in pais])} FROM paises) as `Pais_nacio`
        #                 ON `Pais_nacio`.pais_nacio_id = `Contacto`.coleccionista_id_pais_nacio
        #                 INNER JOIN (SELECT {', '.join([f'{i} as pais_reside_{i}' for i in pais])} FROM paises) as `Pais_reside`
        #                 ON `Pais_reside`.pais_reside_id = `Contacto`.coleccionista_id_pais_reside
        #                 WHERE `Contacto`.coleccionista_dni = %s
        #                 """
        query_action = f"""SELECT * 
                        FROM caj_contactos
                        WHERE id = %s
                        """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query_action,(self.kwargs.get('id'),))
        dato = cursor.fetchone()
        if dato:
            return Contacto.model(**dato)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM caj_contactos WHERE id = %s",(instance.id,))
        connection.commit()

