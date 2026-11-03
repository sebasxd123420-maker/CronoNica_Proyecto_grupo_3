import flet as ft
import asyncio
import math
import os
import flet as ft

from datos import (
    IMG_DIR, img as ruta_img,
    COLOR_TEAL,
    LOGIN_USUARIO, LOGIN_PASSWORD
)

from entidades import Aro
from funciones import FONT, lbl, M,  A, ctr, btn, borde, P, despues, enfocar, refrescar, Col


# =====================================================================
# PANTALLA DE LOGIN
# =====================================================================
@ft.control
class LoginScreen(ft.Container):
    """Pantalla de login — fondo blanco con aros animados en péndulo."""

    # Definición de aros decorativos animados
    _AROS = [
        Aro(0.12, 0.28, 120, "#FFD700", 20, 0.00, 0.016, 18),
        Aro(0.08, 0.72, 80,  "#FFD700", 15, 1.20, 0.013, 14),
        Aro(0.88, 0.22, 100, "#0E9A91", 14, 0.80, 0.015, 16),
        Aro(0.92, 0.75, 130, "#0E9A91", 11, 2.00, 0.011, 12),
        Aro(0.50, 0.08, 65,  "#E05555", 15, 0.40, 0.019, 20),
        Aro(0.18, 0.90, 90,  "#E05555", 20, 1.60, 0.014, 15),
        Aro(0.80, 0.52, 70,  "#FFD700", 16, 3.00, 0.017, 13),
        Aro(0.55, 0.88, 55,  "#0E9A91", 12, 2.50, 0.018, 11),
        Aro(0.35, 0.05, 45,  "#E05555", 13, 0.90, 0.021, 16),
        Aro(0.70, 0.95, 60,  "#FFD700", 10, 1.80, 0.015, 14),
    ]

    @classmethod
    def crear(cls, on_login_success):
        pantalla = cls()
        pantalla._on_login_success = on_login_success
        return pantalla

    def init(self):
        self.expand = True
        self.bgcolor = "#FFFFFF"
        self._on_login_success = None
        self._fases = [aro.fase_inicial for aro in self._AROS]
        self._activo = True
        self._build_ui()

    def did_mount(self):
        self.page.run_task(self._animar)

    def will_unmount(self):
        self._activo = False

    # ------------------------------------------------------------------
    def _campo(self, hint, password=False, autofocus=False):
        return ft.TextField(
            value="", hint_text=hint,
            hint_style=ft.TextStyle(size=13, color="#AAAAAA", font_family=FONT),
            text_style=ft.TextStyle(size=13, color="#1A1A1A", font_family=FONT),
            bgcolor="#F7F7F7", filled=True,
            border_color="#DDDDDD", focused_border_color="#DDDDDD",
            border_width=2, border_radius=10, height=44,
            content_padding=P(l=12, t=12, r=12, b=12),
            password=password, autofocus=autofocus,
            on_submit=lambda e: self._try_login(),
        )

    def _build_ui(self):
        # ── Capa de aros (se dibujan aquí) ───────────────────
        self._aros_ctrl = []
        for aro in self._AROS:
            d = 2 * aro.radio + aro.grosor      # el trazo de tk se centra sobre el borde
            self._aros_ctrl.append(ft.Container(
                width=d, height=d, border_radius=d / 2,
                border=borde(aro.grosor, aro.color), left=0, top=0,
            ))
        self.canvas = ft.Stack(controls=self._aros_ctrl, left=0, top=0, right=0, bottom=0)

        # ── Panel central encima ──────────────────────────────
        if os.path.exists(os.path.join(IMG_DIR, "logo2.png")):
            logo = ft.Image(src=ruta_img("logo2.png"), width=200, height=130,
                            fit=ft.BoxFit.FILL)
        else:
            logo = ft.Container(width=200, height=130, bgcolor="#0E9A91")

        self.entry_user = self._campo("Ingresa tu usuario", autofocus=True)
        self.entry_pass = self._campo("Ingresa tu contraseña", password=True)
        self.error_label = lbl("", 11, color="#E05555", anchor="w", m=M(l=36, r=36, b=10))
        self.btn_login = btn(
            "Entrar", self._try_login, fg=COLOR_TEAL, hover="#0A7A73", size=14, bold=True,
            height=48, radius=12, margin=M(l=36, r=36, b=16),
        )

        panel = ft.Container(
            width=420, height=590, bgcolor="#680000", border_radius=24,
            border=borde(2, "#000000"),
            content=Col([
                ctr(logo, M(t=28, b=2)),
                lbl("Aventura Histórica de Nicaragua", 11, color="#999999", m=M(b=16)),
                # Separador
                ft.Container(height=1, bgcolor="#E8E8E8", margin=M(l=36, r=36, b=16)),
                # Campo usuario
                lbl("Usuario", 12, True, "#FFFFFF", anchor="w", m=M(l=36, r=36)),
                ft.Container(content=self.entry_user, margin=M(l=36, r=36, t=4, b=12)),
                # Campo contraseña
                lbl("Contraseña", 12, True, "#FFFFFF", anchor="w", m=M(l=36, r=36)),
                ft.Container(content=self.entry_pass, margin=M(l=36, r=36, t=4, b=6)),
                self.error_label,
                self.btn_login,
                lbl("usuario: admin   |   contraseña: 12345", 9, color="#BBBBBB"),
            ]),
        )

        self.content = ft.Stack(
            controls=[
                self.canvas,
                ft.Container(content=panel, alignment=A(0, 0),
                             left=0, top=0, right=0, bottom=0),
            ],
            expand=True,
        )

    # ------------------------------------------------------------------
    async def _animar(self):
        """Mueve los aros con movimiento pendular suave en bucle."""
        await asyncio.sleep(0.05)
        while self._activo:
            w = self.page.width or self.page.window.width or 0
            h = self.page.height or self.page.window.height or 0
            if w < 10 or h < 10:
                await asyncio.sleep(0.05)
                continue
            for i, aro in enumerate(self._AROS):
                self._fases[i] += aro.velocidad
                dy = math.sin(self._fases[i]) * aro.amplitud     # péndulo en Y
                cx = int(aro.x_rel * w)
                cy = int(aro.y_rel * h + dy)
                c = self._aros_ctrl[i]
                c.left = cx - aro.radio - aro.grosor / 2
                c.top = cy - aro.radio - aro.grosor / 2
            if not self._activo:
                return
            self.canvas.update()
            await asyncio.sleep(0.03)

    # ------------------------------------------------------------------
    def _try_login(self):
        user = (self.entry_user.value or "").strip()
        pwd = (self.entry_pass.value or "").strip()

        if user == LOGIN_USUARIO and pwd == LOGIN_PASSWORD:
            self.error_label.content.value = ""
            self.btn_login.configurar(texto="Verificando...", activo=False)
            self._activo = False
            self.update()
            despues(self.page, 300, self._on_login_success)
        else:
            self.error_label.content.value = "⚠  Usuario o contraseña incorrectos."
            self.entry_pass.value = ""
            self.update()
            self.page.run_task(enfocar, self.entry_pass)
            self._shake_entry()

    def _shake_entry(self):
        self.entry_pass.border_color = "#E05555"
        self.entry_pass.focused_border_color = "#E05555"
        self.entry_pass.update()
        despues(self.page, 400, self._restaurar_borde)

    def _restaurar_borde(self):
        self.entry_pass.border_color = "#DDDDDD"
        self.entry_pass.focused_border_color = "#DDDDDD"
        refrescar(self.entry_pass)
