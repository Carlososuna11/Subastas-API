from rest_framework import serializers
from database.conexion import conectar 
from apps.eventos.models import Planificador

            
class PlanificadorSerializer(serializers.Serializer):
    id_organizacion = serializers.IntegerField()
    id_evento = serializers.IntegerField()

    @conectar
    def validate_id_organizacion(self, id_organizacion,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_organizaciones WHERE id = %s"""
        cursor.execute(mysql_query,(id_organizacion,))
        if cursor.fetchone():
            return id_organizacion    
        raise serializers.ValidationError('La caj_organización no Existe')
        

    @conectar
    def validate_id_evento(self, id_evento,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_eventos WHERE id = %s"""
        cursor.execute(mysql_query,(id_evento,))
        if cursor.fetchone():
            return id_evento
        raise serializers.ValidationError('El Evento no existe')

    @conectar
    def validate(self,validated_data,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM caj_planificadores WHERE (id_organizacion,id_evento) = (%s, %s)"""
        cursor.execute(mysql_query,(validated_data['id_organizacion'],validated_data['id_evento']))
        if cursor.fetchone():
            raise serializers.ValidationError('Ya existe dicha organizacion para el Evento')
        return validated_data

    @conectar
    def create(self, validated_data:dict,connection):
        mysql_insert_query = """INSERT INTO caj_planificadores (id_evento, id_organizacion) 
                                VALUES (%s, %s)"""
        cursor = connection.cursor()
        planificador = Planificador.model(**validated_data)
        planificador.normalize()
        data = (planificador.id_evento,planificador.id_organizacion)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        return planificador

    # @conectar
    # def update(self, instance:Planificador, validated_data:dict,connection):
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

    def to_representation(self, instance:Planificador):
        instance.to_representation()
        pais= instance.__dict__
        return pais