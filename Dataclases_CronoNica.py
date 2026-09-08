from dataclasses import dataclass

@dataclass
class usuario:
    nombre: str
    id: str
    progreso: str
    experiencia: str

@dataclass
class capitulo:
    id: str
    nombre: str
    descripcion: str
    progreso: str
    estado: bool

@dataclass
class logro:
    id: str
    nombre:str
    descripcion: str
    estado: bool

@dataclass
class quiz:
    id: str
    pregunta: str
    respuesta: str
    puntos: int

@dataclass
class personaje:
    id: str
    nombre: str
    descripcion: str
    capitulo: str 