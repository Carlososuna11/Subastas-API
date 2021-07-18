import datetime
from apps.commons.models import *
from apps.organizaciones.models import *

class Coleccionista:
    """Representacion en Objeto de la Entidad Coleccionista"""
    def __init__(self,dni:str,nombre:str,apellido:str,segundoApellido:str,
        telefono:str,email:str,fechaNacimiento:datetime.date,id_pais_nacio:int,
        id_pais_reside:int,segundoNombre:str=None,pais_nacio:Pais=None,pais_reside:Pais=None,id=None):
        self.id = id
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
        if self.pais_reside:
            self.pais_reside.to_representation()
        if self.pais_nacio:
            self.pais_nacio.to_representation()
    
    @classmethod
    def model(cls, **kwargs):
        if 'pais_nacio' in kwargs:
            kwargs['pais_nacio'] = Pais.model(**kwargs['pais_nacio'])
        if 'pais_reside' in kwargs:
            kwargs['pais_reside'] = Pais.model(**kwargs['pais_reside'])
        return cls(**kwargs)

class Cliente:
    """Representacion en Objeto de la Entidad Cliente"""
    def __init__(self,id_coleccionista:int,id_organizacion:int,fechaIngreso:datetime.date=None,
                numeroExpedienteUnico:int=None,coleccionista:Coleccionista=None,organizacion:Organizacion=None):
        self.id_coleccionista = id_coleccionista
        self.id_organizacion = id_organizacion
        self.fechaIngreso= fechaIngreso
        self.numeroExpedienteUnico = numeroExpedienteUnico
        self.organizacion = organizacion
        self.coleccionista = coleccionista

    def normalize(self):
        if self.organizacion:
            self.organizacion.normalize()
        if self.coleccionista:
            self.coleccionista.normalize()
    
    def to_representation(self):
        self.organizacion.to_representation()
        self.coleccionista.to_representation()
    
    @classmethod
    def model(cls, **kwargs):
        if 'organizacion' in kwargs:
            kwargs['organizacion'] = Organizacion.model(**kwargs['organizacion'])
        if 'coleccionista' in kwargs:
            kwargs['coleccionista'] = Coleccionista.model(**kwargs['coleccionista'])
        return cls(**kwargs)