from rest_framework import serializers
from database.conexion import conectar 
from apps.pinturas.models import Pintura_Artista

            
class Pintura_ArtistaSerializer(serializers.Serializer):
    id_pintura = serializers.IntegerField()
    id_artista = serializers.IntegerField()

    @conectar
    def validate_id_pintura(self, id_pintura,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_Catalogo_Pintura_Tienda WHERE nur = %s"""
        cursor.execute(mysql_query,(id_pintura,))
        if cursor.fetchone():
            return id_pintura    
        raise serializers.ValidationError('La Pintura no existe')
        

    @conectar
    def validate_id_artista(self, id_artista,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_artistas WHERE id = %s"""
        cursor.execute(mysql_query,(id_artista,))
        if cursor.fetchone():
            return id_artista
        raise serializers.ValidationError('El artista no existe')

    @conectar
    def validate(self,validated_data,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_P_A WHERE (id_pintura,id_artista) = (%s, %s)"""
        cursor.execute(mysql_query,(validated_data['id_pintura'],validated_data['id_artista']))
        if cursor.fetchone():
            raise serializers.ValidationError('Ya existe dicho artista para la Moneda')
        return validated_data

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_insert_query = """INSERT INTO caj_P_A (id_pintura, id_artista) 
                                VALUES (%s, %s)"""
        cursor = connection.cursor()
        pais = Pintura_Artista.model(**validated_data)
        pais.normalize()
        data = (pais.id_pintura,pais.id_artista)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        return pais

    # @conectar
    # def update(self, instance:Pintura_Artista, validated_data:dict,connection):
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

    def to_representation(self, instance:Pintura_Artista):
        instance.to_representation()
        pais= instance.__dict__
        return pais