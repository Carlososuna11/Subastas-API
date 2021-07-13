from rest_framework import generics
import datetime
from database.conexion import conectar
from apps.monedas.api.serializers.moneda import *
from apps.commons.models import *
from apps.monedas.models import *
from django.http import Http404

class MonedaListAPIView(generics.ListAPIView):

    serializer_class = MonedaSerializer

    @conectar
    def get_queryset(self,connection):
        moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
        divisa = ['id','id_pais','nombre']
        artista = ['id','nombre','apellido','nombreArtistico']
        moneda_artista = ['id_moneda','id_artista']
        pais = ['id','nombre','nacionalidad']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'paises.{i} as pais_{i}' for i in pais])},
                        {', '.join([f'M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])}
                        FROM monedas
                        INNER JOIN divisas
                        ON (divisas.id,divisas.id_pais) = (monedas.id_divisa,monedas.id_pais_divisa) 
                        INNER JOIN paises as `divisa_pais`
                        ON divisas.id_pais = divisa_pais.id
                        INNER JOIN paises
                        ON monedas.id_pais = paises.id
                        LEFT JOIN M_A
                        ON M_A.id_moneda = monedas.id
                        LEFT JOIN artistas
                        ON M_A.id_artista = artistas.id
                        """
        print(query_action)
        cursor.execute(query_action)
        #print(pais_quey,id_pais_query)
        monedas = {}
        id_monedas = []
        for dato in cursor:
            artistaData = {}
            if dato['moneda_id'] not in id_monedas:
                monedaDato = {}
                monedaDivisa = {}
                divisaPais = {}
                monedaPais = {}
                artistasList = []
                for i in moneda:
                    if i != 'ano':
                        monedaDato[f'{i}'] = dato[f'moneda_{i}']
                    else:
                        monedaDato[f'{i}'] = datetime.date(year=dato[f'moneda_{i}'],month=1,day=1)
                for i in divisa:
                    monedaDivisa[f'{i}'] = dato[f'divisa_{i}']
                for i in pais:
                    divisaPais[f'{i}'] = dato[f'divisa_pais_{i}']
                    monedaPais[f'{i}'] = dato[f'pais_{i}']
                monedaDivisa['pais'] = divisaPais
                monedaDato['divisa']= monedaDivisa
                monedaDato['pais']= monedaPais
                monedaDato['artistas'] = artistasList
                id_monedas.append(dato['moneda_id'])
                monedas[dato['moneda_id']]= monedaDato
            for i in artista:
                artistaData[f'{i}'] = dato[f'artista_{i}']
            monedas[dato['moneda_id']]['artistas'].append(artistaData)
        monedas = [Moneda.model(**dato) for dato in monedas.values()]
        monedas.sort(key=lambda x: x.id)
        return monedas
    

class MonedaCreateAPIView(generics.CreateAPIView):
    serializer_class = MonedaSerializer

class MonedaRetriveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MonedaSerializer
    
    @conectar
    def get_object(self,connection):
        moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
        artista = ['id','nombre','apellido','nombreArtistico']
        moneda_artista = ['id_moneda','id_artista']
        divisa = ['id','id_pais','nombre']
        pais = ['id','nombre','nacionalidad']
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        query_action = f"""SELECT {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'paises.{i} as pais_{i}' for i in pais])},
                        {', '.join([f'M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])}
                        FROM monedas
                        INNER JOIN divisas
                        ON (divisas.id,divisas.id_pais) = (monedas.id_divisa,monedas.id_pais_divisa) 
                        INNER JOIN paises as `divisa_pais`
                        ON divisas.id_pais = divisa_pais.id
                        INNER JOIN paises
                        ON monedas.id_pais = paises.id
                        LEFT JOIN M_A
                        ON M_A.id_moneda = monedas.id
                        LEFT JOIN artistas
                        ON M_A.id_artista = artistas.id
                        WHERE monedas.id = %s
                        """
        print(query_action)
        cursor.execute(query_action,(self.kwargs.get('id'),))
        datos = cursor.fetchall()
        if datos:
            monedas = None
            id_monedas = []
            for dato in datos:
                artistaData = {}
                if dato['moneda_id'] not in id_monedas:
                    monedaDato = {}
                    monedaDivisa = {}
                    divisaPais = {}
                    monedaPais = {}
                    artistasList = []
                    for i in moneda:
                        if i != 'ano':
                            monedaDato[f'{i}'] = dato[f'moneda_{i}']
                        else:
                            monedaDato[f'{i}'] = datetime.date(year=dato[f'moneda_{i}'],month=1,day=1)
                    for i in divisa:
                        monedaDivisa[f'{i}'] = dato[f'divisa_{i}']
                    for i in pais:
                        divisaPais[f'{i}'] = dato[f'divisa_pais_{i}']
                        monedaPais[f'{i}'] = dato[f'pais_{i}']
                    monedaDivisa['pais'] = divisaPais
                    monedaDato['divisa']= monedaDivisa
                    monedaDato['pais']= monedaPais
                    monedaDato['artistas'] = artistasList
                    id_monedas.append(dato['moneda_id'])
                    monedas= monedaDato
                for i in artista:
                    artistaData[f'{i}'] = dato[f'artista_{i}']
                monedas['artistas'].append(artistaData)
            return Moneda.model(**monedas)
        else:
            raise Http404
    @conectar
    def perform_destroy(self, instance,connection):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM monedas WHERE id = %s",(instance.id,))
        connection.commit()
