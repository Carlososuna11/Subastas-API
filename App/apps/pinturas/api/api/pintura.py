from rest_framework import generics
import datetime
from database.conexion import conectar
from apps.pinturas.api.serializers.pintura import *
from apps.commons.models import *
from apps.pinturas.models import *
from django.http import Http404

class PinturaListAPIView(generics.ListAPIView):

    serializer_class = PinturaSerializer

    @conectar
    def get_queryset(self,connection):
        # moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        # 'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        # 'imagen']
        #divisa = ['id','id_pais','nombre']
        artista = ['id','nombre','apellido','nombreArtistico']
        pintura_artista = ['id_pintura','id_artista']
        pais = ['id','nombre','nacionalidad']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        #catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        pintura = ['nur','titulo','dimensionescm','estilo','ano','imagen','id_coleccionista','id_organizacion']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT 
                        {', '.join([f'Catalogo_Pintura_Tienda.{i} as catalogo_{i}' for i in pintura])},
                        {', '.join([f'P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])},
                        {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM Catalogo_Pintura_Tienda
                        LEFT JOIN P_A
                        ON P_A.id_pintura = Catalogo_Pintura_Tienda.nur
                        LEFT JOIN artistas
                        ON P_A.id_artista = artistas.id
                        LEFT JOIN organizaciones
                        ON organizaciones.id = Catalogo_Pintura_Tienda.id_organizacion
                        LEFT JOIN paises as organizacion_pais
                        ON organizacion_pais.id = organizaciones.id_pais
                        LEFT JOIN coleccionistas
                        ON coleccionistas.id = Catalogo_Pintura_Tienda.id_coleccionista
                        LEFT JOIN paises as pais_nacio
                        ON pais_nacio.id = coleccionistas.id_pais_nacio
                        LEFT JOIN paises as pais_reside
                        ON pais_reside.id = coleccionistas.id_pais_reside
                        """
        #print(query_action)
        cursor.execute(query_action)

        #------Aqui viene el desmadre--------
        catalogo = []
        pinturas = {}
        id_pinturas = []
        for dato in cursor:
            #print(dato)
            artistaData = {}
            if dato['catalogo_nur'] not in id_pinturas: #---Meto todo en catalogo
                catalogoDato={}
                coleccionistaData = {}
                paisNacio = {}
                paisReside = {}
                artistasList = []
                organizacionData = {}
                paisResideOrganizacion = {}
                for i in organizacion:
                    organizacionData[f'{i}'] = dato[f'organizacion_{i}']
                for i in pais:
                    paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
                organizacionData['pais']= paisResideOrganizacion
                for i in pintura:
                    if i!= 'ano':
                        catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                    else:
                        if dato[f'catalogo_{i}'] != None:
                            catalogoDato[f'{i}']= datetime.date(year=dato[f'catalogo_{i}'],month=1,day=1)
                        else:
                            catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                for i in coleccionista:
                    coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
                for i in pais:
                    paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                    paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
                coleccionistaData['pais_reside']= paisReside
                coleccionistaData['pais_nacio']=paisNacio
                catalogoDato['artistas'] = artistasList
                id_pinturas.append(dato['catalogo_nur'])
                pinturas[dato['catalogo_nur']]= catalogoDato
                #----Asignaciones de Objetos
                catalogoDato['coleccionista']=coleccionistaData
                catalogoDato['organizacion']=organizacionData
                catalogo.append(catalogoDato)
            for i in artista:
                artistaData[f'{i}'] = dato[f'artista_{i}']
            pinturas[dato['catalogo_nur']]['artistas'].append(artistaData)
        # for dato in catalogo:
        #     print(dato)
        monedas = [Pintura.model(**dato) for dato in catalogo]
        monedas.sort(key=lambda x: x.nur)
        return monedas
    

class PinturaCreateAPIView(generics.CreateAPIView):
    serializer_class = PinturaSerializer

class PinturaRetriveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = PinturaSerializer
    
    @conectar
    def get_object(self,connection):
        artista = ['id','nombre','apellido','nombreArtistico']
        pintura_artista = ['id_pintura','id_artista']
        pais = ['id','nombre','nacionalidad']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        coleccionista = ['id','dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        #catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        pintura = ['nur','titulo','dimensionescm','estilo','ano','imagen','id_coleccionista','id_organizacion']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT 
                        {', '.join([f'Catalogo_Pintura_Tienda.{i} as catalogo_{i}' for i in pintura])},
                        {', '.join([f'P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])},
                        {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM Catalogo_Pintura_Tienda
                        LEFT JOIN P_A
                        ON P_A.id_pintura = Catalogo_Pintura_Tienda.nur
                        LEFT JOIN artistas
                        ON P_A.id_artista = artistas.id
                        LEFT JOIN organizaciones
                        ON organizaciones.id = Catalogo_Pintura_Tienda.id_organizacion
                        LEFT JOIN paises as organizacion_pais
                        ON organizacion_pais.id = organizaciones.id_pais
                        LEFT JOIN coleccionistas
                        ON coleccionistas.id = Catalogo_Pintura_Tienda.id_coleccionista
                        LEFT JOIN paises as pais_nacio
                        ON pais_nacio.id = coleccionistas.id_pais_nacio
                        LEFT JOIN paises as pais_reside
                        ON pais_reside.id = coleccionistas.id_pais_reside
                        WHERE Catalogo_Pintura_Tienda.nur = %s
                        """
        cursor.execute(query_action,(self.kwargs.get('nur'),))
        datos = cursor.fetchall()
        if datos:
            catalogo = None
            pinturas = {}
            id_pinturas = []
            for dato in datos:
                #print(dato)
                artistaData = {}
                if dato['catalogo_nur'] not in id_pinturas: #---Meto todo en catalogo
                    catalogoDato={}
                    coleccionistaData = {}
                    paisNacio = {}
                    paisReside = {}
                    artistasList = []
                    organizacionData = {}
                    paisResideOrganizacion = {}
                    for i in organizacion:
                        organizacionData[f'{i}'] = dato[f'organizacion_{i}']
                    for i in pais:
                        paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
                    organizacionData['pais']= paisResideOrganizacion
                    for i in pintura:
                        if i!= 'ano':
                            catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                        else:
                            if dato[f'catalogo_{i}'] != None:
                                catalogoDato[f'{i}']= datetime.date(year=dato[f'catalogo_{i}'],month=1,day=1)
                            else:
                                catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                    for i in coleccionista:
                        coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
                    for i in pais:
                        paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                        paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
                    coleccionistaData['pais_reside']= paisReside
                    coleccionistaData['pais_nacio']=paisNacio
                    catalogoDato['artistas'] = artistasList
                    id_pinturas.append(dato['catalogo_nur'])
                    pinturas[dato['catalogo_nur']]= catalogoDato
                    #----Asignaciones de Objetos
                    catalogoDato['coleccionista']=coleccionistaData
                    catalogoDato['organizacion']=organizacionData
                    catalogo=catalogoDato
                for i in artista:
                    artistaData[f'{i}'] = dato[f'artista_{i}']
                pinturas[dato['catalogo_nur']]['artistas'].append(artistaData)
            return Pintura.model(**catalogo)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Catalogo_Pintura_Tienda WHERE nur = %s",(instance.id,))
        connection.commit()
