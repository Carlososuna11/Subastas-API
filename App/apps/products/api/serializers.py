from rest_framework import serializers
from database.conexion import conectar 
from apps.products.models import Producto
class ProductSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=50)
    descripcion = serializers.CharField(max_length=500,style={'base_template':'textarea.html'})
    precio = serializers.DecimalField(max_digits=10,decimal_places=2,min_value=0)
    imagen = serializers.ImageField()

    def validate_imagen(self,data):
        return data

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
        return producto

    @conectar
    def update(self, instance:Producto, validated_data:dict,connection):
        cursor = connection.cursor()
        mysql_update_query =  "UPDATE productos SET %s = %s WHERE id = %s"
        for key,value in validated_data:
            # instance.nombre = validated_data.get('nombre',instance.nombre)
            cursor.execute(mysql_update_query,(key,value,instance.id))
            setattr(instance,key,value)
        connection.commit()
        return instance
    
    # def save(self,connection):
    #     pass

    # def to_representation(self, instance):
    #     return super().to_representation(instance)