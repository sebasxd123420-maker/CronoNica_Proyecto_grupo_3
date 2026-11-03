from dataclasses import dataclass

# =====================================================================
# DATOS: definición de un aro animado (antes tupla posicional)
# =====================================================================
@dataclass
class Aro:
    """Parámetros de un aro decorativo animado en péndulo en LoginScreen."""
    x_rel: float        # posición X relativa al ancho de la pantalla (0.0 - 1.0)
    y_rel: float        # posición Y relativa al alto de la pantalla (0.0 - 1.0)
    radio: int          # radio del círculo en píxeles
    color: str          # color del trazo (hex)
    grosor: int         # grosor del trazo en píxeles
    fase_inicial: float # fase inicial de la oscilación (radianes)
    velocidad: float    # incremento de fase por frame
    amplitud: float     # amplitud del desplazamiento pendular en Y (píxeles)

# =====================================================================
# DATOS: logros e insignias del panel (antes tuplas posicionales)
# =====================================================================
@dataclass
class LogroReciente:
    """Un logro con ícono y nombre, mostrado en la tarjeta 'Logros recientes'."""
    icono: str
    nombre: str
    color_icono: str
    color_fondo: str

@dataclass
class Insignia:
    """Una insignia hexagonal sin texto, mostrada en la fila de badges del perfil."""
    icono: str
    color_icono: str
    color_fondo: str

@dataclass
class OpcionQuiz:
    """Una alternativa de respuesta del quiz rápido (Dashboard)"""
    letra: str
    texto: str
    es_correcta: bool

# =====================================================================
# DATOS: ficha de personaje histórico (antes llamadas repetidas)
# =====================================================================
@dataclass
class Personaje:
    """Un personaje histórico destacado, mostrado como tarjeta en PersonajesScreen."""
    imagen: str
    nombre: str
    descripcion: str
    color: str

# =====================================================================
# DATOS: ficha de dato histórico / eventos / personajes clave
# =====================================================================
@dataclass
class DatoHistorico:
    """Un dato puntual mostrado en la ficha 'Datos históricos' de AventuraScreen."""
    icono: str
    etiqueta: str
    valor: str

@dataclass
class EventoHistorico:
    """Un punto en la línea de tiempo de AventuraScreen."""
    fecha: str
    icono: str
    descripcion: str
    destacado: bool
    color: str

@dataclass
class PersonajeClave:
    """Avatar compacto de un personaje histórico en la barra lateral de AventuraScreen."""
    iniciales: str
    color_fondo: str
    color_texto: str
    nombre: str
    rol: str