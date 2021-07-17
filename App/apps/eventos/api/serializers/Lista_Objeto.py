from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.eventos.models import *


class Lista_ObjetoSerializer(serializers.Serializer):
    precio = serializers.DecimalField(13,2,min_value=1)
    porcentajeGananciaMin = serializers.DecimalField(8,2,min_value=0)
    id_evento = serializers.IntegerField()
    nur_moneda = serializers.IntegerField(required=False)
    id_pintura = serializers.IntegerField(required=False)
    
    @conectar
    def validate_nur_moneda(self,nur_moneda,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM Catalogo_Moneda_Tienda WHERE nur= %s"""
        cursor.execute(mysql_query,(nur_moneda,))
        if cursor.fetchone():
            return nur_moneda
        raise serializers.ValidationError('La moneda no Existe')
  
    @conectar
    def validate_id_pintura(self,id_pintura,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM Catalogo_Pintura_Tienda WHERE nur= %s"""
        cursor.execute(mysql_query,(id_pintura,))
        if cursor.fetchone():
            return id_pintura
        raise serializers.ValidationError('La Pintura no Existe')

    # def validate(self, attrs):
    #     return super().validate(attrs)

    @conectar
    def create(self, validated_data:dict,connection):
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
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        mysql_moneda_query = f"""SELECT 
                        {', '.join([f'Catalogo_Moneda_Tienda.{i} as catalogo_{i}' for i in catalogo_moneda_tienda])},
                        {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
                        {', '.join([f'divisas.{i} as divisa_{i}' for i in divisa])},
                        {', '.join([f'`divisa_pais`.{i} as divisa_pais_{i}' for i in pais])},
                        {', '.join([f'moneda_pais.{i} as moneda_pais_{i}' for i in pais])},
                        {', '.join([f'M_A.{i} as moneda_artista_{i}' for i in moneda_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])}
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
                        WHERE Catalogo_Moneda_Tienda.nur = %s
                        """
        cursor = connection.cursor(dictionary=True)
        #query = self.request.query_params.get('id_pais',None)
        mysql_pintura_query = f"""SELECT 
                        {', '.join([f'Catalogo_Pintura_Tienda.{i} as catalogo_{i}' for i in pintura])},
                        {', '.join([f'P_A.{i} as pintura_artista_{i}' for i in pintura_artista])},
                        {', '.join([f'artistas.{i} as artista_{i}' for i in artista])}
                        FROM Catalogo_Pintura_Tienda
                        LEFT JOIN P_A
                        ON P_A.id_pintura = Catalogo_Pintura_Tienda.nur
                        LEFT JOIN artistas
                        ON P_A.id_artista = artistas.id
                        WHERE Catalogo_Pintura_Tienda.nur = %s
                        """
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO Lista_Objetos (id_evento, id_eventoParticipante, id_pintura, nur_moneda,
                            id_moneda, porcentajeGananciaMin, bid, ask, precioAlcanzado, orden, duracionmin, razonNoVenta, fechaIngresoParticipante,
                            id_coleccionistaParticipante, id_organizacionParticipante) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        #------------PINTURA --------
        if 'id_pintura' in validated_data and validated_data['id_pintura']!= None:
            cursor.execute(mysql_pintura_query,(validated_data['id_pintura'],))
            datos = cursor.fetchall()
            catalogo = None
            pinturas = {}
            id_pinturas = []
            for dato in datos:
                #print(dato)
                artistaData = {}
                if dato['catalogo_nur'] not in id_pinturas: #---Meto todo en catalogo
                    catalogoDato={}
                    artistasList = []
                    for i in pintura:
                        if i!= 'ano':
                            catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                        else:
                            if dato[f'catalogo_{i}'] != None:
                                catalogoDato[f'{i}']= datetime.date(year=dato[f'catalogo_{i}'],month=1,day=1)
                            else:
                                catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
                    catalogoDato['artistas'] = artistasList
                    id_pinturas.append(dato['catalogo_nur'])
                    pinturas[dato['catalogo_nur']]= catalogoDato
                    #----Asignaciones de Objetos
                    catalogo=catalogoDato
                for i in artista:
                    artistaData[f'{i}'] = dato[f'artista_{i}']
                pinturas[dato['catalogo_nur']]['artistas'].append(artistaData)
            validated_data['pintura']=catalogo
        #------------Catalogo_Moneda_Tienda
        else:
            cursor.execute(mysql_moneda_query,(validated_data['id_moneda'],))
            catalogo = None
            monedas = {}
            datos = cursor.fetchall()
            id_monedas = []
            for dato in datos:
                artistaData = {}
                if dato['moneda_id'] not in id_monedas: #---Meto todo en catalogo
                    catalogoDato={}
                    monedaDato = {}
                    monedaDivisa = {}
                    divisaPais = {}
                    monedaPais = {}
                    artistasList = []
                    for i in catalogo_moneda_tienda:
                        catalogoDato[f'{i}'] = dato[f'catalogo_{i}']
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
                    catalogo=catalogoDato
                for i in artista:
                    artistaData[f'{i}'] = dato[f'artista_{i}']
                monedas[dato['moneda_id']]['artistas'].append(artistaData)
            validated_data['moneda']=catalogo
        validated_data['bid'] = 0
        validated_data['ask'] = validated_data['precio']*(1+(validated_data['porcentajeGananciaMin']/100))
        validated_data.pop('precio')
        objetos = Lista_Objeto.model(**validated_data)
        objetos.normalize()
        data = (objetos.id_evento,objetos.id_eventoParticipante,objetos.id_pintura,objetos.nur_moneda,objetos.id_moneda,
                objetos.porcentajeGananciaMin,objetos.bid,objetos.ask,objetos.precioAlcanzado,objetos.orden,objetos.duracionmin,
                objetos.razonNoVenta,objetos.fechaIngresoParticipante,objetos.id_coleccionistaParticipante,objetos.id_organizacionParticipante)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        objetos.id = cursor.lastrowid
        return objetos

    @conectar
    def update(self, instance:Lista_Objeto, validated_data:dict,connection):
        cursor = connection.cursor()
        instance.porcentajeGananciaMin = validated_data['porcentajeGananciaMin']
        instance.ask  = validated_data['precio']*(1+(validated_data['porcentajeGananciaMin']/100))
        instance.normalize()
        mysql_update_query =  """UPDATE Lista_Objetos SET ask = %s, porcentajeGananciaMin = %s WHERE id = %s"""
        cursor.execute(mysql_update_query,(instance.ask,instance.porcentajeGananciaMin,instance.id))
        connection.commit()
        return instance

    def to_representation(self, instance:Lista_Objeto):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa