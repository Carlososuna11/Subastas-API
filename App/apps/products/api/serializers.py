
from rest_framework import serializers
from database.conexion import conectar 
from apps.products.models import Producto
import os
import simplejson as json
from pyreportjasper import PyReportJasper


def json_to_pdf():
    input_file = './static/jaspersoft/productos.jrxml'
    output_file = './media/pdf/productos'
    conn = {
        'driver': 'json',
        'data_file': './media/reports/productos.json',
        'json_query': 'productos'
    }
    pyreportjasper = PyReportJasper()
    pyreportjasper.config(
        input_file,
        output_file,
        output_formats=["pdf"],
        db_connection=conn
    )
    pyreportjasper.process_report()
    print('Result is the file below.')
    print(output_file + '.pdf')


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
        #producto.imagen = 'default.png'
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
                    instance.imagen = None 
                mysql_update_query =  "UPDATE productos SET imagen = %s WHERE id = %s"
                cursor.execute(mysql_update_query,(instance.imagen,instance.id))
        connection.commit()
        return instance

    
    def to_representation(self, instance):
        producto = instance.__dict__
        producto['imagen'] = 'media/img/default.png' if not(producto['imagen']) else f"media/img/{producto['imagen']}"
        return producto

    @conectar
    def save(self,connection, **kwargs):
        retornar =  super().save(**kwargs)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = { "productos" : [self.to_representation(Producto(**dato)) for dato in cursor]}
        with open('./media/reports/productos.json', 'w') as outfile:
            json.dump(productos,outfile, indent=4,encoding="utf-8")
        try:
            json_to_pdf()
        except Exception as e:
            print(e)
        return retornar
    # def save(self,connection):
    #     pass


    # return super().to_representation(instance)