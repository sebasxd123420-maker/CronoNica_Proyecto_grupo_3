import flet as ft
from funciones import px, interruptor, FONT, Boton
from funciones import msgbox, M, T,ctr, btn, borde, P, Row, Col


# =====================================================================
# AJUSTES
# =====================================================================
@ft.control
class AjustesScreen(ft.Container):
    
    @classmethod
    def crear(cls, controller):
        pantalla = cls()
        pantalla._controller = controller
        return pantalla

    def init(self):
        self.expand = True
        self.padding = P(l=30, t=20, r=30, b=20)       # frame.pack(padx=30, pady=20)
        self._controller = None
        self.modo_oscuro = False
        self.bg_actual = "#F5F5F5"
        self.fg_actual = "black"
        self._bg_ctrls = []     # controles cuyo fondo cambia con el modo
        self._fg_ctrls = []     # textos cuyo color cambia con el modo
        self._build_ui()

    def _cerrar_sesion(self):
        # destruye toda la app y la reinicia
        self._controller.reiniciar_sesion()

    # ──────────────────────────────────────────────
    def _cambiar_modo(self, estado):
        self.modo_oscuro = estado
        if estado:
            self.bg_actual = "#2D2D2D"
            self.fg_actual = "white"
        else:
            self.bg_actual = "#F5F5F5"
            self.fg_actual = "black"
        self.frame.bgcolor = self.bg_actual
        self._actualizar_colores(self.bg_actual, self.fg_actual)
        self.update()

    def _actualizar_colores(self, bg, fg):
        for c in self._bg_ctrls:
            if isinstance(c, Boton):
                c.configurar(fondo=bg, color_texto=fg)
            else:
                c.bgcolor = bg
        for t in self._fg_ctrls:
            t.color = fg

    # ──────────────────────────────────────────────
    def _texto(self, texto, size=px(9), bold=False, familia=None):
        
        t = T(texto, size, bold, self.fg_actual, familia=familia)
        c = ft.Container(content=t, bgcolor=self.bg_actual)
        self._bg_ctrls.append(c)
        self._fg_ctrls.append(t)
        return c

    def _linea(self, texto, size=px(9), bold=False, familia=None, m=None):
        """Label empaquetado con anchor="w"."""
        return ft.Container(margin=m, content=Row([self._texto(texto, size, bold, familia)]))

    def _slider(self, minimo, maximo, valor):
        s = ft.Slider(min=minimo, max=maximo, value=valor, divisions=maximo - minimo,
                      label="{value}", width=250)
        c = ft.Container(content=s, bgcolor="#F0F0F0")     #color de fondo
        self._bg_ctrls.append(c)
        return ft.Container(margin=M(t=5, b=5), content=Row([c]))

    def _fila(self, controles):
        return ft.Container(bgcolor="#F5F5F5", content=Row(
            controles, vertical_alignment=ft.CrossAxisAlignment.CENTER))

    def _boton_tk(self, texto, comando, fg, color, size, bold, **kw):
        b = btn(texto, comando, fg=fg, hover=None, color=color, size=size, bold=bold,
                familia=FONT, radius=2, border=borde(1, "#ADADAD"), **kw)
        self._bg_ctrls.append(b)
        return b

    # ──────────────────────────────────────────────
    def _build_ui(self):
        # Título
        titulo = ft.Container(bgcolor="#F8E56A", padding=P(l=10, t=5, r=10, b=5),
                              content=T("⚙ Ajustes", px(16), True, "black", familia=FONT))
        self._bg_ctrls.append(titulo)
        self._fg_ctrls.append(titulo.content)

        # Idioma (ttk.Combobox readonly, width=18)
        self.idioma = ft.Dropdown(
            value="Español", width=170,
            options=[ft.DropdownOption(key="Español"), ft.DropdownOption(key="Miskito")],
            on_select=self._seleccionar_idioma,
        )

        items = [
            ctr(titulo, M(t=10, b=10)),

            # Accesibilidad
            self._linea("Accesibilidad", px(13), True, FONT, m=M(t=15, b=5)),
            self._linea("Tamaño de fuente"),
            self._slider(8, 24, 12),
            self._fila([self._texto("Subtítulos", px(11), familia=FONT), interruptor(True)]),

            # Juego
            self._linea("Juego", px(13), True, FONT, m=M(t=20, b=5)),
            self._fila([self._texto("Respuestas de alta retroalimentación", px(11),
                                    familia=FONT), interruptor(True)]),

            # Personalización
            self._linea("Personalización", px(13), True, FONT, m=M(t=20, b=5)),
            ft.Container(margin=M(t=5, b=5), content=Row([self._boton_tk(
                "Editar perfil",
                lambda: msgbox(self.page, "Perfil", "Aquí se abriría la edición del perfil."),
                "#F0F0F0", "black", px(9), False, height=None,
                padding=P(l=10, t=3, r=10, b=3))])),
            self._linea("Volumen"),
            self._slider(0, 100, 50),
            self._fila([self._texto("Modo oscuro", px(11), familia=FONT),
                        interruptor(False, self._cambiar_modo)]),

            # Idioma
            self._linea("Idioma", px(11), False, FONT, m=M(t=20, b=5)),
            Row([self.idioma]),

            # Botón volver
            ctr(self._boton_tk(
                "Volver al inicio", lambda: self._controller.show_frame("DashboardScreen"),
                "#F8E56A", "black", px(11), True, width=170, height=30),
                M(t=40, b=40)),

            # Cerrar sesión
            ctr(self._boton_tk(
                "🔒 Cerrar Sesión", self._cerrar_sesion, "#C0392B", "white", px(11), True,
                width=170, height=30),
                M(t=10, b=40)),
        ]

        self.frame = ft.Container(
            expand=True, bgcolor=self.bg_actual,
            content=Col(items, scroll=ft.ScrollMode.AUTO, expand=True),
        )
        self.content = self.frame

    def _seleccionar_idioma(self, e):
        msgbox(self.page, "Idioma", f"Idioma seleccionado: {self.idioma.value}")

