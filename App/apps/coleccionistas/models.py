import datetime
from apps.commons.models import *


class Coleccionista:
    """Representacion en Objeto de la Entidad Coleccionista"""
    def __init__(self,dni:int,nombre:str,apellido:str,segundoApellido:str,
        telefono:str,email:str,fechaNacimiento:datetime.date,id_pais_nacio:int,
        id_pais_reside:int,segundoNombre:str=None,pais_nacio:Pais=None,pais_reside:Pais=None):
        self.dni = dni
        self.nombre = nombre
        self.segundoNombre = segundoNombre
        self.apellido = apellido
        self.segundoApellido = segundoApellido
        self.telefono = telefono
        self.email = email
        self.fechaNacimiento = fechaNacimiento
        self.id_pais_reside = id_pais_reside
        self.id_pais_nacio = id_pais_nacio
        self.pais_nacio = pais_nacio
        self.pais_reside = pais_reside

    def normalize(self):
        self.nombre = self.nombre.lower()
        self.segundoNombre = None if self.segundoNombre==None else self.segundoNombre.lower()
        self.apellido = self.apellido.lower()
        self.segundoApellido = self.segundoApellido.lower()
        self.email = self.email.lower()
        if self.pais_nacio:
            self.pais_nacio.normalize()
        if self.pais_reside:
            self.pais_reside.normalize()
        
    def to_representation(self):
        self.nombre = self.nombre.capitalize()
        self.segundoNombre = '' if self.segundoNombre==None else self.segundoNombre.capitalize()
        self.apellido = self.apellido.capitalize()
        self.segundoApellido = self.segundoApellido.capitalize()
        self.pais_nacio.to_representation()
        self.pais_reside.to_representation()
    
    @classmethod
    def model(cls, **kwargs):
        if 'pais_nacio' in kwargs:
            kwargs['pais_nacio'] = Pais.model(**kwargs['pais_nacio'])
        if 'pais_reside' in kwargs:
            kwargs['pais_reside'] = Pais.model(**kwargs['pais_reside'])
        return cls(**kwargs)