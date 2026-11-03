import flet as ft
from gui.Dashboard import DashboardScreen
from gui.Biblioteca import BibliotecaScreen
from gui.Ajustes import AjustesScreen
from gui.Aventura import AventuraScreen
from gui.Quiz import QuizPrecolombino
from gui.LoadingScreen import LoadingScreen
from gui.Login import LoginScreen
from gui.Personajes import PersonajesScreen
from datos import (
    COLOR_OSCURO, COLOR_TEAL, COLOR_FONDO, COLOR_SIDEBAR, COLOR_TEXTO, COLOR_AMARILLO,
)
from funciones import make_logo
from funciones import lbl, M, ctr, btn, borde, P, Col

# =====================================================================
# APLICACIÓN PRINCIPAL
# =====================================================================
class App:
    """Raíz de la app, maneja la navegación entre pantallas y el sidebar."""

    def __init__(self, page: ft.Page):
        self.page = page
        page.title = "Aventura Histórica de Nicaragua"
        page.window.width = 1360
        page.window.height = 880
        page.window.min_width = 1200
        page.window.min_height = 780
        page.padding = 0
        page.spacing = 0
        page.bgcolor = COLOR_OSCURO
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = ft.Theme(scrollbar_theme=ft.ScrollbarTheme(thumb_color="#0E9A91"))

        # Paleta de colores
        self.COLOR_FONDO = COLOR_FONDO
        self.COLOR_SIDEBAR = COLOR_SIDEBAR
        self.COLOR_OSCURO = COLOR_OSCURO
        self.COLOR_TEAL = COLOR_TEAL
        self.COLOR_MORADO = "#2D0A3D"
        self.COLOR_TEXTO_MENU = COLOR_TEXTO
        self.COLOR_AMARILLO = COLOR_AMARILLO

        self.frames = {}
        self.nav_buttons = {}

        self.root = ft.Container(expand=True, bgcolor=COLOR_OSCURO)

        # ── Flujo de pantallas: carga → login → carga → app ──────────
        self.loading_screen = LoadingScreen.crear(self._show_login)
        self.root.content = self.loading_screen
        page.add(self.root)

    def _mostrar(self, pantalla):
        """Reemplaza la pantalla visible."""
        self.root.content = pantalla
        self.root.update()

    def reiniciar_sesion(self):
        """Destruye la app principal y vuelve al login."""
        for frame in self.frames.values():
            if hasattr(frame, "_cancelar_cronometro"):
                frame._cancelar_cronometro()
        self.frames = {}
        self.nav_buttons = {}
        self.root.bgcolor = COLOR_OSCURO
        self._show_login()

    # ------------------------------------------------------------------
    def _show_login(self):
        self.login_screen = LoginScreen.crear(self._on_login_ok)
        self._mostrar(self.login_screen)

    def _on_login_ok(self):
        self.loading_screen = LoadingScreen.crear(self._launch_app)
        self._mostrar(self.loading_screen)

    def _launch_app(self):
        self.root.bgcolor = self.COLOR_FONDO
        self._build_main_ui()

    # ------------------------------------------------------------------
    def _build_main_ui(self):
        """Construye el layout principal (sidebar + contenido)."""
        self.nav_buttons = {}
        self.sidebar_frame = ft.Container(
            width=238, bgcolor=self.COLOR_SIDEBAR, content=self.init_sidebar())

        self.frames = {}
        for ScreenClass, key in [
            (DashboardScreen, "DashboardScreen"),
            (AventuraScreen, "Aventura"),
            (BibliotecaScreen, "Biblioteca"),
            (QuizPrecolombino, "QuizPrecolombino"),
            (AjustesScreen, "Ajustes"),
            (PersonajesScreen, "Personajes"),
        ]:
            self.frames[key] = ScreenClass.crear(self)

        # Aquí se coloca la pantalla activa
        self.main_container = ft.Container(expand=True, margin=20)

        self._mostrar(ft.Row(
            controls=[self.sidebar_frame, self.main_container],
            spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        ))
        self.show_frame("DashboardScreen")

    # ------------------------------------------------------------------
    def init_sidebar(self):
        items = [
            ctr(make_logo(62), M(t=22, b=4)),
            lbl("Prahaku", 13, True, self.COLOR_OSCURO, m=M(b=14)),
            ft.Container(height=1, bgcolor="#E0E0E0", margin=M(l=18, r=18, b=10)),
        ]

        buttons_data = [
            ("🏠  Inicio",     "DashboardScreen"),
            ("🗺️  Aventura",   "Aventura"),
            ("📚  Biblioteca", "Biblioteca"),
            ("👥  Personajes", "Personajes"),
            ("🏆  Logros",     "Logros"),
            ("🛒  Tienda",     "Tienda"),
            ("⚙️  Ajustes",    "Ajustes"),
            ("🏺  Quiz",       "QuizPrecolombino"),
        ]
        for text, screen_name in buttons_data:
            b = btn(
                text, lambda name=screen_name: self.show_frame(name),
                fg=None, hover="#E0F2F1", color=self.COLOR_TEXTO_MENU, size=13, bold=True,
                height=40, radius=10, anchor="w",
                margin=M(l=14, r=14, t=2, b=2), padding=P(l=12),
            )
            items.append(b)
            self.nav_buttons[screen_name] = b

        items.append(ft.Container(expand=True))

        items.append(ft.Container(
            bgcolor="#FFF3E0", border_radius=10, margin=M(l=14, r=14, b=8),
            content=Col([
                lbl("🔥  Racha: 7 días", 12, True, "#E65100", anchor="w", m=M(l=12, t=8, b=2)),
                lbl("¡Sigue así, explorador!", 10, color="#BF360C", anchor="w",
                    m=M(l=12, b=8)),
            ]),
        ))

        items.append(ft.Container(
            bgcolor="#F5F5F5", border_radius=12, border=borde(1, "#E0E0E0"),
            margin=M(l=14, r=14, b=18),
            content=Col([
                lbl("🇳🇮", 30, height=None, m=M(t=10, b=2)),
                lbl('"Conoce tu historia,\nentiende tu presente,\nconstruye tu futuro."\n'
                    '— Proverbio Nicaragüense',
                    9, color="#555555", italic=True, height=None, justify="center",
                    m=M(l=10, r=10, b=10)),
            ]),
        ))
        return Col(items)

    # ------------------------------------------------------------------
    def show_frame(self, page_name):
        if page_name not in self.frames:
            return

        # Detener el cronómetro del quiz si salimos de él
        for name, frame in self.frames.items():
            if name != page_name and hasattr(frame, "_cancelar_cronometro"):
                frame._cancelar_cronometro()

        # La pantalla elegida pasa a ser el único contenido visible
        frame = self.frames[page_name]
        frame.visible = True
        self.main_container.content = frame

        # Resaltar el botón activo del sidebar
        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configurar(fondo=self.COLOR_AMARILLO, color_texto="#062A2B")
            else:
                button.configurar(fondo=None, color_texto=self.COLOR_TEXTO_MENU)

        self.page.update()

        # on_show después de montar la pantalla (el Quiz arranca su cronómetro aquí)
        if hasattr(frame, "on_show"):
            frame.on_show()

