from rest_framework import generics
from database.conexion import conectar
from apps.organizaciones.api.serializers.contacto import *
from apps.commons.models import Pais
from apps.organizaciones.models import *
from django.http import Http404


class ContactoListAPIView(generics.ListAPIView):
    """
    Adicionalmente incluye un query param que retorna todos los contactos por un id de Organizacion
    ejemplo: http://127.0.0.1:8000/contacto/?id_organizacion=2
    """
    serializer_class = ContactoSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        # pais = ['id','nombre','nacionalidad']
        query = self.request.query_params.get('id_organizacion',None)
        contacto = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'cargo','id_organizacion']
        if query:
            query_action = f"""SELECT * 
                        FROM contactos 
                        where id_organizacion = %s
                        """
            cursor.execute(query_action,(query,))
        else:
            query_action = f"""SELECT * 
                        FROM contactos
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
        contactos.sort(key=lambda x: x.dni)
        return []
    

class ContactoCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactoSerializer

class ContactoRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ContactoSerializer
    
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
                        FROM contactos
                        WHERE dni = %s
                        """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query_action,(self.kwargs.get('dni'),))
        dato = cursor.fetchone()
        if dato:
            return Contacto.model(**dato)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM contactos WHERE dni = %s",(instance.dni,))
        connection.commit()

