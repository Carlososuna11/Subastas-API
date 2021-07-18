
from rest_framework import serializers
from database.conexion import conectar 
from apps.commons.models import Artista

            
class ArtistaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=30,required=False)
    apellido = serializers.CharField(max_length=30,required=False)
    nombreArtistico = serializers.CharField(max_length=30,required=False)
    
    @conectar
    def create(self, validated_data:dict,connection):
        mysql_insert_query = """INSERT INTO caj_artistas (nombre, apellido, nombreArtistico) 
                                VALUES (%s, %s, %s)"""
        cursor = connection.cursor()
        artista = Artista.model(**validated_data)
        artista.normalize()
        data = (artista.nombre,artista.apellido,artista.nombreArtistico)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        artista.id = cursor.lastrowid
        return artista

    @conectar
    def update(self, instance:Artista, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
                setattr(instance,key,value)
        instance.normalize()
        pais = instance.__dict__.copy()
        pais.pop('id')
        for key,value in pais.items():
            mysql_update_query =  f"UPDATE caj_artistas SET {key} = %s WHERE id = %s"
            cursor.execute(mysql_update_query,(value,instance.id))
        connection.commit()
        return instance

    def to_representation(self, instance:Artista):
        instance.to_representation()
        artista= instance.__dict__
        return artista