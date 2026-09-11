import os
from dataclasses import dataclass, field
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "Imagenes")

# Credenciales de acceso
LOGIN_USUARIO   = "admin"
LOGIN_PASSWORD  = "12345"

# Paleta compartida
COLOR_FONDO    = "#D4EBE7"
COLOR_OSCURO   = "#062A2B"
COLOR_TEAL     = "#0E9A91"
COLOR_AMARILLO = "#FFE57F"
COLOR_SIDEBAR  = "#FFFFFF"
COLOR_TEXTO    = "#1A1A1A"

# Constantes de quiz

@dataclass
class Pregunta:
    """Representa una pregunta del quiz de historia precolombina."""
    pregunta: str
    opciones: List[str] = field(default_factory=list)
    correcta: int = 0


PREGUNTAS: List[Pregunta] = [
    Pregunta(
        pregunta="¿Cuál fue la cultura precolombina más importante\nque habitó el lago de Nicaragua (Cocibolca)?",
        opciones=["Los Chorotegas", "Los Aztecas", "Los Mayas"],
        correcta=0,
    ),
    Pregunta(
        pregunta="¿Cómo se llamaba el instrumento de cerámica\nusado por los Nicaraos para almacenar granos?",
        opciones=["Petate", "Tinaja", "Metate"],
        correcta=1,
    ),
    Pregunta(
        pregunta="¿Qué deidad principal adoraban los Chorotegas\nen la región del Pacífico de Nicaragua?",
        opciones=["Quetzalcóatl", "Mixcóatl", "Tláloc"],
        correcta=0,
    ),
    Pregunta(
        pregunta="¿De qué material eran fabricadas principalmente\nlas estatuas encontradas en la Isla Zapatera?",
        opciones=["Madera de cedro", "Basalto volcánico", "Barro cocido"],
        correcta=1,
    ),
    Pregunta(
        pregunta="¿Qué grupo indígena le dio el nombre\n'Nicaragua' a la región?",
        opciones=["Los Lencas", "Los Nicaraos", "Los Matagalpas"],
        correcta=1,
    ),
    Pregunta(
        pregunta="¿Cuál era el principal cultivo de subsistencia\nde los pueblos precolombinos de Nicaragua?",
        opciones=["La yuca", "El maíz", "El frijol negro"],
        correcta=1,
    ),
    Pregunta(
        pregunta="¿Dónde se encontraron los petroglifos más\nimportantes del período precolombino nicaragüense?",
        opciones=["Isla de Ometepe", "Cosigüina", "Las Segovias"],
        correcta=0,
    ),
]

TIEMPO_INICIAL = 50

COLOR_OPCION_BG    = "#3B1F00"
COLOR_OPCION_HOVER = "#5C3200"
COLOR_OPCION_BORDE = "#C8860A"
COLOR_TEXTO_OPC    = "#FFE4A0"
COLOR_TIMER_OK     = "#00C896"
COLOR_TIMER_WARN   = "#FF8C00"
COLOR_TIMER_DANGER = "#FF2222"
COLOR_CORRECTO     = "#1B7F00"
COLOR_INCORRECTO   = "#8B0000"
COLOR_TITULO       = "#FFD700"
COLOR_PANEL        = "#2D1500"
COLOR_PREGUNTA     = "#F5DEB3"