from rest_framework import serializers
from database.conexion import conectar 
from apps.commons.models import Pais

            
class PaisSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=30)
    nacionalidad = serializers.CharField(max_length=30)

    @conectar
    def validate_nombre(self, nombre,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM paises WHERE nombre = %s"""
        cursor.execute(mysql_query,(nombre,))
        if cursor.fetchone():
            raise serializers.ValidationError('El Nombre del Pais ya existe')
        return nombre

    @conectar
    def validate_nacionalidad(self, nacionalidad,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM paises WHERE nacionalidad = %s"""
        cursor.execute(mysql_query,(nacionalidad,))
        if cursor.fetchone():
            raise serializers.ValidationError('El Nombre de la Nacionalidad ya existe')
        return nacionalidad

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_insert_query = """INSERT INTO paises (nombre, nacionalidad) 
                                VALUES (%s, %s)"""
        cursor = connection.cursor()
        pais = Pais.model(**validated_data)
        pais.normalize()
        data = (pais.nombre,pais.nacionalidad)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        pais.id = cursor.lastrowid
        return pais

    @conectar
    def update(self, instance:Pais, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
                setattr(instance,key,value)
        instance.normalize()
        pais = instance.__dict__.copy()
        pais.pop('id')
        for key,value in pais.items():
            mysql_update_query =  f"UPDATE paises SET {key} = %s WHERE id = %s"
            cursor.execute(mysql_update_query,(value,instance.id))
        connection.commit()
        return instance

    def to_representation(self, instance:Pais):
        instance.to_representation()
        pais= instance.__dict__
        return pais