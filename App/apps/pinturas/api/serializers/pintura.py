from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from database.saveImage import saveImage
from database.random_nur import random_nur
from apps.commons.models import Pais
from apps.pinturas.models import *
import os

required_formats = ['%Y', '%d-%m-%Y']
class PinturaSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=100)
    dimensionescm = serializers.CharField(max_length=20)
    id_organizacion = serializers.IntegerField()
    estilo = serializers.CharField(max_length=30)
    ano = serializers.DateField(input_formats=required_formats,required=False)
    imagen = serializers.ImageField(allow_null=True,allow_empty_file=True,required=False)

    #id_coleccionista = serializers.IntegerField(required=False)

    def validate_ano(self,ano):
        return ano.year

    # @conectar
    # def validate_id_coleccionista(self,id_coleccionista,connection):
    #     cursor = connection.cursor()
    #     mysql_query = """SELECT * FROM coleccionistas WHERE id= %s"""
    #     cursor.execute(mysql_query,(id_coleccionista,))
    #     if cursor.fetchone():
    #         return id_coleccionista
    #     raise serializers.ValidationError('El Coleccionista no Existe')

    @conectar
    def validate_id_organizacion(self,id_organizacion,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_organizaciones WHERE id= %s"""
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
        # artista = ['id','nombre','apellido','nombreArtistico']
        # moneda_artista = ['id_moneda','id_artista']
        # divisa = ['id','id_pais','nombre']
        pais = ['id','nombre','nacionalidad']
        # coleccionista = ['dni','nombre','segundoNombre','apellido','segundoApellido','telefono','email',
        #                 'fechaNacimiento','id_pais_nacio','id_pais_reside']
        organizacion = ['id','nombre','proposito','fundacion','alcance','tipo','telefonoPrincipal',
                        'paginaWeb','emailCorporativo','id_pais']
        # mysql_query_coleccionista = f"""SELECT 
        #                     {', '.join([f'coleccionistas.{i} as coleccionista_{i}' for i in coleccionista])},
        #                     {', '.join([f'pais_nacio.{i} as pais_nacio_{i}' for i in pais])},
        #                     {', '.join([f'paises.{i} as pais_reside_{i}' for i in pais])}
        #                 FROM coleccionistas
        #                 INNER JOIN paises as pais_nacio
        #                 ON pais_nacio.id = coleccionistas.id_pais_nacio
        #                 INNER JOIN paises
        #                 ON paises.id = coleccionistas.id_pais_reside
        #                 WHERE coleccionistas.dni = %s
        #                 """
        mysql_query_organizacion = f"""SELECT 
                        {', '.join([f'caj_organizaciones.{i} as organizacion_{i}' for i in organizacion])},
                        {', '.join([f'caj_paises.{i} as pais_{i}' for i in pais])}
                        FROM caj_organizaciones
                        INNER JOIN caj_paises
                        ON caj_paises.id = caj_organizaciones.id_pais
                        WHERE caj_organizaciones.id = %s
                        """
        mysql_insert_query = """INSERT INTO caj_Catalogo_Pintura_Tienda (nur,titulo, dimensionescm, estilo, ano, imagen, id_coleccionista, id_organizacion) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        validated_data['nur'] = random_nur()
        catalogo = Pintura.model(**validated_data)
        catalogo.normalize()
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
        data = (catalogo.nur, catalogo.titulo, catalogo.dimencionescm, catalogo.estilo, catalogo.ano,
                catalogo.imagen, catalogo.id_coleccionista,catalogo.id_organizacion)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        if 'imagen' in validated_data and validated_data['imagen']!= None:
            saveImage(validated_data['imagen'],'pintura',catalogo.nur)
            _,file_extension = os.path.splitext(str(validated_data['imagen']))
            catalogo.imagen =f"pintura{catalogo.nur}{file_extension}" 
            mysql_update_query =  "UPDATE caj_Catalogo_Pintura_Tienda SET imagen = %s WHERE nur = %s"
            cursor.execute(mysql_update_query,(catalogo.imagen,catalogo.nur))
            connection.commit()
        return catalogo

    @conectar
    def update(self, instance:Pintura, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
                if key not in ['nur']:
                    if key == 'imagen' and value:
                        saveImage(validated_data['imagen'],'pintura',instance.nur)
                        _,file_extension = os.path.splitext(str(validated_data['imagen']))
                        instance.imagen =f"pintura{instance.id}{file_extension}" 
                    else:
                        setattr(instance,key,value)
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('nur')
        divisa.pop('coleccionista')
        divisa.pop('organizacion')
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE caj_Catalogo_Pintura_Tienda SET {key} """
            mysql_update_query+= """= %s WHERE nur = %s"""
            cursor.execute(mysql_update_query,(value,instance.dni))
        connection.commit()
        return instance

    def to_representation(self, instance:Pintura):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa