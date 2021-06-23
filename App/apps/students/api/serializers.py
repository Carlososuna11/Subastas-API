
from rest_framework import serializers
from database.conexion import conectar 
from apps.students.models import Estudiante
import os

def saveImage(image,id):
    _,file_extension = os.path.splitext(str(image))
    with open(f'media/img/student{id}{file_extension}', 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)

class StudentSerializer(serializers.Serializer):
    dni = serializers.IntegerField(min_value=0)
    nombre = serializers.CharField(max_length=50)
    apellido = serializers.CharField(max_length=50)
    segundoApellido = serializers.CharField(max_length=50)
    segundoNombre = serializers.CharField(max_length=50,required=False)
    imagen = serializers.ImageField(allow_null=True,allow_empty_file=True)

    @conectar
    def validate_dni(self, dni,connection):
        cursor = connection.cursor()
        mysql_query = """SELECT * FROM estudiantes WHERE dni = %s"""
        cursor.execute(mysql_query,(dni,))
        if cursor.fetchone():
            raise serializers.ValidationError('El DNI ya existe')
        return dni

    @conectar
    def create(self, validated_data:dict,connection):
        
        mysql_insert_query = """INSERT INTO estudiantes (dni, nombre, apellido, segundoApellido, imagen) 
                                VALUES (%s, %s, %s, %s, %s) """
        cursor = connection.cursor()
        estudiante = Estudiante(**validated_data)
        estudiante.imagen='default.png'
        data = (estudiante.dni,estudiante.nombre,estudiante.apellido,estudiante.segundoApellido,estudiante.imagen)
        cursor.execute(mysql_insert_query,data)
        if 'segundoNombre' in validated_data:
            cursor.execute('UPDATE estudiantes SET segundoNombre = %s WHERE dni=%s',(estudiante.segundoNombre,estudiante.dni))
        if validated_data['imagen']:
            saveImage(validated_data['imagen'],estudiante.dni,)
            _,file_extension = os.path.splitext(str(validated_data['imagen']))
            estudiante.imagen =f"student{estudiante.dni}{file_extension}" 
            mysql_update_query =  "UPDATE estudiantes SET imagen = %s WHERE dni = %s"
            cursor.execute(mysql_update_query,(estudiante.imagen,estudiante.dni))
        connection.commit()
        return estudiante

    @conectar
    def update(self, instance:Estudiante, validated_data:dict,connection):
        cursor = connection.cursor()
        for key,value in validated_data.items():
            # instance.nombre = validated_data.get('nombre',instance.nombre)
            if key != 'imagen':
                mysql_update_query =  f"UPDATE estudiantes SET {key} = %s WHERE dni = %s"
                cursor.execute(mysql_update_query,(value,instance.dni))
                setattr(instance,key,value)
            else:
                
                if value:
                    saveImage(validated_data['imagen'],instance.id)
                    _,file_extension = os.path.splitext(str(validated_data['imagen']))
                    instance.imagen =f"student{instance.id}{file_extension}"
                else:
                    instance.imagen = 'default.png'
                mysql_update_query =  "UPDATE estudiantes SET imagen = %s WHERE dni = %s"
                cursor.execute(mysql_update_query,(instance.imagen,instance.dni))
        connection.commit()
        return instance

    
    def to_representation(self, instance):
        producto = instance.__dict__
        producto['imagen'] = 'default.png' if producto['imagen']==None else f"media/img/{producto['imagen']}"
        return producto
    # def save(self,connection):
    #     pass


    # return super().to_representation(instance)