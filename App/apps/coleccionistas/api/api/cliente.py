from rest_framework import generics
import datetime
from database.conexion import conectar
from apps.coleccionistas.api.serializers.cliente import *
from apps.commons.models import *
from apps.coleccionistas.models import *
from django.http import Http404

class ClienteListAPIView(generics.ListAPIView):

    serializer_class = ClienteSerializer

    @conectar
    def get_queryset(self,connection):
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        cliente = ['fechaIngreso','numeroExpedienteUnico','id_coleccionista','id_organizacion']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT 
                        {', '.join([f'caj_clientes.{i} as cliente_{i}' for i in cliente])},
                        {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM caj_clientes
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
        #print(query_action)
        cursor.execute(query_action)

        #------Aqui viene el desmadre--------
        clientes = []
        for dato in cursor:
            #print(dato)
            clienteDato={}
            coleccionistaData = {}
            paisNacio = {}
            paisReside = {}
            organizacionData = {}
            paisResideOrganizacion = {}
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
            clientes.append(clienteDato)
        # for dato in catalogo:
        #     print(dato)
        monedas = [Cliente.model(**dato) for dato in clientes]
        monedas.sort(key=lambda x: x.fechaIngreso)
        return monedas
    

class ClienteCreateAPIView(generics.CreateAPIView):
    serializer_class = ClienteSerializer

# class ClienteRetriveAPIView(generics.RetrieveAPIView):
#     serializer_class = ClienteSerializer
    
#     @conectar
#     def get_object(self,connection):
#         pais = ['id','nombre','nacionalidad']
#         coleccionista = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
#                         'fechaNacimiento','id_pais_nacio','id_pais_reside']
#         organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
#                         'paginaWeb','emailCorporativo','id_pais']
#         cliente = ['fechaIngreso','numeroExpedienteUnico','id_coleccionista','ir_organizacion']
#         cursor = connection.cursor(dictionary=True)
#         #query = self.request.query_params.get('id_pais',None)
#         query_action = f"""SELECT 
#                         {', '.join([f'clientes.{i} as cliente_{i}' for i in cliente])},
#                         {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
#                         {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
#                         {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
#                         {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
#                         {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
#                         FROM clientes
#                         INNER JOIN organizaciones
#                         ON organizaciones.id = clientes.id_organizacion
#                         INNER JOIN paises as organizacion_pais
#                         ON organizacion_pais.id = organizaciones.id_pais
#                         INNER JOIN coleccionistas
#                         ON coleccionistas.dni = clientes.id_coleccionista
#                         INNER JOIN paises as pais_nacio
#                         ON pais_nacio.id = coleccionistas.id_pais_nacio
#                         INNER JOIN paises as pais_reside
#                         ON pais_reside.id = coleccionistas.id_pais_reside
#                         WHERE 
#                         """
#         cursor.execute(query_action,(self.kwargs.get('nur'),))
#         datos = cursor.fetchall()
#         if datos:
#             catalogo = None
#             monedas = {}
#             id_monedas = []
#             for dato in datos:
#                 artistaData = {}
#                 if dato['moneda_id'] not in id_monedas: #---Meto todo en catalogo
#                     catalogoDato={}
#                     coleccionistaData = {}
#                     paisNacio = {}
#                     paisReside = {}
#                     monedaDato = {}
#                     monedaDivisa = {}
#                     divisaPais = {}
#                     monedaPais = {}
#                     artistasList = []
#                     organizacionData = {}
#                     paisResideOrganizacion = {}
#                     for i in organizacion:
#                         organizacionData[f'{i}'] = dato[f'organizacion_{i}']
#                     for i in pais:
#                         paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
#                     organizacionData['pais']= paisResideOrganizacion
#                     for i in catalogo_moneda_tienda:
#                         catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
#                     for i in coleccionista:
#                         coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
#                     for i in pais:
#                         paisReside[f'{i}'] = dato[f'pais_reside_{i}']
#                         paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
#                     coleccionistaData['pais_reside']= paisReside
#                     coleccionistaData['pais_nacio']=paisNacio
#                     for i in moneda:
#                         if i != 'ano':
#                             monedaDato[f'{i}'] = dato[f'moneda_{i}']
#                         else:
#                             monedaDato[f'{i}'] = datetime.date(year=dato[f'moneda_{i}'],month=1,day=1)
#                     for i in divisa:
#                         monedaDivisa[f'{i}'] = dato[f'divisa_{i}']
#                     for i in pais:
#                         divisaPais[f'{i}'] = dato[f'divisa_pais_{i}']
#                         monedaPais[f'{i}'] = dato[f'moneda_pais_{i}']
#                     monedaDivisa['pais'] = divisaPais
#                     monedaDato['divisa']= monedaDivisa
#                     monedaDato['pais']= monedaPais
#                     monedaDato['artistas'] = artistasList
#                     id_monedas.append(dato['moneda_id'])
#                     monedas[dato['moneda_id']]= monedaDato
#                     #----Asignaciones de Objetos
#                     catalogoDato['moneda']=monedaDato
#                     catalogoDato['coleccionista']=coleccionistaData
#                     catalogoDato['organizacion']=organizacionData
#                     catalogo=catalogoDato
#                 for i in artista:
#                     artistaData[f'{i}'] = dato[f'artista_{i}']
#                 monedas[dato['moneda_id']]['artistas'].append(artistaData)
#             return Cliente.model(**catalogo)
#         else:
#             raise Http404
#     @conectar
#     def perform_destroy(self, instance,connection):
#         cursor = connection.cursor()
#         cursor.execute("DELETE FROM Catalogo_Cliente_Tienda WHERE nur = %s",(instance.id,))
#         connection.commit()
