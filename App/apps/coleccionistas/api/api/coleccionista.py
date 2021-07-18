from rest_framework import generics
from database.conexion import conectar
from apps.coleccionistas.api.serializers.coleccionista import *
from apps.commons.models import Pais
from apps.coleccionistas.models import *
from django.http import Http404


class ColeccionistaListAPIView(generics.ListAPIView):
    serializer_class = ColeccionistaSerializer

    @conectar
    def get_queryset(self,connection):
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        query_action = f"""SELECT 
                            {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                            {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                            {', '.join([f'caj_paises.{i} as pais_reside_{i}' for i in pais])}
                        FROM caj_coleccionistas
                        INNER JOIN caj_paises as pais_nacio
                        ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
                        INNER JOIN caj_paises
                        ON caj_paises.id = caj_coleccionistas.id_pais_reside
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
        coleccionistas = []
        for dato in cursor:
            coleccionistaData = {}
            paisNacio = {}
            paisReside = {}
            for i in coleccionista:
                coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
            for i in pais:
                paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
            coleccionistaData['pais_reside']= paisReside
            coleccionistaData['pais_nacio']=paisNacio
            coleccionistas.append(coleccionistaData)
        coleccionistas = [Coleccionista.model(**dato) for dato in coleccionistas]
        coleccionistas.sort(key=lambda x: x.id)
        return coleccionistas
    

class ColeccionistaCreateAPIView(generics.CreateAPIView):
    serializer_class = ColeccionistaSerializer

class ColeccionistaRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ColeccionistaSerializer
    
    @conectar
    def get_object(self,connection):
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        query_action = f"""SELECT 
                            {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                            {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                            {', '.join([f'caj_paises.{i} as pais_reside_{i}' for i in pais])}
                        FROM caj_coleccionistas
                        INNER JOIN caj_paises as pais_nacio
                        ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
                        INNER JOIN caj_paises
                        ON caj_paises.id = caj_coleccionistas.id_pais_reside
                        WHERE caj_coleccionistas.id = %s
                        """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query_action,(self.kwargs.get('id'),))
        dato = cursor.fetchone()
        if dato:
            coleccionistaData = {}
            paisNacio = {}
            paisReside = {}
            for i in coleccionista:
                coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
            for i in pais:
                paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
            coleccionistaData['pais_reside']= paisReside
            coleccionistaData['pais_nacio']=paisNacio
            return Coleccionista.model(**coleccionistaData)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM coleccionistas WHERE id = %s",(instance.id,))
        connection.commit()

