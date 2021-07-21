from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.organizaciones.models import *

required_formats = ['%Y','%d-%m-%Y']
class OrganizacionSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=50)
    proposito = serializers.CharField()
    fundacion = serializers.DateField(input_formats=required_formats)
    alcance = serializers.CharField(max_length=15)
    tipo = serializers.CharField(max_length=10)
    telefonoPrincipal = serializers.CharField(max_length=20)
    paginaWeb = serializers.URLField(max_length=50,required=False)
    emailCorporativo = serializers.EmailField(max_length=50,required=False)
    id_pais = serializers.IntegerField()
    
    def validate_ano(self,ano):
        return ano.year
        
    @conectar
    def validate_id_pais(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais,))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('El Pais de Origen no Existe')
    
    @conectar
    def validate_emailCorporativo(self,emailCorporativo,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_organizaciones WHERE emailCorporativo= %s"""
        cursor.execute(mysql_query,(emailCorporativo,))
        if cursor.fetchone():
            raise serializers.ValidationError('El email ya Existe')
        return emailCorporativo

    @conectar
    def validate_telefonoPrincipal(self,telefonoPrincipal,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_organizaciones WHERE telefonoPrincipal= %s"""
        cursor.execute(mysql_query,(telefonoPrincipal,))
        if cursor.fetchone():
            raise serializers.ValidationError('El telefono ya Existe')
        return telefonoPrincipal

    def validate_alcance(self,alcance):
        if alcance.lower() in ['nacional','internacional']:
            return alcance.lower()
        raise serializers.ValidationError("El alcance no es Válido, solo puede ser 'nacional' o 'internacional' ")

    def validate_tipo(self,tipo):
        if tipo.lower() in ['galeria','tienda','otro']:
            return tipo.lower()
        raise serializers.ValidationError("El tipo de tienda no es Válido, solo puede ser 'galeria', 'tienda' o 'otro' ")


    # def validate(self, attrs):
    #     return super().validate(attrs)

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO caj_organizaciones (nombre, proposito, fundacion,
                                alcance, tipo, telefonoPrincipal, paginaWeb, emailCorporativo, id_pais) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        validated_data['fundacion'] =validated_data['fundacion'].year
        organizacion = Organizacion.model(**validated_data)
        organizacion.normalize()
        #-------Pais de origen ---------
        cursor.execute(mysql_query,(organizacion.id_pais,))
        organizacion.pais = Pais.model(**cursor.fetchone())
        #-------Insertar data--------
        data = (organizacion.nombre, organizacion.proposito, organizacion.fundacion, organizacion.alcance, organizacion.tipo,
                organizacion.telefonoPrincipal,organizacion.paginaWeb,organizacion.emailCorporativo,organizacion.id_pais)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        organizacion.id = cursor.lastrowid
        return organizacion

    @conectar
    def update(self, instance:Organizacion, validated_data:dict,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        for key,value in validated_data.items():
                setattr(instance,key,value)
                if key in ['id_pais']:
                   cursor.execute(mysql_query,(instance.id_pais,))
                   setattr(instance,'pais',Pais.model(**cursor.fetchone()))
                   
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('id')
        divisa.pop('pais')
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE caj_organizaciones SET {key} """
            mysql_update_query+= """= %s WHERE id = %s"""
            cursor.execute(mysql_update_query,(value,instance.id))
        connection.commit()
        return instance

    def to_representation(self, instance:Organizacion):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa