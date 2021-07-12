from rest_framework import serializers
from database.conexion import conectar 
from database.jsonFormat import get_json
from apps.commons.models import Divisa,Pais

            
class DivisaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=30)
    id_pais = serializers.IntegerField()

    @conectar
    def validate_id_pais(self,id_pais,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        cursor.execute(mysql_query,(id_pais,))
        if cursor.fetchone():
            return id_pais
        raise serializers.ValidationError('El Pais no Existe')

    # def validate(self, attrs):
    #     return super().validate(attrs)

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_query = """SELECT * FROM paises WHERE id= %s"""
        mysql_insert_query = """INSERT INTO divisas (nombre, id_pais) 
                                VALUES (%s, %s)"""
        cursor = connection.cursor(dictionary=True)
        divisa = Divisa(**validated_data)
        divisa.normalize()
        cursor.execute(mysql_query,(divisa.id_pais,))
        pais = Pais.model(**cursor.fetchone())
        divisa.pais = pais
        data = (divisa.nombre,divisa.id_pais)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        divisa.id = cursor.lastrowid
        return divisa

    @conectar
    def update(self, instance:Divisa, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
                setattr(instance,key,value)
        instance.normalize()
        divisa = instance.__dict__.copy()
        divisa.pop('id')
        divisa.pop('id_pais')
        divisa.pop('pais')
        for key,value in divisa.items():
            mysql_update_query =  f"""UPDATE divisas SET {key} """
            mysql_update_query+= """= %s WHERE (id, id_pais) = (%s, %s)"""
            print(mysql_update_query)
            cursor.execute(mysql_update_query,(value,instance.id,instance.id_pais))
        connection.commit()
        return instance

    def to_representation(self, instance:Divisa):
        instance.to_representation()
        divisa = get_json(instance)
        return divisa