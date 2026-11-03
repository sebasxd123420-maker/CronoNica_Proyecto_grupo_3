import flet as ft
import asyncio
import os
import flet as ft

from datos import (
    IMG_DIR, img as ruta_img,
    COLOR_OSCURO, COLOR_TEAL
)
from funciones import barra_progreso, lbl, msgbox, M, grad_barra, T, A
# =====================================================================
# PANTALLA DE CARGA (Loading Screen)
# =====================================================================
@ft.control
class LoadingScreen(ft.Container):
    """Pantalla de carga animada que aparece tras el login exitoso."""

    _STATUS_MSGS = [
        "Cargando mapas históricos...",
        "Preparando personajes...",
        "Cargando capítulos...",
        "Inicializando aventura...",
        "¡Listo para explorar!",
    ]

    @classmethod
    def crear(cls, callback_fin):
        pantalla = cls()
        pantalla._callback_fin = callback_fin
        return pantalla

    def init(self):
        self.expand = True
        self.bgcolor = COLOR_OSCURO
        self._callback_fin = None
        self._activo = True
        self._paso = 0
        self._fade_alpha = 1.0
        self._logo_ok = os.path.exists(os.path.join(IMG_DIR, "logo.png"))

        # Logo
        if self._logo_ok:
            logo = ft.Image(src=ruta_img("logo.png"), width=120, height=120,
                            fit=ft.BoxFit.FILL)
        else:
            logo = ft.Container(width=120, height=120, bgcolor=COLOR_TEAL, border_radius=8)

        # Barra de progreso + label de estado
        self.progress_bar = barra_progreso(0, 10, "#0A3A3B", COLOR_TEAL, 8, ancho=320)
        self.status_label = T("Cargando recursos...", 12, color="#80CBC4")

        # Contenedor central
        center = ft.Column(
            controls=[
                ft.Container(content=logo, margin=M(b=12)),
                lbl("Prahaku", 36, True, COLOR_TEAL, height=None),
                lbl("Aventura Histórica de Nicaragua", 14, color="#80CBC4", m=M(t=4, b=28)),
                ft.Container(content=self.progress_bar, margin=M(b=14)),
                ft.Container(content=self.status_label, height=28, alignment=A(0, 0)),
            ],
            spacing=0, tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Igual que el original, el "canvas" (fondo fijo #062A2B) tapa toda la pantalla.
        self.content = ft.Stack(
            controls=[
                ft.Container(left=0, top=0, right=0, bottom=0, bgcolor="#062A2B"),
                ft.Container(content=center, alignment=A(0, 0),
                             left=0, top=0, right=0, bottom=0),
                # Barra inferior de acento
                ft.Container(height=4, bgcolor=COLOR_TEAL, left=0, right=0, bottom=0),
            ],
            expand=True,
        )

    def did_mount(self):
        if not self._logo_ok:
            msgbox(self.page, "Error", "No se pudo abrir Imagenes/logo.png")
        self.page.run_task(self._secuencia)

    def will_unmount(self):
        self._activo = False

    async def _secuencia(self):
        # after(80, _fade_in) + after(100, _run_progress)
        await asyncio.sleep(0.18)
        total_steps = 50

        # _run_progress: incrementa la barra en pasos
        while self._activo and self._paso <= total_steps:
            pct = self._paso / total_steps
            self.progress_bar.gradient = grad_barra(pct, COLOR_TEAL, "#0A3A3B")
            msg_idx = min(int(pct * len(self._STATUS_MSGS)), len(self._STATUS_MSGS) - 1)
            self.status_label.value = self._STATUS_MSGS[msg_idx]
            self.update()
            self._paso += 1
            delay = 30 if self._paso < total_steps * 0.7 else 55
            await asyncio.sleep(delay / 1000)
        if not self._activo:
            return

        # Carga completa → esperar y hacer fade-out
        await asyncio.sleep(0.4)
        self._fade_alpha = 1.0
        while self._activo:
            self._fade_alpha -= 0.05
            if self._fade_alpha <= 0:
                break
            self.bgcolor = "#{:02x}{:02x}{:02x}".format(
                max(0, int(6 * self._fade_alpha)),
                max(0, int(42 * self._fade_alpha)),
                max(0, int(43 * self._fade_alpha)),
            )
            self.update()
            await asyncio.sleep(0.03)
        if not self._activo:
            return
        self.bgcolor = "#000000"
        self.update()
        await asyncio.sleep(0.06)
        if self._callback_fin:
            self._callback_fin()

