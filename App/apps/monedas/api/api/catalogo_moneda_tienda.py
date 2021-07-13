from rest_framework import generics
import datetime
from database.conexion import conectar
from apps.monedas.api.serializers.catalogo_moneda_tienda import *
from apps.commons.models import *
from apps.monedas.models import *
from django.http import Http404

class Catalogo_Moneda_TiendaListAPIView(generics.ListAPIView):

    serializer_class = Catalogo_Moneda_TiendaSerializer

    @conectar
    def get_queryset(self,connection):
        moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
        divisa = ['id','id_pais','nombre']
        artista = ['id','nombre','apellido','nombreArtistico']
        moneda_artista = ['id_moneda','id_artista']
        pais = ['id','nombre','nacionalidad']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        coleccionista = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT 
                        {', '.join([f'Catalogo_Moneda_Tienda.{i} as catalogo_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])},
                        {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM Catalogo_Moneda_Tienda
                        INNER JOIN monedas
                        ON monedas.id = Catalogo_Moneda_Tienda.id_moneda
                        INNER JOIN divisas
                        ON (divisas.id,divisas.id_pais) = (monedas.id_divisa,monedas.id_pais_divisa) 
                        INNER JOIN paises as `divisa_pais`
                        ON divisas.id_pais = divisa_pais.id
                        INNER JOIN paises as moneda_pais
                        ON monedas.id_pais = moneda_pais.id
                        LEFT JOIN M_A
                        ON M_A.id_moneda = monedas.id
                        LEFT JOIN artistas
                        ON M_A.id_artista = artistas.id
                        LEFT JOIN organizaciones
                        ON organizaciones.id = Catalogo_Moneda_Tienda.id_organizacion
                        LEFT JOIN paises as organizacion_pais
                        ON organizacion_pais.id = organizaciones.id_pais
                        LEFT JOIN coleccionistas
                        ON coleccionistas.dni = Catalogo_Moneda_Tienda.id_coleccionista
                        LEFT JOIN paises as pais_nacio
                        ON pais_nacio.id = coleccionistas.id_pais_nacio
                        LEFT JOIN paises as pais_reside
                        ON pais_reside.id = coleccionistas.id_pais_reside
                        """
        #print(query_action)
        cursor.execute(query_action)

        #------Aqui viene el desmadre--------
        catalogo = []
        monedas = {}
        id_monedas = []
        for dato in cursor:
            #print(dato)
            artistaData = {}
            if dato['moneda_id'] not in id_monedas: #---Meto todo en catalogo
                catalogoDato={}
                coleccionistaData = {}
                paisNacio = {}
                paisReside = {}
                monedaDato = {}
                monedaDivisa = {}
                divisaPais = {}
                monedaPais = {}
                artistasList = []
                organizacionData = {}
                paisResideOrganizacion = {}
                for i in organizacion:
                    organizacionData[f'{i}'] = dato[f'organizacion_{i}']
                for i in pais:
                    paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
                organizacionData['pais']= paisResideOrganizacion
                for i in catalogo_moneda_tienda:
                    catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                for i in coleccionista:
                    coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
                for i in pais:
                    paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                    paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
                coleccionistaData['pais_reside']= paisReside
                coleccionistaData['pais_nacio']=paisNacio
                for i in moneda:
                    if i != 'ano':
                        monedaDato[f'{i}'] = dato[f'moneda_{i}']
                    else:
                        monedaDato[f'{i}'] = datetime.date(year=dato[f'moneda_{i}'],month=1,day=1)
                for i in divisa:
                    monedaDivisa[f'{i}'] = dato[f'divisa_{i}']
                for i in pais:
                    divisaPais[f'{i}'] = dato[f'divisa_pais_{i}']
                    monedaPais[f'{i}'] = dato[f'moneda_pais_{i}']
                monedaDivisa['pais'] = divisaPais
                monedaDato['divisa']= monedaDivisa
                monedaDato['pais']= monedaPais
                monedaDato['artistas'] = artistasList
                id_monedas.append(dato['moneda_id'])
                monedas[dato['moneda_id']]= monedaDato
                #----Asignaciones de Objetos
                catalogoDato['moneda']=monedaDato
                catalogoDato['coleccionista']=coleccionistaData
                catalogoDato['organizacion']=organizacionData
                catalogo.append(catalogoDato)
            for i in artista:
                artistaData[f'{i}'] = dato[f'artista_{i}']
            monedas[dato['moneda_id']]['artistas'].append(artistaData)
        # for dato in catalogo:
        #     print(dato)
        monedas = [Catalogo_Moneda_Tienda.model(**dato) for dato in catalogo]
        monedas.sort(key=lambda x: x.nur)
        return monedas
    

class Catalogo_Moneda_TiendaCreateAPIView(generics.CreateAPIView):
    serializer_class = Catalogo_Moneda_TiendaSerializer

class Catalogo_Moneda_TiendaRetriveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = Catalogo_Moneda_TiendaSerializer
    
    @conectar
    def get_object(self,connection):
        moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
        divisa = ['id','id_pais','nombre']
        artista = ['id','nombre','apellido','nombreArtistico']
        moneda_artista = ['id_moneda','id_artista']
        pais = ['id','nombre','nacionalidad']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        coleccionista = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT 
                        {', '.join([f'Catalogo_Moneda_Tienda.{i} as catalogo_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])},
                        {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM Catalogo_Moneda_Tienda
                        INNER JOIN monedas
                        ON monedas.id = Catalogo_Moneda_Tienda.id_moneda
                        INNER JOIN divisas
                        ON (divisas.id,divisas.id_pais) = (monedas.id_divisa,monedas.id_pais_divisa) 
                        INNER JOIN paises as `divisa_pais`
                        ON divisas.id_pais = divisa_pais.id
                        INNER JOIN paises as moneda_pais
                        ON monedas.id_pais = moneda_pais.id
                        LEFT JOIN M_A
                        ON M_A.id_moneda = monedas.id
                        LEFT JOIN artistas
                        ON M_A.id_artista = artistas.id
                        LEFT JOIN organizaciones
                        ON organizaciones.id = Catalogo_Moneda_Tienda.id_organizacion
                        LEFT JOIN paises as organizacion_pais
                        ON organizacion_pais.id = organizaciones.id_pais
                        LEFT JOIN coleccionistas
                        ON coleccionistas.dni = Catalogo_Moneda_Tienda.id_coleccionista
                        LEFT JOIN paises as pais_nacio
                        ON pais_nacio.id = coleccionistas.id_pais_nacio
                        LEFT JOIN paises as pais_reside
                        ON pais_reside.id = coleccionistas.id_pais_reside
                        WHERE Catalogo_Moneda_Tienda.nur = %s
                        """
        cursor.execute(query_action,(self.kwargs.get('nur'),))
        datos = cursor.fetchall()
        if datos:
            catalogo = None
            monedas = {}
            id_monedas = []
            for dato in datos:
                artistaData = {}
                if dato['moneda_id'] not in id_monedas: #---Meto todo en catalogo
                    catalogoDato={}
                    coleccionistaData = {}
                    paisNacio = {}
                    paisReside = {}
                    monedaDato = {}
                    monedaDivisa = {}
                    divisaPais = {}
                    monedaPais = {}
                    artistasList = []
                    organizacionData = {}
                    paisResideOrganizacion = {}
                    for i in organizacion:
                        organizacionData[f'{i}'] = dato[f'organizacion_{i}']
                    for i in pais:
                        paisResideOrganizacion[f'{i}'] = dato[f'organizacion_pais_{i}']
                    organizacionData['pais']= paisResideOrganizacion
                    for i in catalogo_moneda_tienda:
                        catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                    for i in coleccionista:
                        coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
                    for i in pais:
                        paisReside[f'{i}'] = dato[f'pais_reside_{i}']
                        paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
                    coleccionistaData['pais_reside']= paisReside
                    coleccionistaData['pais_nacio']=paisNacio
                    for i in moneda:
                        if i != 'ano':
                            monedaDato[f'{i}'] = dato[f'moneda_{i}']
                        else:
                            monedaDato[f'{i}'] = datetime.date(year=dato[f'moneda_{i}'],month=1,day=1)
                    for i in divisa:
                        monedaDivisa[f'{i}'] = dato[f'divisa_{i}']
                    for i in pais:
                        divisaPais[f'{i}'] = dato[f'divisa_pais_{i}']
                        monedaPais[f'{i}'] = dato[f'moneda_pais_{i}']
                    monedaDivisa['pais'] = divisaPais
                    monedaDato['divisa']= monedaDivisa
                    monedaDato['pais']= monedaPais
                    monedaDato['artistas'] = artistasList
                    id_monedas.append(dato['moneda_id'])
                    monedas[dato['moneda_id']]= monedaDato
                    #----Asignaciones de Objetos
                    catalogoDato['moneda']=monedaDato
                    catalogoDato['coleccionista']=coleccionistaData
                    catalogoDato['organizacion']=organizacionData
                    catalogo=catalogoDato
                for i in artista:
                    artistaData[f'{i}'] = dato[f'artista_{i}']
                monedas[dato['moneda_id']]['artistas'].append(artistaData)
            return Catalogo_Moneda_Tienda.model(**catalogo)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Catalogo_Catalogo_Moneda_Tienda_Tienda WHERE nur = %s",(instance.id,))
        connection.commit()