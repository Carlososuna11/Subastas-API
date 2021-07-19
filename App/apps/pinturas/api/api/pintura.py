from rest_framework import generics
from database.conexion import conectar
from apps.pinturas.api.serializers.pintura import *
from apps.commons.models import *
from apps.pinturas.models import *
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.conf import settings
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
                        {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_{i}' for i in pintura])},
                        {', '.join([f'caj_P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'caj_artistas.{i} as artista_{i}' for i in artista])},
                        {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM caj_Catalogo_Pintura_Tienda
                        LEFT JOIN caj_P_A
                        ON caj_P_A.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_artistas
                        ON caj_P_A.id_artista = caj_artistas.id
                        LEFT JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_Catalogo_Pintura_Tienda.id_organizacion
                        LEFT JOIN caj_paises as organizacion_pais
                        ON organizacion_pais.id = caj_organizaciones.id_pais
                        LEFT JOIN caj_coleccionistas
                        ON caj_coleccionistas.id = caj_Catalogo_Pintura_Tienda.id_coleccionista
                        LEFT JOIN caj_paises as pais_nacio
                        ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
                        LEFT JOIN caj_paises as pais_reside
                        ON pais_reside.id = caj_coleccionistas.id_pais_reside
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
    
class PinturaColeccionistaListAPIView(generics.ListAPIView):

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
                        {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_{i}' for i in pintura])},
                        {', '.join([f'caj_P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'caj_artistas.{i} as artista_{i}' for i in artista])},
                        {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM caj_Catalogo_Pintura_Tienda
                        LEFT JOIN caj_P_A
                        ON caj_P_A.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_artistas
                        ON caj_P_A.id_artista = caj_artistas.id
                        LEFT JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_Catalogo_Pintura_Tienda.id_organizacion
                        LEFT JOIN caj_paises as organizacion_pais
                        ON organizacion_pais.id = caj_organizaciones.id_pais
                        LEFT JOIN caj_coleccionistas
                        ON caj_coleccionistas.id = caj_Catalogo_Pintura_Tienda.id_coleccionista
                        LEFT JOIN caj_paises as pais_nacio
                        ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
                        LEFT JOIN caj_paises as pais_reside
                        ON pais_reside.id = caj_coleccionistas.id_pais_reside
                        WHERE caj_Catalogo_Pintura_Tienda.id_organizacion = %s
                        """
        #print(query_action)
        cursor.execute(query_action,(self.kwargs.get('id'),))

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

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('x-token')
        if not token:
            raise AuthenticationFailed('No Autorizado')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No Autorizado!')
        if payload['tipo'] != 'organizacion':
            raise AuthenticationFailed('No Autorizado!')
        request.data['id_organizacion'] = payload['id']
        return self.create(request, *args, **kwargs)

class PinturaRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PinturaSerializer

    def put(self, request, *args, **kwargs):
        token = request.COOKIES.get('x-token')
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
                        {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_{i}' for i in pintura])},
                        {', '.join([f'caj_P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'caj_artistas.{i} as artista_{i}' for i in artista])},
                        {', '.join([f'caj_coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                        {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                        {', '.join([f'pais_reside.{i} as pais_reside_{i}' for i in pais])},
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'organizacion_pais.{i} as organizacion_pais_{i}' for i in pais])}
                        FROM caj_Catalogo_Pintura_Tienda
                        LEFT JOIN caj_P_A
                        ON caj_P_A.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_artistas
                        ON caj_P_A.id_artista = caj_artistas.id
                        LEFT JOIN caj_organizaciones
                        ON caj_organizaciones.id = caj_Catalogo_Pintura_Tienda.id_organizacion
                        LEFT JOIN caj_paises as organizacion_pais
                        ON organizacion_pais.id = caj_organizaciones.id_pais
                        LEFT JOIN caj_coleccionistas
                        ON caj_coleccionistas.id = caj_Catalogo_Pintura_Tienda.id_coleccionista
                        LEFT JOIN caj_paises as pais_nacio
                        ON pais_nacio.id = caj_coleccionistas.id_pais_nacio
                        LEFT JOIN caj_paises as pais_reside
                        ON pais_reside.id = caj_coleccionistas.id_pais_reside
                        WHERE caj_Catalogo_Pintura_Tienda.nur = %s
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
        cursor.execute("DELETE FROM caj_Catalogo_Pintura_Tienda WHERE nur = %s",(instance.id,))
        connection.commit()
