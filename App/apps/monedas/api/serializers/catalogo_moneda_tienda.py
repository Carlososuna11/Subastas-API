from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.monedas.models import *


class Catalogo_Moneda_TiendaSerializer(serializers.Serializer):
    id_moneda = serializers.IntegerField()
    id_organizacion = serializers.IntegerField(required=False)
    #id_coleccionista = serializers.IntegerField(required=False)

    # @conectar
    # def validate_id_coleccionista(self,id_coleccionista,connection):
    #     cursor = connection.cursor()
    #     mysql_query = """SELECT * FROM coleccionistas WHERE id= %s"""
    #     cursor.execute(mysql_query,(id_coleccionista,))
    #     if cursor.fetchone():
    #         return id_coleccionista
    #     raise serializers.ValidationError('El Coleccionista no Existe')

    @conectar
    def validate_id_moneda(self,id_moneda,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM monedas WHERE id= %s"""
        cursor.execute(mysql_query,(id_moneda,))
        if cursor.fetchone():
            return id_moneda
        raise serializers.ValidationError('El La moneda no Existe')

    @conectar
    def validate_id_organizacion(self,id_organizacion,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM organizaciones WHERE id= %s"""
        cursor.execute(mysql_query,(id_organizacion,))
        if cursor.fetchone():
            return id_organizacion
        raise serializers.ValidationError('La Organizacion No existe')
    
    # @conectar
    # def validate_email(self,email,connection):
    #     cursor = connection.cursor()
    #     mysql_query = """SELECT * FROM coleccionistas WHERE email= %s"""
    #     cursor.execute(mysql_query,(email,))
    #     if cursor.fetchone():
    #         raise serializers.ValidationError('El email ya Existe')
    #     return email

    # @conectar
    # def validate_telefono(self,telefono,connection):
    #     cursor = connection.cursor()
    #     mysql_query = """SELECT * FROM coleccionistas WHERE telefono= %s"""
    #     cursor.execute(mysql_query,(telefono,))
    #     if cursor.fetchone():
    #         raise serializers.ValidationError('El telefono ya Existe')
    #     return telefono


    # def validate(self, attrs):
    #     return super().validate(attrs)
    
    # @conectar
    # def validate(self,validated_data):
    #     if validated_data.get('id_organizacion',None) and validated_data.get('id_coleccionista',None):
    #         raise serializers.ValidationError('Un objeto no Puede Tener organizacion y coleccionista a la vez')
    #     return validated_data

    @conectar
    def create(self, validated_data:dict,connection):
        moneda = ['id','nombre','denominacion','mintage','forma','metal','diametromm','canto',
        'pesogr','ano','motivo','acunacion','anverso','reverso','id_pais_divisa','id_pais','id_divisa',
        'imagen']
        artista = ['id','nombre','apellido','nombreArtistico']
        moneda_artista = ['id_moneda','id_artista']
        divisa = ['id','id_pais','nombre']
        pais = ['id','nombre','nacionalidad']
        coleccionista = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
                        'fechaNacimiento','id_pais_nacio','id_pais_reside']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        mysql_query_coleccionista = f"""SELECT 
                            {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
                            {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
                            {', '.join([f'paises.{i} as pais_reside_{i}' for i in pais])}
                        FROM coleccionistas
                        INNER JOIN paises as pais_nacio
                        ON pais_nacio.id = coleccionistas.id_pais_nacio
                        INNER JOIN paises
                        ON paises.id = coleccionistas.id_pais_reside
                        WHERE coleccionistas.dni = %s
                        """
        mysql_query_organizacion = f"""SELECT 
                        {', '.join([f'organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'paises.{i} as pais_{i}' for i in pais])}
                        FROM organizaciones
                        INNER JOIN paises
                        ON paises.id = organizaciones.id_pais
                        WHERE organizaciones.id = %s
                        """
        mysql_query_moneda = f"""SELECT {', '.join([f'monedas.{i} as moneda_{i}' for i in moneda])},
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
        mysql_insert_query = """INSERT INTO Catalogo_Moneda_Tienda (id_moneda, id_coleccionista, id_organizacion) 
                                VALUES (%s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        catalogo = Catalogo_Moneda_Tienda.model(**validated_data)
        catalogo.normalize()
        #-------Moneda----------------------------
        cursor.execute(mysql_query_moneda,(catalogo.id_moneda,))
        datos = cursor.fetchall()
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
        catalogo.moneda = Moneda.model(**monedas)
        #-------coleccionista (si existe) ---------
        # if validated_data.get('id_coleccionista',None):
        #     cursor.execute(mysql_query_coleccionista,(catalogo.id_coleccionista,))
        #     dato = cursor.fetchone()
        #     coleccionistaData = {}
        #     paisNacio = {}
        #     paisReside = {}
        #     for i in coleccionista:
        #         coleccionistaData[f'{i}'] = dato[f'coleccionista_{i}']
        #     for i in pais:
        #         paisReside[f'{i}'] = dato[f'pais_reside_{i}']
        #         paisNacio[f'{i}'] = dato[f'pais_nacio_{i}']
        #     coleccionistaData['pais_reside']= paisReside
        #     coleccionistaData['pais_nacio']=paisNacio
        #     catalogo.coleccionista = Coleccionista.model(**coleccionistaData)
        # else:
            #-----------------Organizacion:-----------------
        cursor.execute(mysql_query_organizacion,(catalogo.id_organizacion,))
        dato = cursor.fetchone()
        organizacionData = {}
        paisReside = {}
        print(dato)
        for i in organizacion:
            organizacionData[f'{i}'] = dato[f'organizacion_{i}']
        for i in pais:
            paisReside[f'{i}'] = dato[f'pais_{i}']
        organizacionData['pais']= paisReside
        catalogo.organizacion = Organizacion.model(**organizacionData)
        #-------Insertar data--------
        data = (catalogo.id_moneda,catalogo.id_coleccionista,catalogo.id_organizacion)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        catalogo.nur = cursor.lastrowid
        return catalogo

    # @conectar
    # def update(self, instance:Catalogo_Moneda_Tienda, validated_data:dict,connection):
    #     cursor = connection.cursor()
    #     pais_objeto ={
    #         'id_pais_reside':'pais_reside',
    #         'id_pais_nacio':'pais_nacio'
    #     }
    #     mysql_query = """SELECT * FROM paises WHERE id= %s"""
    #     for key,value in validated_data.items():
    #             setattr(instance,key,value)
    #             if key in ['id_moneda','id_pais_nacio']:
    #                cursor.execute(mysql_query,(value,))
    #                setattr(instance,pais_objeto[key],Pais.model(**cursor.fetchone()))
                   
    #     instance.normalize()
    #     divisa = instance.__dict__.copy()
    #     divisa.pop('dni')
    #     divisa.pop('pais_reside')
    #     divisa.pop('pais_nacio')
    #     for key,value in divisa.items():
    #         mysql_update_query =  f"""UPDATE coleccionistas SET {key} """
    #         mysql_update_query+= """= %s WHERE dni = %s"""
    #         cursor.execute(mysql_update_query,(value,instance.dni))
    #     connection.commit()
    #     return instance

    def to_representation(self, instance:Catalogo_Moneda_Tienda):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa