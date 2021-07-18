from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Pais
from apps.eventos.models import *

            
class CostoEnvioSerializer(serializers.Serializer):
    id_pais = serializers.IntegerField()
    id_evento = serializers.IntegerField()
    costoExtra = serializers.FloatField(required=False,min_value=0)

    @conectar
    def validate_id_pais(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais,))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('El Pais no Existe')

    @conectar
    def validate_id_evento(self,id_evento,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_eventos WHERE id= %s"""
        cursor.execute(mysql_query,(id_evento,))
        if cursor.fetchone():
            return id_evento
        raise serializers.ValidationError('El evento no Existe')

    @conectar    
    def validate(self, attrs,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_costoEnvios WHERE (id_evento,id_pais) = (%s, %s)"""
        cursor.execute(mysql_query,(attrs['id_evento'],attrs['id_pais']))
        if cursor.fetchone():
            raise serializers.ValidationError('El costo de Envio para el pais Ya existe')
        return attrs

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO caj_costoEnvios (id_evento,id_pais,costoExtra) 
                                VALUES (%s, %s, %s)"""
        cursor = connection.cursor(dictionary=True)
        costoEnvio = CostoEnvio.model(**validated_data)
        costoEnvio.normalize()
        cursor.execute(mysql_query,(costoEnvio.id_pais,))
        costoEnvio.pais=Pais.model(**cursor.fetchone())
        data = (costoEnvio.id_evento,costoEnvio.id_pais,costoEnvio.costoExtra)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        costoEnvio.id = cursor.lastrowid
        return costoEnvio

    @conectar
    def update(self, instance:CostoEnvio, validated_data:dict,connection):
        mysql_query = """SELECT * FROM caj_paises WHERE id= %s"""
        cursor = connection.cursor()
        for key,value in validated_data.items():
                setattr(instance,key,value)
                if key in ['id_pais']:
                    cursor.execute(mysql_query,(value,))
                    setattr(instance,'pais',Pais.model(**cursor.fetchone()))
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('id')
        divisa.pop('id_evento')
        divisa.pop('pais')
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE caj_costoEnvios SET {key} """
            mysql_update_query+= """= %s WHERE (id,id_evento) = (%s, %s)"""
            print(mysql_update_query)
            cursor.execute(mysql_update_query,(value,instance.id,instance.id_evento))
        connection.commit()
        return instance

    def to_representation(self, instance:CostoEnvio):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa