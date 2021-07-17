from rest_framework import generics
import datetime
from database.conexion import conectar
from apps.eventos.api.serializers.Lista_Objeto import *
from apps.commons.models import *
from apps.monedas.models import *
from django.http import Http404

class Lista_ObjetoListAPIView(generics.ListAPIView):

    serializer_class = Lista_ObjetoSerializer

    @conectar
    def get_queryset(self,connection):
        artista = ['id','nombre','apellido','nombreArtistico']
        pintura_artista = ['id_pintura','id_artista']
        #catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        pintura = ['nur','titulo','dimensionescm','estilo','ano','imagen','id_coleccionista','id_organizacion']
        moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
        pais = ['id','nombre','nacionalidad']
        divisa = ['id','id_pais','nombre']
        moneda_artista = ['id_moneda','id_artista']
        catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        lista_objeto = ['id_evento','id_eventoParticipante','id','id_pintura','nur_moneda','id_moneda','porcentajeGananciaMin',
                        'bid','ask','precioAlcanzado','orden','duracionmin','razonNoVenta','fechaIngresoParticipante','id_coleccionistaParticipante',
                        'id_organizacionParticipante']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT 
                        {', '.join([f'Lista_Objetos.{i} as lista_{i}' for i in lista_objeto])},
                        {', '.join([f'Catalogo_Moneda_Tienda.{i} as catalogo_moneda_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas_moneda.{i} as artista_moneda_{i}' for i in artista])},
                        {', '.join([f'Catalogo_Pintura_Tienda.{i} as catalogo_pintura_{i}' for i in pintura])},
                        {', '.join([f'P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas_pintura.{i} as artista_pintura_{i}' for i in artista])}
                        FROM Lista_Objetos
                        LEFT JOIN Catalogo_Moneda_Tienda
                        ON Catalogo_Moneda_Tienda.nur = Lista_Objetos.nur_moneda
                        LEFT JOIN monedas
                        ON monedas.id = Catalogo_Moneda_Tienda.id_moneda
                        LEFT JOIN divisas
                        ON (divisas.id,divisas.id_pais) = (monedas.id_divisa,monedas.id_pais_divisa) 
                        LEFT JOIN paises as `divisa_pais`
                        ON divisas.id_pais = divisa_pais.id
                        LEFT JOIN paises as moneda_pais
                        ON monedas.id_pais = moneda_pais.id
                        LEFT JOIN M_A
                        ON M_A.id_moneda = monedas.id
                        LEFT JOIN artistas as artistas_moneda
                        ON M_A.id_artista = artistas_moneda.id
                        LEFT JOIN Catalogo_Pintura_Tienda
                        ON Lista_Objetos.id_pintura = Catalogo_Pintura_Tienda.nur
                        LEFT JOIN P_A
                        ON P_A.id_pintura = Catalogo_Pintura_Tienda.nur
                        LEFT JOIN artistas as artistas_pintura
                        ON P_A.id_artista = artistas_pintura.id                        
                        """
        #print(query_action)
        cursor.execute(query_action)

        #------Aqui viene el desmadre--------
        lista_obj = []
        monedas = {}
        pinturas = {}
        id_monedas = []
        id_pinturas = []
        for dato in cursor:
            #print(dato)
            artistaData = {}
            if dato['moneda_id']:
                if dato['moneda_id'] not in id_monedas: #---Meto todo en catalogocatalogo_moneda_nur
                    listaObjetoDato = {}
                    catalogoDato={}
                    monedaDato = {}
                    monedaDivisa = {}
                    divisaPais = {}
                    monedaPais = {}
                    artistasList = []
                    for i in lista_objeto:
                        listaObjetoDato[f'{i}'] = dato[f'lista_{i}']
                    for i in catalogo_moneda_tienda:
                        catalogoDato[f'{i}'] = dato[f'catalogo_moneda_{i}']
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
                    lista_obj.append(listaObjetoDato)
                    listaObjetoDato['moneda'] = catalogoDato
                for i in artista:
                    artistaData[f'{i}'] = dato[f'artista_moneda_{i}']
                monedas[dato['moneda_id']]['artistas'].append(artistaData)
            else:
                if dato['catalogo_pintura_nur'] not in id_pinturas:
                    catalogoDato={}
                    listaObjetoDato = {}
                    artistasList = []
                    for i in lista_objeto:
                        listaObjetoDato[f'{i}'] = dato[f'lista_{i}']
                    for i in pintura:
                        if i!= 'ano':
                            catalogoDato[f'{i}'] = dato[f'catalogo_pintura_{i}']
                        else:
                            if dato[f'catalogo_pintura_{i}'] != None:
                                catalogoDato[f'{i}']= datetime.date(year=dato[f'catalogo_pintura_{i}'],month=1,day=1)
                            else:
                                catalogoDato[f'{i}'] = dato[f'catalogo_pintura_{i}']
                    catalogoDato['artistas'] = artistasList
                    id_pinturas.append(dato['catalogo_pintura_nur'])
                    pinturas[dato['catalogo_pintura_nur']]= catalogoDato
                    #----Asignaciones de Objetos
                    lista_obj.append(listaObjetoDato)
                    listaObjetoDato['pintura'] = catalogoDato
                for i in artista:
                    artistaData[f'{i}'] = dato[f'artista_pintura_{i}']
                pinturas[dato['catalogo_pintura_nur']]['artistas'].append(artistaData)   
        for i in lista_obj:
            print(i)
        monedas = [Lista_Objeto.model(**dato) for dato in lista_obj]
        monedas.sort(key=lambda x: x.id)
        return monedas
    

class Lista_ObjetoCreateAPIView(generics.CreateAPIView):
    serializer_class = Lista_ObjetoSerializer

class Lista_ObjetoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Lista_ObjetoSerializer
    
    @conectar
    def get_object(self,connection):
        artista = ['id','nombre','apellido','nombreArtistico']
        pintura_artista = ['id_pintura','id_artista']
        #catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        pintura = ['nur','titulo','dimensionescm','estilo','ano','imagen','id_coleccionista','id_organizacion']
        moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
        pais = ['id','nombre','nacionalidad']
        divisa = ['id','id_pais','nombre']
        moneda_artista = ['id_moneda','id_artista']
        catalogo_moneda_tienda = ['nur','id_moneda','id_coleccionista','id_organizacion']
        lista_objeto = ['id_evento','id_eventoParticipante','id','id_pintura','nur_moneda','id_moneda','porcentajeGananciaMin',
                        'bid','ask','precioAlcanzado','orden','duracionmin','razonNoVenta','fechaIngresoParticipante','id_coleccionistaParticipante',
                        'id_organizacionParticipante']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT 
                        {', '.join([f'Lista_Objetos.{i} as lista_{i}' for i in lista_objeto])},
                        {', '.join([f'Catalogo_Moneda_Tienda.{i} as catalogo_moneda_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas_moneda.{i} as artista_moneda_{i}' for i in artista])},
                        {', '.join([f'Catalogo_Pintura_Tienda.{i} as catalogo_pintura_{i}' for i in pintura])},
                        {', '.join([f'P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas_pintura.{i} as artista_pintura_{i}' for i in artista])}
                        FROM Lista_Objetos
                        LEFT JOIN Catalogo_Moneda_Tienda
                        ON Catalogo_Moneda_Tienda.nur = Lista_Objetos.nur_moneda
                        LEFT JOIN monedas
                        ON monedas.id = Catalogo_Moneda_Tienda.id_moneda
                        LEFT JOIN divisas
                        ON (divisas.id,divisas.id_pais) = (monedas.id_divisa,monedas.id_pais_divisa) 
                        LEFT JOIN paises as `divisa_pais`
                        ON divisas.id_pais = divisa_pais.id
                        LEFT JOIN paises as moneda_pais
                        ON monedas.id_pais = moneda_pais.id
                        LEFT JOIN M_A
                        ON M_A.id_moneda = monedas.id
                        LEFT JOIN artistas as artistas_moneda
                        ON M_A.id_artista = artistas_moneda.id
                        LEFT JOIN Catalogo_Pintura_Tienda
                        ON Lista_Objetos.id_pintura = Catalogo_Pintura_Tienda.nur
                        LEFT JOIN P_A
                        ON P_A.id_pintura = Catalogo_Pintura_Tienda.nur
                        LEFT JOIN artistas as artistas_pintura
                        ON P_A.id_artista = artistas_pintura.id
                        WHERE Lista_Objetos.id = %s                        
                        """
        cursor.execute(query_action,(self.kwargs.get('id'),))
        datos = cursor.fetchall()
        if datos:
            lista_obj = None
            monedas = {}
            pinturas = {}
            id_monedas = []
            id_pinturas = []
            for dato in datos:
                #print(dato)
                artistaData = {}
                if dato['moneda_id']:
                    if dato['moneda_id'] not in id_monedas: #---Meto todo en catalogocatalogo_moneda_nur
                        listaObjetoDato = {}
                        catalogoDato={}
                        monedaDato = {}
                        monedaDivisa = {}
                        divisaPais = {}
                        monedaPais = {}
                        artistasList = []
                        for i in lista_objeto:
                            listaObjetoDato[f'{i}'] = dato[f'lista_{i}']
                        for i in catalogo_moneda_tienda:
                            catalogoDato[f'{i}'] = dato[f'catalogo_moneda_{i}']
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
                        lista_obj = listaObjetoDato
                        listaObjetoDato['moneda'] = catalogoDato
                    for i in artista:
                        artistaData[f'{i}'] = dato[f'artista_moneda_{i}']
                    monedas[dato['moneda_id']]['artistas'].append(artistaData)
                else:
                    if dato['catalogo_pintura_nur'] not in id_pinturas:
                        catalogoDato={}
                        listaObjetoDato = {}
                        artistasList = []
                        for i in lista_objeto:
                            listaObjetoDato[f'{i}'] = dato[f'lista_{i}']
                        for i in pintura:
                            if i!= 'ano':
                                catalogoDato[f'{i}'] = dato[f'catalogo_pintura_{i}']
                            else:
                                if dato[f'catalogo_pintura_{i}'] != None:
                                    catalogoDato[f'{i}']= datetime.date(year=dato[f'catalogo_pintura_{i}'],month=1,day=1)
                                else:
                                    catalogoDato[f'{i}'] = dato[f'catalogo_pintura_{i}']
                        catalogoDato['artistas'] = artistasList
                        id_pinturas.append(dato['catalogo_pintura_nur'])
                        pinturas[dato['catalogo_pintura_nur']]= catalogoDato
                        #----Asignaciones de Objetos
                        lista_obj = listaObjetoDato
                        listaObjetoDato['pintura'] = catalogoDato
                    for i in artista:
                        artistaData[f'{i}'] = dato[f'artista_pintura_{i}']
                    pinturas[dato['catalogo_pintura_nur']]['artistas'].append(artistaData)  
            return Lista_Objeto.model(**lista_obj)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Lista_Objetos WHERE id = %s",(instance.id,))
        connection.commit()