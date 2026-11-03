import flet as ft
from datos import img as ruta_img

# =====================================================================
# PANTALLA DE BIBLIOTECA
# =====================================================================
@ft.control
class BibliotecaScreen(ft.Container):
    """Pestaña Biblioteca (unicamente como ejemplificación): muestra Biblioteca.png ocupando todo el espacio de la pestaña."""

    @classmethod
    def crear(cls, controller):
        pantalla = cls()
        pantalla._controller = controller
        return pantalla

    def init(self):
        self.expand = True
        self._controller = None
        self.border_radius = 6
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE

        self.content = ft.Image(
            src=ruta_img("Biblioteca.png"),
            expand=True,
            fit=ft.BoxFit.FILL,
        )