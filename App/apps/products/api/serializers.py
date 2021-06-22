
from rest_framework import serializers
from database.conexion import conectar 
from apps.products.models import Producto
import os

def saveImage(image,id):
    _,file_extension = os.path.splitext(str(image))
    with open(f'media/img/product{id}{file_extension}', 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)
class ProductSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=50)
    descripcion = serializers.CharField(max_length=500,style={'base_template':'textarea.html'})
    precio = serializers.DecimalField(max_digits=10,decimal_places=2,min_value=0)
    imagen = serializers.ImageField(allow_null=True,allow_empty_file=True)


    @conectar
    def create(self, validated_data:dict,connection):
        
        mysql_insert_query = """INSERT INTO productos (nombre, descripcion, precio) 
                                VALUES (%s, %s, %s) """
        cursor = connection.cursor()
        producto = Producto(**validated_data)
        data = (producto.nombre,producto.descripcion,producto.precio)
        cursor.execute(mysql_insert_query,data)
        connection.commit()
        producto.id = cursor.lastrowid
        if validated_data['imagen']:
            saveImage(validated_data['imagen'],producto.id)
            _,file_extension = os.path.splitext(str(validated_data['imagen']))
            producto.imagen =f"product{producto.id}{file_extension}" 
            mysql_update_query =  "UPDATE productos SET imagen = %s WHERE id = %s"
            cursor.execute(mysql_update_query,(producto.imagen,producto.id))
            connection.commit()
        return producto

    @conectar
    def update(self, instance:Producto, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
            # instance.nombre = validated_data.get('nombre',instance.nombre)
            if key != 'imagen':
                mysql_update_query =  f"UPDATE productos SET {key} = %s WHERE id = %s"
                cursor.execute(mysql_update_query,(value,instance.id))
                setattr(instance,key,value)
            else:
                
                if value:
                    saveImage(validated_data['imagen'],instance.id)
                    _,file_extension = os.path.splitext(str(validated_data['imagen']))
                    instance.imagen =f"product{instance.id}{file_extension}"
                else:
                    instance.imagen = value 
                mysql_update_query =  "UPDATE productos SET imagen = %s WHERE id = %s"
                cursor.execute(mysql_update_query,(instance.imagen,instance.id))
        connection.commit()
        return instance

    
    def to_representation(self, instance):
        producto = instance.__dict__
        producto['imagen'] = '' if producto['imagen']==None else f"media/img/{producto['imagen']}"
        return producto
    # def save(self,connection):
    #     pass


    # return super().to_representation(instance)