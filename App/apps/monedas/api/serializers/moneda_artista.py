from rest_framework import serializers
from database.conexion import conectar 
from apps.monedas.models import Moneda_Artista

            
class Moneda_ArtistaSerializer(serializers.Serializer):
    id_moneda = serializers.IntegerField()
    id_artista = serializers.IntegerField()

    @conectar
    def validate_id_moneda(self, id_moneda,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM monedas WHERE id = %s"""
        cursor.execute(mysql_query,(id_moneda,))
        if cursor.fetchone():
            return id_moneda    
        raise serializers.ValidationError('La moneda no existe')
        

    @conectar
    def validate_id_artista(self, id_artista,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM artistas WHERE id = %s"""
        cursor.execute(mysql_query,(id_artista,))
        if cursor.fetchone():
            return id_artista
        raise serializers.ValidationError('El artista no existe')

    @conectar
    def validate(self,validated_data,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM M_A WHERE (id_moneda,id_artista) = (%s, %s)"""
        cursor.execute(mysql_query,(validated_data['id_moneda'],validated_data['id_artista']))
        if cursor.fetchone():
            raise serializers.ValidationError('Ya existe dicho artista para la Moneda')
        return validated_data

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_insert_query = """INSERT INTO M_A (id_moneda, id_artista) 
                                VALUES (%s, %s)"""
        cursor = connection.cursor()
        pais = Moneda_Artista.model(**validated_data)
        pais.normalize()
        data = (pais.id_moneda,pais.id_artista)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        return pais

    # @conectar
    # def update(self, instance:Moneda_Artista, validated_data:dict,connection):
    #     cursor = connection.cursor()
    #     for key,value in validated_data.items():
    #             setattr(instance,key,value)
    #     instance.normalize()
    #     pais = instance.__dict__.copy()
    #     pais.pop('id')
    #     for key,value in pais.items():
    #         mysql_update_query =  f"UPDATE paises SET {key} = %s WHERE id = %s"
    #         cursor.execute(mysql_update_query,(value,instance.id))
    #     connection.commit()
    #     return instance

    def to_representation(self, instance:Moneda_Artista):
        instance.to_representation()
        pais= instance.__dict__
        return pais