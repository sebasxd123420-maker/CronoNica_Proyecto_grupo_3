import flet as ft
from datos import img as ruta_img

from entidades import Personaje
from funciones import lbl, M, T, P, A, ctr, Row, btn, borde, refrescar

# Colores de las pestañas
COLOR_TAB_ACTIVA = "#FFE57F"
COLOR_TAB_ACTIVA_TXT = "#062A2B"
COLOR_TAB = "#0E9A91"
COLOR_TAB_HOVER = "#1A7A74"
COLOR_TAB_TXT = "#FFFFFF"


# =====================================================================
# PANTALLA DE PERSONAJES
# =====================================================================
@ft.control
class PersonajesScreen(ft.Container):
    """Pestañas con los nombres de los personajes. Al elegir una se muestra su ficha
    (nombre al centro, imagen e información) con la misma distribución para todos."""

    @classmethod
    def crear(cls, controller):
        pantalla = cls()
        pantalla._controller = controller
        return pantalla

    def init(self):
        self.expand = True
        self.bgcolor = "#A8D8D4"
        self.border_radius = 6
        self._controller = None

        personajes = [
            Personaje(
                "sandino.png",
                "Augusto César Sandino",
                "Augusto César Sandino fue un líder revolucionario nicaragüense, símbolo de "
                "resistencia y defensor de la soberanía nacional frente a la intervención "
                "estadounidense, conocido como “El General de Hombres Libres”.",
                "#FF6B35",
            ),
            Personaje(
                "ruben.png",
                "Rubén Darío",
                "Rubén Darío es considerado el máximo exponente del modernismo literario en "
                "lengua española y uno de los poetas más influyentes de Latinoamérica.",
                "#FF6B35",
            ),
            Personaje(
                "blanca.png",
                "Blanca Araúz",
                "Blanca Aráuz (1909–1933) fue una telegrafista y revolucionaria nicaragüense, "
                "declarada oficialmente la primera Heroína Nacional de su país. Jugó un papel "
                "clave en la lucha contra la ocupación estadounidense organizando las "
                "comunicaciones del (EDSN) y apoyando las negociaciones de paz.",
                "#FF6B35",
            ),
            Personaje(
                "benjamin.png",
                "Benjamín Francisco Zeledón",
                "Benjamín Francisco Zeledón Rodríguez (1879-1912) fue un abogado, político, "
                "militar y patriota nicaragüense reconocido como Héroe Nacional por su defensa "
                "de la soberanía y su resistencia frente a la intervención estadounidense en 1912.",
                "#FF6B35",
            ),
        ]

        # ── Ficha: misma distribución para todos (nombre → imagen → información) ──
        def crear_ficha(pj):
            nombre = ft.Container(
                alignment=A(0, 0),
                content=T(pj.nombre, 26, True, "#FFE57F", justify="center"),
            )
            linea = ft.Container(width=120, height=4, bgcolor=pj.color, border_radius=2,
                                 margin=M(t=8, b=18))
            imagen = ft.Container(
                width=280, height=280, border_radius=16, bgcolor="#0A3A3B",
                border=borde(3, pj.color), clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=ft.Image(src=ruta_img(pj.imagen), width=280, height=280,
                                 fit=ft.BoxFit.CONTAIN),
            )
            info = ft.Container(
                width=680, bgcolor="#0A3A3B", border_radius=14,
                padding=P(l=22, t=16, r=22, b=18), margin=M(t=20),
                content=T(pj.descripcion, 14, False, "#FFFFFF", justify="center"),
            )
            return ft.Column(
                controls=[nombre, ctr(linea), ctr(imagen), ctr(info)],
                spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        tabs = []

        # ── Cambiar de personaje ──
        def seleccionar(indice):
            for i, tab in enumerate(tabs):
                if i == indice:
                    tab.configurar(fondo=COLOR_TAB_ACTIVA, color_texto=COLOR_TAB_ACTIVA_TXT,
                                   hover=None)
                else:
                    tab.configurar(fondo=COLOR_TAB, color_texto=COLOR_TAB_TXT,
                                   hover=COLOR_TAB_HOVER)
            self.ficha.content = crear_ficha(personajes[indice])
            refrescar(self)

        # ── Pestañas (una por personaje) ──
        for i, pj in enumerate(personajes):
            activa = (i == 0)
            tabs.append(btn(
                pj.nombre, lambda idx=i: seleccionar(idx),
                fg=COLOR_TAB_ACTIVA if activa else COLOR_TAB,
                hover=None if activa else COLOR_TAB_HOVER,
                color=COLOR_TAB_ACTIVA_TXT if activa else COLOR_TAB_TXT,
                size=13, bold=True, height=42, radius=10, width=230,
                margin=M(l=6, r=6, t=4, b=4),
            ))

        barra_tabs = ft.Container(
            bgcolor="#073233", border_radius=14, margin=M(l=20, r=20, b=14),
            padding=P(l=10, t=6, r=10, b=6),
            content=Row(tabs, alignment=ft.MainAxisAlignment.CENTER, wrap=True),
        )

        self.ficha = ft.Container(
            bgcolor="#073233", border_radius=18, margin=M(l=20, r=20),
            padding=P(l=30, t=26, r=30, b=30),
            content=crear_ficha(personajes[0]),
        )

        self.content = ft.Column(
            controls=[
                lbl("Personajes Destacados", 28, True, "#FFFFFF", height=None,
                    m=M(t=20, b=15)),
                barra_tabs,
                self.ficha,
                ctr(btn("Volver al inicio",
                        lambda: self._controller.show_frame("DashboardScreen"),
                        fg="#3B8ED0", hover="#36719F", width=140),
                    M(t=20, b=20)),
            ],
            spacing=0, scroll=ft.ScrollMode.AUTO, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )