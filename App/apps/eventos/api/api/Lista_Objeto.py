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
                        {', '.join([f'caj_Lista_Objetos.{i} as lista_{i}' for i in lista_objeto])},
                        {', '.join([f'caj_Catalogo_Moneda_Tienda.{i} as catalogo_moneda_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'caj_monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'caj_divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'caj_M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas_moneda.{i} as artista_moneda_{i}' for i in artista])},
                        {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_pintura_{i}' for i in pintura])},
                        {', '.join([f'caj_P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas_pintura.{i} as artista_pintura_{i}' for i in artista])}
                        FROM caj_Lista_Objetos
                        LEFT JOIN caj_Catalogo_Moneda_Tienda
                        ON caj_Catalogo_Moneda_Tienda.nur = caj_Lista_Objetos.nur_moneda
                        LEFT JOIN caj_monedas
                        ON caj_monedas.id = caj_Catalogo_Moneda_Tienda.id_moneda
                        LEFT JOIN caj_divisas
                        ON (caj_divisas.id,caj_divisas.id_pais) = (caj_monedas.id_divisa,caj_monedas.id_pais_divisa) 
                        LEFT JOIN caj_paises as `divisa_pais`
                        ON caj_divisas.id_pais = divisa_pais.id
                        LEFT JOIN caj_paises as moneda_pais
                        ON caj_monedas.id_pais = moneda_pais.id
                        LEFT JOIN caj_M_A
                        ON caj_M_A.id_moneda = caj_monedas.id
                        LEFT JOIN caj_artistas as artistas_moneda
                        ON caj_M_A.id_artista = artistas_moneda.id
                        LEFT JOIN caj_Catalogo_Pintura_Tienda
                        ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_P_A
                        ON caj_P_A.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_artistas as artistas_pintura
                        ON caj_P_A.id_artista = artistas_pintura.id                        
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
                        monedaDato[f'{i}'] = dato[f'moneda_{i}']
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

    @conectar
    def finalize_response(self, request, response,connection, *args, **kwargs):
        cursor = connection.cursor(dictionary=True)
        # mysql_get_ask_objeto = """SELECT ask FROM caj_Lista_Objetos WHERE ()"""
        for objeto in response.data:
            objeto['factura'] = None
            if objeto['id_coleccionistaParticipante']:
                mysql_query = """SELECT * FROM caj_facturas WHERE (id_coleccionistaParticipante,id_organizacionParticipante,id_evento) = (%s,%s,%s)"""
                cursor.execute(mysql_query, (objeto['id_coleccionistaParticipante'],objeto['id_organizacionParticipante'],objeto['id_eventoParticipante']))
                factura = cursor.fetchone()
                objeto['factura'] = factura['numeroFactura']
            if objeto['nur_moneda']:
                objeto['objeto'] = 'moneda'
            else:
                objeto['objeto'] = 'pintura'
            objeto['precio'] =  f"{float(objeto['ask'])/(1+float(objeto['porcentajeGananciaMin'])/100):.2f}" 

        return super().finalize_response(request, response, *args, **kwargs)
    
class Lista_Objeto_Por_Evento_ListAPIView(generics.ListAPIView):

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
                        {', '.join([f'caj_Lista_Objetos.{i} as lista_{i}' for i in lista_objeto])},
                        {', '.join([f'caj_Catalogo_Moneda_Tienda.{i} as catalogo_moneda_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'caj_monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'caj_divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'caj_M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas_moneda.{i} as artista_moneda_{i}' for i in artista])},
                        {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_pintura_{i}' for i in pintura])},
                        {', '.join([f'caj_P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas_pintura.{i} as artista_pintura_{i}' for i in artista])}
                        FROM caj_Lista_Objetos
                        LEFT JOIN caj_Catalogo_Moneda_Tienda
                        ON caj_Catalogo_Moneda_Tienda.nur = caj_Lista_Objetos.nur_moneda
                        LEFT JOIN caj_monedas
                        ON caj_monedas.id = caj_Catalogo_Moneda_Tienda.id_moneda
                        LEFT JOIN caj_divisas
                        ON (caj_divisas.id,caj_divisas.id_pais) = (caj_monedas.id_divisa,caj_monedas.id_pais_divisa) 
                        LEFT JOIN caj_paises as `divisa_pais`
                        ON caj_divisas.id_pais = divisa_pais.id
                        LEFT JOIN caj_paises as moneda_pais
                        ON caj_monedas.id_pais = moneda_pais.id
                        LEFT JOIN caj_M_A
                        ON caj_M_A.id_moneda = caj_monedas.id
                        LEFT JOIN caj_artistas as artistas_moneda
                        ON caj_M_A.id_artista = artistas_moneda.id
                        LEFT JOIN caj_Catalogo_Pintura_Tienda
                        ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_P_A
                        ON caj_P_A.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_artistas as artistas_pintura
                        ON caj_P_A.id_artista = artistas_pintura.id
                        WHERE caj_Lista_Objetos.id_evento = %s                        
                        """
        #print(query_action)
        cursor.execute(query_action,(self.kwargs.get('id_evento',None),))

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
                        monedaDato[f'{i}'] = dato[f'moneda_{i}']
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

    @conectar
    def finalize_response(self, request, response,connection, *args, **kwargs):
        cursor = connection.cursor(dictionary=True)
        # mysql_get_ask_objeto = """SELECT ask FROM caj_Lista_Objetos WHERE ()"""
        for objeto in response.data:
            objeto['factura'] = None
            print(objeto)
            if objeto['id_coleccionistaParticipante']:
                mysql_query = """SELECT * FROM caj_facturas WHERE (id_coleccionistaParticipante,id_organizacionParticipante,id_evento) = (%s,%s,%s)"""
                cursor.execute(mysql_query, (objeto['id_coleccionistaParticipante'],objeto['id_organizacionParticipante'],objeto['id_eventoParticipante']))
                print(objeto['id_coleccionistaParticipante'],objeto['id_organizacionParticipante'],objeto['id_eventoParticipante'])
                factura = cursor.fetchone()
                objeto['factura'] = factura['numeroFactura']
            if objeto['nur_moneda']:
                objeto['objeto'] = 'moneda'
            else:
                objeto['objeto'] = 'pintura'
            objeto['precio'] =  f"{float(objeto['ask'])/(1+float(objeto['porcentajeGananciaMin'])/100):.2f}" 

        return super().finalize_response(request, response, *args, **kwargs)



class Lista_ObjetoCreateAPIView(generics.CreateAPIView):
    serializer_class = Orden_Lista_ObjetoSerializer
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
                        {', '.join([f'caj_Lista_Objetos.{i} as lista_{i}' for i in lista_objeto])},
                        {', '.join([f'caj_Catalogo_Moneda_Tienda.{i} as catalogo_moneda_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'caj_monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'caj_divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'caj_M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas_moneda.{i} as artista_moneda_{i}' for i in artista])},
                        {', '.join([f'caj_Catalogo_Pintura_Tienda.{i} as catalogo_pintura_{i}' for i in pintura])},
                        {', '.join([f'caj_P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas_pintura.{i} as artista_pintura_{i}' for i in artista])}
                        FROM caj_Lista_Objetos
                        LEFT JOIN caj_Catalogo_Moneda_Tienda
                        ON caj_Catalogo_Moneda_Tienda.nur = caj_Lista_Objetos.nur_moneda
                        LEFT JOIN caj_monedas
                        ON caj_monedas.id = caj_Catalogo_Moneda_Tienda.id_moneda
                        LEFT JOIN caj_divisas
                        ON (caj_divisas.id,caj_divisas.id_pais) = (caj_monedas.id_divisa,caj_monedas.id_pais_divisa) 
                        LEFT JOIN caj_paises as `divisa_pais`
                        ON caj_divisas.id_pais = divisa_pais.id
                        LEFT JOIN caj_paises as moneda_pais
                        ON caj_monedas.id_pais = moneda_pais.id
                        LEFT JOIN caj_M_A
                        ON caj_M_A.id_moneda = caj_monedas.id
                        LEFT JOIN caj_artistas as artistas_moneda
                        ON caj_M_A.id_artista = artistas_moneda.id
                        LEFT JOIN caj_Catalogo_Pintura_Tienda
                        ON caj_Lista_Objetos.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_P_A
                        ON caj_P_A.id_pintura = caj_Catalogo_Pintura_Tienda.nur
                        LEFT JOIN caj_artistas as artistas_pintura
                        ON caj_P_A.id_artista = artistas_pintura.id 
                        WHERE caj_Lista_Objetos.id = %s                        
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
                            monedaDato[f'{i}'] = dato[f'moneda_{i}']
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
        cursor.execute("DELETE FROM caj_Lista_Objetos WHERE id = %s",(instance.id,))
        connection.commit()

