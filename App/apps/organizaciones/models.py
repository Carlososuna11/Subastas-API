import datetime
from apps.commons.models import *


class Organizacion:
    """Representacion en Objeto de la Entidad Organizacion"""
    def __init__(self,nombre:str,proposito:str,fundacion:datetime.date,alcance:str,
                tipo:str,telefonoPrincipal:str,id_pais:int,paginaWeb:str=None,emailCorporativo:str=None,
                id:int=None,pais:Pais=None):
        self.id = id
        self.nombre = nombre
        self.proposito = proposito
        self.fundacion = fundacion
        self.alcance = alcance
        self.tipo = tipo
        self.telefonoPrincipal = telefonoPrincipal
        self.id_pais = id_pais
        self.paginaWeb = paginaWeb
        self.emailCorporativo = emailCorporativo
        self.pais = pais

    def normalize(self):
        self.nombre.lower()
        self.alcance.lower()
        self.tipo.lower()
        if self.paginaWeb:
            self.paginaWeb.lower()
        if self.emailCorporativo:
            self.emailCorporativo.lower()
        if self.pais:
            self.pais.normalize()
        
    def to_representation(self):
        self.nombre.capitalize()
        self.alcance.capitalize()
        self.tipo.capitalize()
        self.paginaWeb = '' if self.paginaWeb == None else self.paginaWeb.capitalize()
        self.emailCorporativo= '' if self.emailCorporativo == None else self.emailCorporativo.capitalize()
        self.pais.to_representation()

    @classmethod
    def model(cls, **kwargs):
        if 'pais' in kwargs:
            kwargs['pais'] = Pais.model(**kwargs['pais'])
        return cls(**kwargs)


class Contacto:
    """Representacion en Objeto de la Entidad Contacto"""
    def __init__(self,dni:int,nombre:str,apellido:str,segundoApellido:str,
        telefono:str,email:str,id_organizacion:int,cargo:str,segundoNombre:str=None):
        self.dni = dni
        self.nombre = nombre
        self.segundoNombre = segundoNombre
        self.apellido = apellido
        self.segundoApellido = segundoApellido
        self.telefono = telefono
        self.email = email
        self.id_organizacion = id_organizacion
        self.cargo = cargo

    def normalize(self):
        self.nombre = self.nombre.lower()
        self.segundoNombre = None if self.segundoNombre==None else self.segundoNombre.lower()
        self.apellido = self.apellido.lower()
        self.segundoApellido = self.segundoApellido.lower()
        self.email = self.email.lower()
        self.cargo = self.cargo.lower()
        
    def to_representation(self):
        self.nombre = self.nombre.capitalize()
        self.segundoNombre = '' if self.segundoNombre==None else self.segundoNombre.capitalize()
        self.apellido = self.apellido.capitalize()
        self.segundoApellido = self.segundoApellido.capitalize()
        self.cargo = self.cargo.capitalize()
    
    @classmethod
    def model(cls, **kwargs):
        if 'pais_nacio' in kwargs:
            kwargs['pais_nacio'] = Pais.model(**kwargs['pais_nacio'])
        if 'pais_reside' in kwargs:
            kwargs['pais_reside'] = Pais.model(**kwargs['pais_reside'])
        return cls(**kwargs)