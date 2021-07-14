import datetime
from apps.commons.models import *
from apps.coleccionistas.models import *
class Evento:
    """Representacion en Objeto de la Entidad Evento (Subasta)"""
    def __init__(self,inscripcionCliente:float,fecha:datetime.date,
        status:str,tipo:str,tipoPuja:str,duracionHoras:int,lugar:str=None,
        id_pais:int=None,pais:Pais=None,inscripcionClienteNuevo:float=None,id:int=None):
        self.id = id
        self.inscripcionCliente = inscripcionCliente
        self.inscripcionClienteNuevo = inscripcionClienteNuevo
        self.fecha = fecha
        self.status = status
        self.tipo = tipo
        self.tipoPuja = tipoPuja
        self.duracionHoras = duracionHoras
        self.lugar = lugar
        self.id_pais=id_pais
        self.pais = pais
        if self.pais:
            self.pais = self.pais if self.pais.id != None else None

    def normalize(self):
        self.status = self.status.lower()
        self.tipo = self.tipo.lower()
        self.tipoPuja = self.tipoPuja.lower()
        if self.lugar:
            self.lugar = self.lugar.lower()
        if self.pais:
            self.pais.normalize()
    
    def to_representation(self):
        self.status = self.status.capitalize()
        self.tipo = self.tipo.capitalize()
        self.tipoPuja = self.tipoPuja.capitalize()
        if self.lugar:
            self.lugar = self.lugar.capitalize()
        if self.pais:
            self.pais.to_representation()
    
    @classmethod
    def model(cls, **kwargs):
        if 'pais' in kwargs:
            kwargs['pais'] = Pais.model(**kwargs['pais'])
        return cls(**kwargs)

class Participante:
    """Representación en Objeto de la entidad Participante(comprador)"""
    def __init__(self,id_evento:int,fechaIngresoCliente:datetime.date,
                id_coleccionista_cliente:int,id_organizacion_cliente:int,
                id_pais:int=None,evento:Evento=None,cliente:Cliente=None,pais:Pais=None):
        self.id_evento=id_evento
        self.fechaIngresoCliente = fechaIngresoCliente
        self.id_coleccionista_cliente = id_coleccionista_cliente
        self.id_organizacion_cliente = id_organizacion_cliente
        self.id_pais = id_pais
        self.pais = pais
        if self.pais:
            self.pais = None if self.pais.id == None else self.pais
        self.cliente = cliente
        self.evento = evento

    def normalize(self):
        if self.pais:
            self.pais.normalize()
        if self.cliente:
            self.cliente.normalize()
        if self.evento:
            self.evento.normalize()
    
    def to_representation(self):
        if self.pais:
            self.pais.to_representation()
        self.cliente.normalize()
        self.evento.normalize()

    @classmethod
    def model(cls, **kwargs):
        if 'pais' in kwargs:
            kwargs['pais'] = Pais.model(**kwargs['pais'])
        if 'cliente' in kwargs:
            kwargs['cliente'] = Cliente.model(**kwargs['cliente'])
        if 'evento' in kwargs:
            kwargs['evento'] = Evento.model(**kwargs['evento'])
        return cls(**kwargs)