from dataclasses import dataclass

# se encuentra en el archivo Datos.py - linea 22
@dataclass
class Pregunta:
    """Representa una pregunta del quiz de historia precolombina."""
    pregunta: str
    opciones: List[str] = field(default_factory=list)
    correcta: int = 0

# se encuentra en el archivo Entidades.py - linea 146
@dataclass
class Aro:
    """Parámetros de un aro decorativo animado en péndulo en LoginScreen."""
    x_rel: float        # posición X relativa al ancho del canvas (0.0 - 1.0)
    y_rel: float        # posición Y relativa al alto del canvas (0.0 - 1.0)
    radio: int          # radio del círculo en píxeles
    color: str          # color del trazo (hex)
    grosor: int         # grosor del trazo en píxeles
    fase_inicial: float # fase inicial de la oscilación (radianes)
    velocidad: float    # incremento de fase por frame
    amplitud: float     # amplitud del desplazamiento pendular en Y (píxeles)

# archivo Entidades.py - linea 509
@dataclass
class LogroReciente:
    """Un logro con ícono y nombre, mostrado en la tarjeta 'Logros recientes'."""
    icono: str
    nombre: str
    color_icono: str
    color_fondo: str

# archivo Entiddaes.py - linea 518
@dataclass
class Insignia:
    """Una insignia hexagonal sin texto, mostrada en la fila de badges del perfil."""
    icono: str
    color_icono: str
    color_fondo: str

# archivo Entidades.py - linea 986
@dataclass
class Personaje:
    """Un personaje histórico destacado, mostrado como tarjeta en PersonajesScreen."""
    imagen: str
    nombre: str
    descripcion: str
    color: str

# archivo Entidades.py - linea 1107
@dataclass
class DatoHistorico:
    """Un dato puntual mostrado en la ficha 'Datos históricos' de AventuraScreen."""
    icono: str
    etiqueta: str
    valor: str

# archivo Entidades.py - linea 1115
@dataclass
class EventoHistorico:
    """Un punto en la línea de tiempo de AventuraScreen."""
    fecha: str
    icono: str
    descripcion: str
    destacado: bool
    color: str
    
# archivo Entidades.py - linea 1125
@dataclass
class PersonajeClave:
    """Avatar compacto de un personaje histórico en la barra lateral de AventuraScreen."""
    iniciales: str
    color_fondo: str
    color_texto: str
    nombre: str
    rol: str

# archivo Entidades.py - linea 1135
@dataclass
class OpcionQuiz:
    """Una alternativa de respuesta del quiz rápido (Dashboard) o del acto (Aventura)."""
    letra: str
    texto: str
    es_correcta: bool

