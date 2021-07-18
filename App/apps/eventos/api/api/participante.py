from rest_framework import generics
from database.conexion import conectar
from apps.eventos.api.serializers import *
from apps.commons.models import Pais
from apps.organizaciones.models import *
from django.http import Http404


class ParticipanteListAPIView(generics.ListAPIView):
    serializer_class = ParticipanteSerializer

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
        organizaciones.sort(key=lambda x: x.fechaIngresoCliente)
        return organizaciones
    

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

