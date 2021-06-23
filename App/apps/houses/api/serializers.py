
from rest_framework import serializers
from database.conexion import conectar 
from apps.houses.models import Casa
import os

def saveImage(image,id):
    _,file_extension = os.path.splitext(str(image))
    with open(f'media/img/house{id}{file_extension}', 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)
            
class HouseSerializer(serializers.Serializer):
    habitaciones = serializers.IntegerField(min_value=0)
    banos = serializers.IntegerField(min_value=0)
    gas = serializers.BooleanField()
    balcon = serializers.BooleanField()
    imagen = serializers.ImageField(allow_null=True,allow_empty_file=True)


    @conectar
    def create(self, validated_data:dict,connection):
        
        mysql_insert_query = """INSERT INTO casas (habitaciones, banos, gas, balcon, imagen) 
                                VALUES (%s, %s, %s, %s, %s) """
        cursor = connection.cursor()
        casa = Casa(**validated_data)
        casa.imagen='default.png'
        data = (casa.habitaciones,casa.banos,casa.gas,casa.balcon,casa.imagen)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        casa.id = cursor.lastrowid
        if validated_data['imagen']:
            saveImage(validated_data['imagen'],casa.id)
            _,file_extension = os.path.splitext(str(validated_data['imagen']))
            casa.imagen =f"house{casa.id}{file_extension}" 
            mysql_update_query =  "UPDATE casas SET imagen = %s WHERE id = %s"
            cursor.execute(mysql_update_query,(casa.imagen,Casa.id))
            connection.commit()
        return casa

    @conectar
    def update(self, instance:Casa, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
            # instance.nombre = validated_data.get('nombre',instance.nombre)
            if key != 'imagen':
                mysql_update_query =  f"UPDATE casas SET {key} = %s WHERE id = %s"
                cursor.execute(mysql_update_query,(value,instance.id))
                setattr(instance,key,value)
            else:
                
                if value:
                    saveImage(validated_data['imagen'],instance.id)
                    _,file_extension = os.path.splitext(str(validated_data['imagen']))
                    instance.imagen =f"house{instance.id}{file_extension}"
                else:
                    instance.imagen = 'default.png' 
                mysql_update_query =  "UPDATE casas SET imagen = %s WHERE id = %s"
                cursor.execute(mysql_update_query,(instance.imagen,instance.id))
        connection.commit()
        return instance

    
    def to_representation(self, instance):
        producto = instance.__dict__
        producto['gas'] = 'Si' if producto['gas'] else 'No'
        producto['balcon'] = 'Si' if producto['balcon'] else 'No'
        producto['imagen'] = '' if producto['imagen']==None else f"media/img/{producto['imagen']}"
        return producto
    # def save(self,connection):
    #     pass


    # return super().to_representation(instance)