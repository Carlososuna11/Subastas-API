from apps.organizaciones.models import Organizacion
from apps.coleccionistas.models import Coleccionista
from apps.commons.models import *
import datetime


class Moneda_Artista:
    """Representacion en Objeto de la Entidad M_A"""
    def __init__(self,id_moneda:int,id_artista:int):
        self.id_moneda = id_moneda
        self.id_artista =id_artista
    
    def normalize(self):
        pass
    
    def to_representation(self):
        pass

    @classmethod
    def model(cls, **kwargs):
        return cls(**kwargs)

class Moneda:
    """Representacion en Objeto de la Entidad Moneda"""
    def __init__(self,nombre:str,denominacion:int,
    mintage:int,forma:str,metal:str,diametromm:int,canto:str,
    pesogr:int,ano:datetime.date,motivo:str,acunacion:str,
    anverso:str,reverso:str,id_pais_divisa:int,id_pais:int,
    id_divisa:int,pais:Pais=None,divisa:Divisa=None,artistas:list=[],imagen:str=None,id:int=None):
        self.id = id
        self.nombre = nombre
        self.denominacion = denominacion
        self.mintage = mintage
        self.forma = forma
        self.metal = metal
        self.diametromm = diametromm
        self.canto = canto
        self.pesogr = pesogr
        self.ano = ano.year
        self.motivo = motivo
        self.acunacion = acunacion
        self.anverso = anverso
        self.reverso = reverso
        self.id_pais_divisa = id_pais_divisa
        self.id_pais = id_pais
        self.id_divisa = id_divisa
        self.pais = pais
        self.divisa = divisa
        self.artistas = [artista for artista in artistas if artista.id!=None]
        self.imagen = imagen        

    def normalize(self):
        self.nombre = self.nombre.lower()
        self.forma =self.forma.lower()
        self.metal = self.metal.lower()
        self.canto =self.canto.lower()
        self.motivo =self.motivo.lower()
        self.acunacion =self.acunacion.lower()
        if self.pais:
            self.pais.normalize()
        if self.divisa:
            self.divisa.normalize()
        for artista in self.artistas:
            artista.normalize()
        
    def to_representation(self):
        self.nombre = self.nombre.capitalize()
        self.forma =self.forma.capitalize()
        self.metal = self.metal.capitalize()
        self.canto =self.canto.capitalize()
        self.motivo =self.motivo.capitalize()
        self.acunacion =self.acunacion.capitalize()
        if self.pais:
            self.pais.to_representation()
        if self.divisa:
            self.divisa.to_representation()
        for artista in self.artistas:
            artista.to_representation()
        self.imagen = 'media/img/default.png' if self.imagen==None else f"media/img/{self.imagen}"
        #preguntar josa

    @classmethod
    def model(cls, **kwargs):
        if 'pais' in kwargs:
            kwargs['pais'] = Pais.model(**kwargs['pais'])
        if 'divisa' in kwargs:
            kwargs['divisa'] = Divisa.model(**kwargs['divisa'])
        if 'artistas' in kwargs:
            artistas=[]
            for i in kwargs['artistas']:
                artistas.append(Artista(**i))
            kwargs['artistas'] = artistas
        return cls(**kwargs)

class Catalogo_Moneda_Tienda:
    """Representación en Objetos de la entidad Catalogo_Moneda_Tienda"""
    def __init__(self,id_moneda:int,nur:int=None,id_coleccionista:int=None,id_organizacion:int=None,
        moneda:Moneda=None,coleccionista:Coleccionista=None,organizacion:Organizacion=None):
        self.nur = nur
        self.id_moneda = id_moneda
        self.id_coleccionista = id_coleccionista
        self.id_organizacion = id_organizacion
        self.moneda = moneda
        self.coleccionista = coleccionista
        if coleccionista.dni ==None:
            self.coleccionista=None
        self.organizacion = organizacion
        if organizacion.id ==None:
            self.organizacion = None

    def normalize(self):
        if self.moneda:
            self.moneda.normalize()
        if self.coleccionista:
            self.coleccionista.normalize()
        if self.organizacion:
            self.organizacion.normalize()
    
    def to_representation(self):
        self.moneda.to_representation()
        if self.coleccionista:
            self.coleccionista.to_representation()
        if self.organizacion:
            self.organizacion.to_representation()

    @classmethod
    def model(cls, **kwargs):
        if kwargs.get('moneda',None):
            kwargs['moneda'] = Moneda.model(**kwargs['moneda'])
        if kwargs.get('coleccionista',None):
            kwargs['coleccionista'] = Coleccionista.model(**kwargs['coleccionista'])
        if kwargs.get('organizacion',None):
            kwargs['organizacion'] = Organizacion.model(**kwargs['organizacion'])
        return cls(**kwargs)    
