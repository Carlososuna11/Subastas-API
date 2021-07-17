from apps.monedas.models import Catalogo_Moneda_Tienda
from apps.pinturas.models import Pintura
import datetime
from apps.commons.models import *
from apps.coleccionistas.models import *
class Evento:
    """Representacion en Objeto de la Entidad Evento (Subasta)"""
    def __init__(self,inscripcionCliente:float,fecha:datetime.date,
        status:str,tipo:str,tipoPuja:str,duracionHoras:int,lugar:str=None,
        id_pais:int=None,pais:Pais=None,inscripcionClienteNuevo:float=None,planificadores:list=[],id:int=None):
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
        self.planificadores = [planificador for planificador in planificadores if planificador.id !=None]
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
        for i in self.planificadores:
            i.normalize()
    
    def to_representation(self):
        self.fecha = self.fecha.strftime("%d-%m-%Y")
        self.status = self.status.capitalize()
        self.tipo = self.tipo.capitalize()
        self.tipoPuja = self.tipoPuja.capitalize()
        if self.lugar:
            self.lugar = self.lugar.capitalize()
        if self.pais:
            self.pais.to_representation()
        for i in self.planificadores:
            i.to_representation()
    
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
        self.fechaIngresoCliente = self.fechaIngresoCliente.strftime("%d-%m-%Y")
        if self.pais:
            self.pais.to_representation()
        self.cliente.normalize()
        if self.evento:
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


class Planificador:
    """Representacion en Objeto de la Entidad Planificador"""
    def __init__(self,id_organizacion:int,id_evento:int):
        self.id_organizacion = id_organizacion
        self.id_evento = id_evento
    
    def normalize(self):
        pass
    
    def to_representation(self):
        pass

    @classmethod
    def model(cls, **kwargs):
        return cls(**kwargs)

class CostoEnvio:
    """Representación en Objeto de la Entidad CostoEnvio"""
    def __init__(self,id_evento:int,costoExtra:float,id_pais:int,id:int=None,pais:int=None):
        self.id_evento = id_evento
        self.costoExtra = costoExtra
        self.id_pais = id_pais
        self.id = id
        self.pais = pais

    def normalize(self):
        if self.pais:
            self.pais.normalize()
    
    def to_representation(self):
        self.pais.normalize()

    @classmethod
    def model(cls, **kwargs):
        if 'pais' in kwargs:
            kwargs['pais'] = Pais.model(**kwargs['pais'])
        return cls(**kwargs)

class Lista_Objeto:
    """Representacion en Objetos de la clase Lista_Objeto"""
    def __init__(self,id_evento:int,porcentajeGananciaMin:float,bid:int,ask:int,id:int=None,id_pintura:int=None,
                nur_moneda:int=None,id_moneda:int=None,precioAlcanzado:int=None,orden:int=None,duracionmin:int=None,
                razonNoVenta:str=None,pintura:Pintura=None,moneda:Catalogo_Moneda_Tienda=None,id_eventoParticipante:int=None,
                fechaIngresoParticipante:datetime.date=None,id_coleccionistaParticipante:int=None,id_organizacionParticipante:int=None,participante:Participante=None):
        self.id = id 
        self.id_evento = id_evento
        self.porcentajeGananciaMin= porcentajeGananciaMin
        self.bid = bid
        self.ask = ask
        self.id_pintura = id_pintura
        self.nur_moneda = nur_moneda
        self.id_moneda = id_moneda
        self.pintura = None if pintura==None or pintura.nur==None else pintura
        self.moneda = None if moneda==None or moneda.nur==None else moneda
        self.precioAlcanzado = precioAlcanzado
        self.orden = orden
        self.duracionmin = duracionmin
        self.razonNoVenta = razonNoVenta
        self.id_eventoParticipante = id_eventoParticipante
        self.fechaIngresoParticipante = fechaIngresoParticipante
        self.id_coleccionistaParticipante = id_coleccionistaParticipante
        self.participante =None if participante==None or participante.id_coleccionista_cliente == None else participante
        self.id_organizacionParticipante = id_organizacionParticipante
    def normalize(self):
        if self.razonNoVenta:
            self.razonNoVenta = self.razonNoVenta.lower()
        if self.participante:
            self.participante.normalize()
        if self.pintura:
            self.pintura.normalize()
        if self.moneda:
            self.moneda.normalize()
        
    def to_representation(self):
        if self.razonNoVenta:
            self.razonNoVenta = self.razonNoVenta.capitalize()
        if self.participante:
            self.participante.to_representation()
        if self.pintura:
            self.pintura.to_representation()
        if self.moneda:
            self.moneda.to_representation()

    @classmethod
    def model(cls, **kwargs):
        if 'moneda' in kwargs:
            kwargs['moneda'] = Catalogo_Moneda_Tienda.model(**kwargs['moneda'])
        if 'pintura' in kwargs:
            kwargs['pintura'] = Pintura.model(**kwargs['pintura'])
        if 'participante' in kwargs:
            kwargs['participante'] = Participante.model(**kwargs['participante'])
        return cls(**kwargs)