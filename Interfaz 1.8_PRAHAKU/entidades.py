import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import math
import random
from tkinter import ttk, messagebox
import os
from dataclasses import dataclass
from datos import BASE_DIR,IMG_DIR, COLOR_OSCURO, COLOR_TEAL, COLOR_FONDO, COLOR_SIDEBAR, COLOR_TEXTO, COLOR_AMARILLO, LOGIN_USUARIO, LOGIN_PASSWORD, PREGUNTAS, Pregunta, TIEMPO_INICIAL, COLOR_OPCION_BG, COLOR_OPCION_HOVER, COLOR_OPCION_BORDE,COLOR_TEXTO_OPC,COLOR_TIMER_OK,COLOR_TIMER_WARN,COLOR_TIMER_DANGER,COLOR_CORRECTO,COLOR_INCORRECTO, COLOR_TITULO,COLOR_PANEL,COLOR_PREGUNTA
from funciones import make_hero_image, make_chapter_image, make_map_slot_image, make_hex_badge, make_avatar, make_user_avatar, make_quiz_deco, make_logo, make_historia_image, make_chapter_banner, make_login_bg 

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# =====================================================================
# PANTALLA DE CARGA (Loading Screen)
# =====================================================================
class LoadingScreen(ctk.CTkFrame):
    """Pantalla de carga animada que aparece tras el login exitoso."""

    def __init__(self, parent, on_done_callback):
        super().__init__(parent, fg_color=COLOR_OSCURO, corner_radius=0)
        self.on_done_callback = on_done_callback
        self._alpha = 0
        self._step  = 0
        self._dots  = 0

        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._build_ui()
        self.after(80, self._fade_in)

    def _build_ui(self):
        # Fondo degradado (canvas)
        self.canvas = tk.Canvas(self, bg="#062A2B", highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Contenedor central
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        try:
            logo_img = Image.open(os.path.join(IMG_DIR, "logo.png")).convert("RGBA")
        except  Exception as e:
            messagebox.showerror("Error", str(e))

        self.logo_ctk = ctk.CTkImage(
            light_image = logo_img,
            dark_image = logo_img,
            size = (120, 120)
            )
        
        ctk.CTkLabel(
            center,
            image = self.logo_ctk,
            text = ""
            ).pack(pady = (0, 12))
        
        # Título
        ctk.CTkLabel(
            center, text="Prahaku",
            font=("Arial", 36, "bold"), text_color=COLOR_TEAL
        ).pack()

        ctk.CTkLabel(
            center, text="Aventura Histórica de Nicaragua",
            font=("Arial", 14), text_color="#80CBC4"
        ).pack(pady=(4, 28))

        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(
            center, width=320, height=10,
            fg_color="#0A3A3B", progress_color=COLOR_TEAL,
            corner_radius=8
        )
        self.progress_bar.pack(pady=(0, 14))
        self.progress_bar.set(0)

        # Label de estado
        self.status_label = ctk.CTkLabel(
            center, text="Cargando recursos...",
            font=("Arial", 12), text_color="#80CBC4"
        )
        self.status_label.pack()

        # Barra inferior de acento
        bar = ctk.CTkFrame(self, fg_color=COLOR_TEAL, height=4, corner_radius=0)
        bar.place(relx=0, rely=1.0, anchor="sw", relwidth=1)

    # ------------------------------------------------------------------
    _STATUS_MSGS = [
        "Cargando mapas históricos...",
        "Preparando personajes...",
        "Cargando capítulos...",
        "Inicializando aventura...",
        "¡Listo para explorar!",
    ]

    def _fade_in(self):
        """Anima la entrada del frame y luego inicia la barra de progreso."""
        self.lift()
        self.after(100, self._run_progress)

    def _run_progress(self):
        """Incrementa la barra de progreso en pasos."""
        total_steps = 50
        if self._step <= total_steps:
            pct = self._step / total_steps
            self.progress_bar.set(pct)
            msg_idx = min(int(pct * len(self._STATUS_MSGS)), len(self._STATUS_MSGS) - 1)
            self.status_label.configure(text=self._STATUS_MSGS[msg_idx])
            self._step += 1
            delay = 30 if self._step < total_steps * 0.7 else 55
            self.after(delay, self._run_progress)
        else:
            # Carga completa → esperar un momento y hacer fade-out
            self.after(400, self._fade_out_start)

    def _fade_out_start(self):
        self._fade_alpha = 1.0
        self._do_fade_out()

    def _do_fade_out(self):
        """Simula desvanecido oscureciendo el canvas con un overlay."""
        self._fade_alpha -= 0.05
        if self._fade_alpha > 0:
            # Dibuja rectángulo semi-transparente encima usando canvas
            self.canvas.delete("overlay")
            alpha_int = int((1 - self._fade_alpha) * 255)
            hex_col = "#{:02x}{:02x}{:02x}".format(
                max(0, int(6 * self._fade_alpha)),
                max(0, int(42 * self._fade_alpha)),
                max(0, int(43 * self._fade_alpha)),
            )
            # Refrescar fondo del frame para simular fade
            self.configure(fg_color=hex_col)
            self.after(30, self._do_fade_out)
        else:
            self.configure(fg_color="#000000")
            self.after(60, self.on_done_callback)


# =====================================================================
# DATOS: definición de un aro animado (antes tupla posicional)
# =====================================================================
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


# =====================================================================
# PANTALLA DE LOGIN
# =====================================================================
class LoginScreen(ctk.CTkFrame):
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

    def __init__(self, parent, on_login_success):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        self.on_login_success = on_login_success
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._fases = [aro.fase_inicial for aro in self._AROS]
        self._running = True
        self._build_ui()
        self.after(50, self._animar)

    def destroy(self):
        self._running = False
        super().destroy()

    # ------------------------------------------------------------------
    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Canvas fondo blanco (aros se dibujan aquí) ───────
        self.canvas = tk.Canvas(self, bg="#FFFFFF", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # ── Panel central encima ──────────────────────────────
        panel = ctk.CTkFrame(
            self,
            fg_color="#680000",
            corner_radius=24,
            border_color="#000000",
            border_width=2,
            width=420,
            height=590,
        )
        panel.place(relx=0.5, rely=0.5, anchor="center")
        panel.pack_propagate(False)

        # Logo2
        try:
            logo_img = Image.open(os.path.join(IMG_DIR, "logo2.png")).convert("RGBA")
            logo_size = (200, 130)
        except Exception:
            logo_img = Image.new("RGBA", (200, 130), (14, 154, 145, 255))
            logo_size = (200, 130)
        self._logo_ctk = ctk.CTkImage(
            light_image=logo_img, dark_image=logo_img, size=logo_size)
        ctk.CTkLabel(panel, image=self._logo_ctk, text="",
                     fg_color="transparent").pack(pady=(28, 2))

        ctk.CTkLabel(
            panel, text="Aventura Histórica de Nicaragua",
            font=("Arial", 11), text_color="#999999",
            fg_color="transparent"
        ).pack(pady=(0, 16))

        # Separador
        ctk.CTkFrame(panel, fg_color="#E8E8E8", height=1,
                     corner_radius=0).pack(fill="x", padx=36, pady=(0, 16))

        # Campo usuario
        ctk.CTkLabel(panel, text="Usuario", font=("Arial", 12, "bold"),
                     text_color="#FFFFFF", anchor="w",
                     fg_color="transparent").pack(fill="x", padx=36)
        self.entry_user = ctk.CTkEntry(
            panel, placeholder_text="Ingresa tu usuario",
            font=("Arial", 13), fg_color="#F7F7F7",
            border_color="#DDDDDD", text_color="#1A1A1A",
            placeholder_text_color="#AAAAAA",
            height=44, corner_radius=10
        )
        self.entry_user.pack(fill="x", padx=36, pady=(4, 12))

        # Campo contraseña
        ctk.CTkLabel(panel, text="Contraseña", font=("Arial", 12, "bold"),
                     text_color="#FFFFFF", anchor="w",
                     fg_color="transparent").pack(fill="x", padx=36)
        self.entry_pass = ctk.CTkEntry(
            panel, placeholder_text="Ingresa tu contraseña",
            font=("Arial", 13), fg_color="#F7F7F7",
            border_color="#DDDDDD", text_color="#1A1A1A",
            placeholder_text_color="#AAAAAA",
            height=44, corner_radius=10, show="●"
        )
        self.entry_pass.pack(fill="x", padx=36, pady=(4, 6))

        # Label error
        self.error_label = ctk.CTkLabel(
            panel, text="", font=("Arial", 11),
            text_color="#E05555", anchor="w", fg_color="transparent"
        )
        self.error_label.pack(fill="x", padx=36, pady=(0, 10))

        # Botón ingresar
        self.btn_login = ctk.CTkButton(
            panel, text="Entrar",
            font=("Arial", 14, "bold"),
            fg_color=COLOR_TEAL, hover_color="#0A7A73",
            text_color="#FFFFFF", height=48, corner_radius=12,
            command=self._try_login
        )
        self.btn_login.pack(fill="x", padx=36, pady=(0, 16))

        ctk.CTkLabel(
            panel,
            text="usuario: admin   |   contraseña: 12345",
            font=("Arial", 9), text_color="#BBBBBB",
            fg_color="transparent", justify="center"
        ).pack()

        # Binds
        self.entry_pass.bind("<Return>", lambda e: self._try_login())
        self.entry_user.bind("<Return>", lambda e: self._try_login())
        self.after(150, self.entry_user.focus)

    # ------------------------------------------------------------------
    def _animar(self):
        """Dibuja los aros con movimiento pendular suave en bucle."""
        if not self._running:
            return
        try:
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
        except Exception:
            return
        if w < 10 or h < 10:
            self.after(50, self._animar)
            return

        self.canvas.delete("aro")

        for i, aro in enumerate(self._AROS):
            self._fases[i] += aro.velocidad
            # Desplazamiento pendular suave en Y
            dy = math.sin(self._fases[i]) * aro.amplitud
            cx = int(aro.x_rel * w)
            cy = int(aro.y_rel * h + dy)
            r  = aro.radio
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=aro.color, width=aro.grosor, fill="", tags="aro"
            )

        self.after(30, self._animar)

    # ------------------------------------------------------------------
    def _try_login(self):
        user = self.entry_user.get().strip()
        pwd  = self.entry_pass.get().strip()

        if user == LOGIN_USUARIO and pwd == LOGIN_PASSWORD:
            self.error_label.configure(text="")
            self.btn_login.configure(state="disabled", text="Verificando...")
            self._running = False
            self.after(300, self.on_login_success)
        else:
            self.error_label.configure(text="⚠  Usuario o contraseña incorrectos.")
            self.entry_pass.delete(0, "end")
            self.entry_pass.focus()
            self._shake_entry()

    def _shake_entry(self):
        self.entry_pass.configure(border_color="#E05555")
        self.after(400, lambda: self.entry_pass.configure(border_color="#DDDDDD"))


# =====================================================================
# APLICACIÓN PRINCIPAL
# =====================================================================
class App(ctk.CTk):
    def reiniciar_sesion(self):
        """Destruir todos los frames de la app principal"""
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}

        """OCultar sidebar y main container"""
        self.sidebar_frame.destroy()
        self.main_container.destroy()

        """Resetear grid"""
        self.configure(fg_color=COLOR_OSCURO)

        """Mostrar login de nuevo"""
        self._show_login()

    def __init__(self):
        super().__init__()

        self.title("Aventura Histórica de Nicaragua")
        self.geometry("1360x880")
        self.minsize(1200, 780)


        # Paleta de colores
        self.COLOR_FONDO           = COLOR_FONDO
        self.COLOR_SIDEBAR         = COLOR_SIDEBAR
        self.COLOR_OSCURO          = COLOR_OSCURO
        self.COLOR_TEAL            = COLOR_TEAL
        self.COLOR_MORADO          = "#2D0A3D"
        self.COLOR_TEXTO_MENU      = COLOR_TEXTO
        self.COLOR_AMARILLO        = COLOR_AMARILLO
        self.configure(fg_color=COLOR_OSCURO)

        # ── Flujo de pantallas: login → loading → app ──────────
        self.loading_screen = LoadingScreen(self, on_done_callback = self._show_login)
        self.loading_screen.after(80, self.loading_screen._fade_in)

    # ------------------------------------------------------------------
    def _show_login(self):
        """Muestra la pantalla de inicio de sesión."""
        self.login_screen = LoginScreen(self, on_login_success=self._on_login_ok)

    def _on_login_ok(self):
        """Callback tras login exitoso: oculta login y muestra carga."""
        self.login_screen.place_forget()
        self.loading_screen = LoadingScreen(self, on_done_callback=self._launch_app)

    def _launch_app(self):
        """Destruye la pantalla de carga y construye la interfaz principal."""
        self.loading_screen.place_forget()
        self.loading_screen.destroy()
        self.configure(fg_color=self.COLOR_FONDO)
        self._build_main_ui()

    # ------------------------------------------------------------------
    def _build_main_ui(self):
        """Construye el layout principal (sidebar + contenido)."""
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=self.COLOR_SIDEBAR,
                                          corner_radius=0, width=238)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        self.nav_buttons = {}
        self.init_sidebar()

        # Contenedor principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for ScreenClass, key in [
          (DashboardScreen, "DashboardScreen"),
         (AventuraScreen,  "Aventura"),
         (QuizPrecolombino, "QuizPrecolombino"),
          (AjustesScreen,    "Ajustes"),
          (PersonajesScreen, "Personajes")
        ]:
          f = ScreenClass(parent=self.main_container, controller=self)
          self.frames[key] = f

        self.show_frame("DashboardScreen")

    # ------------------------------------------------------------------
    def init_sidebar(self):
        logo_img = make_logo(62)
        logo_ctk = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(62, 62))
        ctk.CTkLabel(self.sidebar_frame, image=logo_ctk, text="").pack(pady=(22, 4))
        ctk.CTkLabel(self.sidebar_frame, text="Prahaku", font=("Arial", 13, "bold"),
                     text_color=self.COLOR_OSCURO).pack(pady=(0, 14))

        sep = ctk.CTkFrame(self.sidebar_frame, fg_color="#E0E0E0", height=1)
        sep.pack(fill="x", padx=18, pady=(0, 10))

        buttons_data = [
            ("🏠  Inicio",        "DashboardScreen"),
            ("🗺️  Aventura",      "Aventura"),
            ("📚  Biblioteca",    "Biblioteca"),
            ("👥  Personajes",    "Personajes"),
            ("🏆  Logros",        "Logros"),
            ("🛒  Tienda",        "Tienda"),
            ("⚙️  Ajustes",       "Ajustes"),
            ("🏺  Quiz", "QuizPrecolombino"),
        ]

        for text, screen_name in buttons_data:
            btn = ctk.CTkButton(
                self.sidebar_frame, text=text, font=("Arial", 13, "bold"),
                fg_color="transparent", text_color=self.COLOR_TEXTO_MENU,
                hover_color="#E0F2F1", corner_radius=10, height=40, anchor="w",
                command=lambda name=screen_name: self.show_frame(name)
            )
            btn.pack(fill="x", padx=14, pady=2)
            self.nav_buttons[screen_name] = btn

        ctk.CTkFrame(self.sidebar_frame, fg_color="transparent").pack(fill="both", expand=True)

        racha_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#FFF3E0", corner_radius=10)
        racha_frame.pack(fill="x", padx=14, pady=(0, 8))
        ctk.CTkLabel(racha_frame, text="🔥  Racha: 7 días", font=("Arial", 12, "bold"),
                     text_color="#E65100").pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(racha_frame, text="¡Sigue así, explorador!", font=("Arial", 10),
                     text_color="#BF360C").pack(anchor="w", padx=12, pady=(0, 8))

        card = ctk.CTkFrame(self.sidebar_frame, fg_color="#F5F5F5", corner_radius=12,
                            border_color="#E0E0E0", border_width=1)
        card.pack(fill="x", padx=14, pady=(0, 18))
        ctk.CTkLabel(card, text="🇳🇮", font=("Arial", 30)).pack(pady=(10, 2))
        ctk.CTkLabel(card,
                     text='"Conoce tu historia,\nentiende tu presente,\nconstruye tu futuro."\n— Proverbio Nicaragüense',
                     font=("Arial", 9, "italic"), text_color="#555555",
                     justify="center").pack(pady=(0, 10), padx=10)

    # ------------------------------------------------------------------
    def show_frame(self, page_name):
        if page_name in self.frames:
         for name, frame in self.frames.items():
            if name == page_name:
                frame.grid(row=0, column=0, sticky="nsew")
                frame.tkraise()
                if hasattr(frame, "on_show"):
                    frame.on_show()
            else:
                if hasattr(frame, "_cancelar_cronometro"):
                    frame._cancelar_cronometro()
                frame.grid_remove()
         for name, button in self.nav_buttons.items():
          if name == page_name:
            button.configure(fg_color=self.COLOR_AMARILLO, text_color="#062A2B")
          else:
            button.configure(fg_color="transparent", text_color=self.COLOR_TEXTO_MENU)


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


# =====================================================================
# DASHBOARD PRINCIPAL
# =====================================================================
class DashboardScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent", scrollbar_button_color="#0E9A91")
        self.controller = controller
        self.grid_columnconfigure(0, weight=7)
        self.grid_columnconfigure(1, weight=3)

        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        left.grid_columnconfigure(0, weight=1)

        self._build_banner(left)
        self._build_chapter(left)
        self._build_map(left)
        self._build_bottom(left)

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        self._build_profile(right)
        self._build_quiz(right)

    # ──────────────────────────────────────────────────────
    def _build_banner(self, parent):
        banner = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=18, width = 900, height=205)
        banner.grid(row=0, column=0, sticky="nsew", pady=(0, 14))
        banner.grid_propagate(False)
        banner.grid_columnconfigure(0, weight=1)

         # Imagen ilustrativa
        hero_img = Image.open(os.path.join(IMG_DIR, "banner.png")).convert("RGBA")
        hero_img = hero_img.resize((900, 205))

        #Overlay de sombreado para mejorar legibilidad del texto
        overlay = Image.new("RGBA", hero_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for x in range (hero_img.width):
            alpha = int(220 * max(0, 1 - (x / (hero_img.width * 0.5 ))))
            draw.line(
                [(x, 0), (x, hero_img.height)],
                fill = (6, 42, 43, alpha))
        
        hero_img = Image.alpha_composite(hero_img, overlay)
        hero_img = hero_img.convert("RGB")

       
        # Texto lado izquierdo
        draw2 = ImageDraw.Draw(hero_img)

        try:
            font_titulo = ImageFont.truetype("arialbd.ttf", 24)
            font_sub = ImageFont.truetype("arial.ttf", 14)
        except:
            try:
                font_titulo = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
                font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
            except:
                font_titulo = ImageFont.load_default()
                font_sub = ImageFont.load_default()

        draw2.text((160, 22), "¡Bienvenido de nuevo", font = font_titulo, fill = "#FFFFFF")
        draw2.text((160, 50), "Explorador!, ¡HOLA!", font = font_titulo, fill = "#FFFFFF")
        draw2.text((160, 75), "Continua tu aventura", font = font_sub, fill = "#FFFFFF")
        draw2.text((160, 93), "Por la historia de Nicaragua", font = font_sub, fill = "#FFFFFF")
        draw2.text((160, 111), "¡Hoy es un gran día para aprender!", font = font_sub, fill = "#FFFFFF")

         #ctk de la imagen anterior despues del overlay
        self.hero_ctk = ctk.CTkImage(light_image = hero_img, dark_image = hero_img, size = (900, 205))

        bg_label = ctk.CTkLabel(banner, image = self.hero_ctk, text = "")
        bg_label.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)


        #Solo los botones queda como widgets de CTk normales encima del banner
        btn_row = ctk.CTkFrame(banner, fg_color="transparent", bg_color="transparent")
        btn_row.place(x=26, y=155)
        ctk.CTkButton(
            btn_row, text="▶  Continuar aventura",
            font=("Arial", 11, "bold"), fg_color="#0E9A91",
            hover_color="#0A7A73", text_color="#FFFFFF",
            corner_radius=10, height=38,
            command=lambda: self.controller.show_frame("Aventura")
        ).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            btn_row, text="📖  Ver biblioteca",
            font=("Arial", 12, "bold"), fg_color="#1A5E5A",
            hover_color="#1E7A74", text_color="#FFFFFF",
            corner_radius=10, height=38
        ).pack(side="left")

        ctk.CTkButton(
            btn_row, text="🏺  Comenzar Quiz",
            font=("Arial", 11, "bold"), fg_color="#FF9500",
            hover_color="#CC7700", text_color="#FFFFFF",
            corner_radius=10, height=38,
            command=lambda: self.controller.show_frame("QuizPrecolombino")
        ).pack(side="left", padx=(10, 0))

       

    # ──────────────────────────────────────────────────────
    def _build_chapter(self, parent):
        card = ctk.CTkFrame(parent, fg_color="#1E1E2E", corner_radius=16)
        card.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
        card.grid_columnconfigure(1, weight=1)

        # Imagen del capítulo
        ch_img = Image.open(os.path.join(IMG_DIR, "cap3.png")).convert("RGBA")
        ch_ctk = ctk.CTkImage(light_image=ch_img, dark_image=ch_img, size=(110, 90))
        ctk.CTkLabel(card, image=ch_ctk, text="").grid(row=0, column=0, padx=16, pady=14, rowspan=3)

        # Chips de info
        chips_frame = ctk.CTkFrame(card, fg_color="transparent")
        chips_frame.grid(row=0, column=1, sticky="w", padx=(0, 16), pady=(14, 2))

        for chip_text, chip_color in [("📖 Capítulo 3", "#0E9A91"), ("⚔️ Independencia", "#4A1525"), ("★ 4.8", "#7A6A1A")]:
            chip = ctk.CTkFrame(chips_frame, fg_color=chip_color, corner_radius=8)
            chip.pack(side="left", padx=(0, 6))
            ctk.CTkLabel(chip, text=chip_text, font=("Arial", 10, "bold"),
                         text_color="#FFFFFF").pack(padx=8, pady=3)

        ctk.CTkLabel(
            card,
            text="La Independencia de Centroamérica (1821)",
            font=("Arial", 15, "bold"), text_color="#FFFFFF", anchor="w"
        ).grid(row=1, column=1, sticky="w", padx=(0, 16))

        ctk.CTkLabel(
            card,
            text="Explora los eventos que llevaron a la independencia de\nCentroamérica del Imperio Español.",
            font=("Arial", 11), text_color="#8A9BB0", anchor="w", justify="left"
        ).grid(row=2, column=1, sticky="w", padx=(0, 16), pady=(0, 14))

        # Barra de progreso del capítulo
        prog_frame = ctk.CTkFrame(card, fg_color="transparent")
        prog_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))
        prog_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(prog_frame, text="Progreso:", font=("Arial", 11, "bold"),
                     text_color="#8A9BB0").grid(row=0, column=0, padx=(0, 10))
        bar = ctk.CTkProgressBar(prog_frame, height=10, corner_radius=6,
                                 fg_color="#2A2A3E", progress_color="#0E9A91")
        bar.grid(row=0, column=1, sticky="ew")
        bar.set(0.42)
        ctk.CTkLabel(prog_frame, text="42%", font=("Arial", 11, "bold"),
                     text_color="#0E9A91").grid(row=0, column=2, padx=(10, 0))

    # ──────────────────────────────────────────────────────
    def _build_map(self, parent):
        """Mapa de viaje de capítulos."""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.grid(row=2, column=0, sticky="nsew", pady=(0, 14))
        section.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(section, text="🗺️  Mapa de Aventura",
                     font=("Arial", 16, "bold"), text_color="#1A1A1A").grid(
            row=0, column=0, sticky="w", pady=(0, 8))

        map_frame = ctk.CTkFrame(section, fg_color="#0A2223", corner_radius=16)
        map_frame.grid(row=1, column=0, sticky="nsew")
        map_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        chapters = [
            (1, "🌿 Precolombino",    "Civilizaciones\noriginarias",    False, False),
            (2, "⛪ Colonial",         "El período\nespañol",            False, False),
            (3, "⚔️ Independencia",   "La firma del\nActa de 1821",     True,  False),
            (4, "🏛️ República",       "Los primeros\naños libres",      False, True),
            (5, "🔫 Revolución",      "El siglo XX\nnicaragüense",      False, True),
            (6, "🏙️ Modernidad",     "Nicaragua\nhoy",                  False, True),
        ]

        for col, (ch_num, title, subtitle, current, locked) in enumerate(chapters):
            slot_img = make_map_slot_image(95, 85, chapter_num=ch_num, locked=locked)
            slot_ctk = ctk.CTkImage(light_image=slot_img, dark_image=slot_img, size=(95, 85))

            slot = ctk.CTkFrame(
                map_frame,
                fg_color="#1A4A4B" if current else ("#0A2223" if locked else "#102E2F"),
                corner_radius=12,
                border_color="#0E9A91" if current else ("#0A2223" if locked else "#1A4A4B"),
                border_width=2 if current else 1
            )
            slot.grid(row=0, column=col, padx=8, pady=12, sticky="nsew")

            ctk.CTkLabel(slot, image=slot_ctk, text="").pack(pady=(10, 4))
            ctk.CTkLabel(slot, text=title, font=("Arial", 10, "bold"),
                         text_color="#FFFFFF" if not locked else "#546E7A").pack()
            ctk.CTkLabel(slot, text=subtitle, font=("Arial", 8),
                         text_color="#80CBC4" if not locked else "#37474F",
                         justify="center").pack(pady=(2, 8))

            if locked:
                ctk.CTkLabel(slot, text="🔒", font=("Arial", 14),
                             text_color="#546E7A").pack(pady=(0, 8))
            elif current:
                ctk.CTkButton(slot, text="▶ Continuar", font=("Arial", 9, "bold"),
                              fg_color="#0E9A91", hover_color="#0A7A73",
                              text_color="#FFFFFF", corner_radius=8, height=26,
                              command=lambda: self.controller.show_frame("Aventura")
                              ).pack(pady=(0, 10), padx=8, fill="x")

    # ──────────────────────────────────────────────────────
    def _build_bottom(self, parent):
        """Fila de cards: Estadísticas, Historia del día, Logros recientes."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.grid(row=3, column=0, sticky="nsew")
        row.grid_columnconfigure((0, 1, 2), weight=1)

        # ── Stats ──
        stats_card = ctk.CTkFrame(row, fg_color="#062A2B", corner_radius=14)
        stats_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(stats_card, text="📊 Estadísticas",
                     font=("Arial", 13, "bold"), text_color="#0E9A91").pack(anchor="w", padx=14, pady=(12, 6))

        stats = [("🏅 XP Total", "2 450"), ("🔥 Racha", "7 días"),
                 ("✅ Capítulos", "2 / 6"), ("⭐ Estrellas", "14 / 30")]
        for label, val in stats:
            r = ctk.CTkFrame(stats_card, fg_color="transparent")
            r.pack(fill="x", padx=14, pady=2)
            ctk.CTkLabel(r, text=label, font=("Arial", 11), text_color="#80CBC4").pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Arial", 11, "bold"), text_color="#FFFFFF").pack(side="right")
        ctk.CTkFrame(stats_card, fg_color="transparent", height=10).pack()

        # ── Historia del día ──
        hist_card = ctk.CTkFrame(row, fg_color="#1A0A20", corner_radius=14)
        hist_card.grid(row=0, column=1, padx=5, sticky="nsew")

        hist_img = make_historia_image(310, 220)
        hist_ctk = ctk.CTkImage(light_image=hist_img, dark_image=hist_img, size=(290, 130))
        ctk.CTkLabel(hist_card, image=hist_ctk, text="").pack(padx=10, pady=(10, 6))

        ctk.CTkLabel(hist_card, text="📜 Historia del día",
                     font=("Arial", 13, "bold"), text_color="#FFD700").pack(anchor="w", padx=14)
        ctk.CTkLabel(hist_card,
                     text="La firma del Acta de Independencia\nCentroamericana, 15 Sep 1821.",
                     font=("Arial", 10), text_color="#D4B8A0",
                     justify="left").pack(anchor="w", padx=14, pady=(4, 0))
        ctk.CTkButton(hist_card, text="Leer más →",
                      font=("Arial", 10, "bold"), fg_color="#4A1525",
                      hover_color="#6A1535", text_color="#FFD700",
                      corner_radius=8, height=30).pack(anchor="w", padx=14, pady=(8, 12))

        # ── Logros recientes ──
        logros_card = ctk.CTkFrame(row, fg_color="#1A2030", corner_radius=14)
        logros_card.grid(row=0, column=2, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(logros_card, text="🏆 Logros recientes",
                     font=("Arial", 13, "bold"), text_color="#FFE57F").pack(anchor="w", padx=14, pady=(12, 6))

        logros = [
            LogroReciente("🥇", "Primer capítulo",  "#FFD700", "#A37500"),
            LogroReciente("📖", "Lector ávido",     "#0E9A91", "#1B9A9C"),
            LogroReciente("⭐", "Racha de 7 días",  "#FF9500", "#985503"),
        ]
        for logro in logros:
            r = ctk.CTkFrame(logros_card, fg_color=logro.color_fondo, corner_radius=10)
            r.pack(fill="x", padx=14, pady=4)
            ctk.CTkLabel(r, text=logro.icono, font=("Arial", 20)).pack(side="left", padx=(10, 8), pady=8)
            ctk.CTkLabel(r, text=logro.nombre, font=("Arial", 11, "bold"),
                         text_color="#FFFFFF").pack(side="left", pady=8)
        ctk.CTkFrame(logros_card, fg_color="transparent", height=10).pack()

    # ──────────────────────────────────────────────────────
    def _build_profile(self, parent):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF",
                            corner_radius=16, border_color="#E0E0E0", border_width=1)
        card.grid(row=0, column=0, sticky="nsew", pady=(0, 14))

        # Avatar
        av_img = make_user_avatar(68)
        av_ctk = ctk.CTkImage(light_image=av_img, dark_image=av_img, size=(68, 68))
        ctk.CTkLabel(card, image=av_ctk, text="").pack(pady=(16, 4))

        ctk.CTkLabel(card, text="Ana García", font=("Arial", 15, "bold"),
                     text_color="#1A1A1A").pack()
        ctk.CTkLabel(card, text="Exploradora Nivel 5", font=("Arial", 11),
                     text_color="#0E9A91").pack(pady=(2, 10))

        # Barra de nivel
        xp_frame = ctk.CTkFrame(card, fg_color="transparent")
        xp_frame.pack(fill="x", padx=18, pady=(0, 4))
        ctk.CTkLabel(xp_frame, text="Nivel 5", font=("Arial", 10, "bold"),
                     text_color="#1A1A1A").pack(side="left")
        ctk.CTkLabel(xp_frame, text="2 450 / 3 000 XP", font=("Arial", 10),
                     text_color="#888888").pack(side="right")

        xp_bar = ctk.CTkProgressBar(card, height=8, corner_radius=6,
                                    fg_color="#E0E0E0", progress_color="#0E9A91")
        xp_bar.pack(fill="x", padx=18, pady=(0, 14))
        xp_bar.set(0.82)

        # Badges
        badges_frame = ctk.CTkFrame(card, fg_color="transparent")
        badges_frame.pack(pady=(0, 12))

        badge_data = [
            Insignia("🏅", "#FFD700", "#896304"),
            Insignia("⭐", "#0E9A91", "#188688"),
            Insignia("🔥", "#FF6B35", "#873F03"),
            Insignia("📖", "#6B3AC0", "#5622A3"),
        ]
        for insignia in badge_data:
            hex_img = make_hex_badge(insignia.icono, insignia.color_fondo, 48)
            hex_ctk = ctk.CTkImage(light_image=hex_img, dark_image=hex_img, size=(48, 48))
            b = ctk.CTkFrame(badges_frame, fg_color=insignia.color_fondo, corner_radius=10, width=48, height=48)
            b.pack(side="left", padx=4)
            b.pack_propagate(False)
            ctk.CTkLabel(b, text=insignia.icono, font=("Arial", 20)).place(relx=0.5, rely=0.5, anchor="center")

    # ──────────────────────────────────────────────────────
    def _build_quiz(self, parent):
        """Widget del quiz diario."""
        self.quiz_card = ctk.CTkFrame(parent, fg_color="#2D1040", corner_radius=16)
        self.quiz_card.grid(row=1, column=0, sticky="nsew")
        self.selected_answer = tk.StringVar(value="")
        self.answered = False

        # Decoración
        quiz_deco = make_quiz_deco(80, 80)
        deco_ctk  = ctk.CTkImage(light_image=quiz_deco, dark_image=quiz_deco, size=(80, 80))

        # Header del quiz
        qhdr = ctk.CTkFrame(self.quiz_card, fg_color="#3D1A58", corner_radius=12)
        qhdr.pack(fill="x", padx=16, pady=(14, 8))
        qhdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(qhdr, image=deco_ctk, text="").grid(row=0, column=0, padx=10, pady=6)
        title_col = ctk.CTkFrame(qhdr, fg_color="transparent")
        title_col.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(title_col, text="❓  Quiz \ndel día",
                     font=("Arial", 10, "bold"), text_color="#FFE57F").pack(anchor="w")
        ctk.CTkLabel(title_col, text="Responde y gana XP",
                     font=("Arial", 10), text_color="#B39DDB").pack(anchor="w")

        xp_chip = ctk.CTkFrame(qhdr, fg_color="#7A6A1A", corner_radius=8)
        xp_chip.grid(row=0, column=2, padx=12)
        ctk.CTkLabel(xp_chip, text="⭐ +50 XP",
                     font=("Arial", 10, "bold"), text_color="#FFE57F").pack(padx=8, pady=4)

        # Pregunta
        ctk.CTkLabel(
            self.quiz_card,
            text="¿Cuándo ocurrió la \n independencia de Centroamérica?",
            font=("Arial", 12, "bold"), text_color="#FFFFFF", justify="left"
        ).pack(anchor="w", padx=20, pady=(14, 10))

        # Opciones
        self.option_buttons = {}
        opciones = [
            OpcionQuiz("A", "1821", True),
            OpcionQuiz("B", "1990", False),
            OpcionQuiz("C", "1512", False),
            OpcionQuiz("D", "1856", False),
        ]
        opts_frame = ctk.CTkFrame(self.quiz_card, fg_color="transparent")
        opts_frame.pack(fill="x", padx=16, pady=(0, 16))
        opts_frame.grid_columnconfigure((0, 1), weight=1)

        for i, opcion in enumerate(opciones):
            row_i = i // 2
            col_i = i % 2
            btn_frame = ctk.CTkFrame(opts_frame, fg_color="#4A1525", corner_radius=12,
                                     border_color="#6A1535", border_width=1)
            btn_frame.grid(row=row_i, column=col_i, padx=6, pady=6, sticky="nsew")

            inner = ctk.CTkFrame(btn_frame, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=12, pady=10)

            letter_badge = ctk.CTkFrame(inner, fg_color="#6A1535", corner_radius=8,
                                        width=30, height=30)
            letter_badge.pack(side="left", padx=(0, 10))
            letter_badge.pack_propagate(False)
            ctk.CTkLabel(letter_badge, text=opcion.letra, font=("Arial", 12, "bold"),
                         text_color="#FFFFFF").place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(inner, text=opcion.texto, font=("Arial", 13, "bold"),
                         text_color="#FFFFFF").pack(side="left")

            self.option_buttons[opcion.letra] = (btn_frame, letter_badge, opcion)

            btn_frame.bind("<Button-1>", lambda e, l=opcion.letra: self._select_answer(l))
            inner.bind("<Button-1>", lambda e, l=opcion.letra: self._select_answer(l))
            for child in inner.winfo_children():
                child.bind("<Button-1>", lambda e, l=opcion.letra: self._select_answer(l))

        # Botón confirmar
        self.confirm_btn = ctk.CTkButton(
            self.quiz_card, text="Confirmar respuesta",
            font=("Arial", 13, "bold"), fg_color="#0E9A91",
            text_color="#FFFFFF", hover_color="#0A7A73",
            corner_radius=10, height=40, state="disabled",
            command=self._confirm_answer
        )
        self.confirm_btn.pack(fill="x", padx=16, pady=(0, 8))

        self.feedback_frame = ctk.CTkFrame(self.quiz_card, fg_color="transparent")
        self.feedback_frame.pack(fill="x", padx=16, pady=(0, 12))

    def _select_answer(self, letter):
        if self.answered:
            return
        self.selected_answer.set(letter)
        for l, (frame, badge, opcion) in self.option_buttons.items():
            if l == letter:
                frame.configure(fg_color="#1A5A55", border_color="#0E9A91")
                badge.configure(fg_color="#0E9A91")
            else:
                frame.configure(fg_color="#4A1525", border_color="#6A1535")
                badge.configure(fg_color="#6A1535")
        self.confirm_btn.configure(state="normal")

    def _confirm_answer(self):
        if self.answered:
            return
        self.answered = True
        chosen = self.selected_answer.get()
        self.confirm_btn.configure(state="disabled", text="✔ Respondido")

        correct_letter = "A"
        is_correct = (chosen == correct_letter)

        for l, (frame, badge, opcion) in self.option_buttons.items():
            if l == correct_letter:
                frame.configure(fg_color="#1B5E20", border_color="#4CAF50")
                badge.configure(fg_color="#2E7D32")
            elif l == chosen and not is_correct:
                frame.configure(fg_color="#7A1515", border_color="#F44336")
                badge.configure(fg_color="#C62828")

        for w in self.feedback_frame.winfo_children():
            w.destroy()

        if is_correct:
            fb = ctk.CTkFrame(self.feedback_frame, fg_color="#1B5E20", corner_radius=12)
            fb.pack(fill="x", pady=4)
            ctk.CTkLabel(fb,
                         text="✅  ¡Correcto! La independencia se proclamó el 15 de septiembre de 1821.",
                         font=("Arial", 11, "bold"), text_color="#A5D6A7",
                         justify="left", wraplength=700).pack(padx=14, pady=8)
        else:
            fb = ctk.CTkFrame(self.feedback_frame, fg_color="#7A1515", corner_radius=12)
            fb.pack(fill="x", pady=4)
            ctk.CTkLabel(fb,
                         text="❌  Incorrecto. La respuesta correcta es A) 1821.",
                         font=("Arial", 11, "bold"), text_color="#FFCDD2",
                         justify="left").pack(padx=14, pady=8)

        ctk.CTkButton(
            self.feedback_frame, text="Continuar →  Acto 3: Los primeros años de la República",
            font=("Arial", 12, "bold"), fg_color="#0E9A91",
            text_color="#FFFFFF", hover_color="#0A7A73", corner_radius=10, height=38
        ).pack(fill="x", pady=(6, 0))

#====================================================================
# DATOS: ficha de personaje histórico (antes llamadas repetidas)
# =====================================================================
@dataclass
class Personaje:
    """Un personaje histórico destacado, mostrado como tarjeta en PersonajesScreen."""
    imagen: str
    nombre: str
    descripcion: str
    color: str


#====================================================================
# PANTALLA DE PERSONAJES
#=====================================================================
class PersonajesScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color = "#A8D8D4")

        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text = "Personajes Destacados",
            font = ("Arial", 28, "bold"),
            text_color = "#FFFFFF"
            )
        titulo.grid(row=0, column=0, pady=(20, 15))

        panel = ctk.CTkFrame(
            self,
            fg_color = "#073233",
            corner_radius = 18
            )
        
        panel.grid(row=1, column=0, padx=20, sticky="ew")

        personajes = ctk.CTkFrame(
            panel,
            fg_color = "transparent"
            )
        
        personajes.pack(padx=20, pady=20)

        personajes_destacados = [
            Personaje(
                "sandino.png",
                "Augusto César Sandino",
                "Augusto César Sandino fue un líder revolucionario nicaragüense, símbolo de resistencia y defensor de la soberanía nacional frente a la intervención estadounidense, conocido como “El General de Hombres Libres",
                "#FF6B35",
            ),
            Personaje(
                "ruben.png",
                "Rubén Darío",
                "Rubén Darío es considerado el máximo exponente del modernismo literario en lengua española y uno de los poetas más influyentes de Latinoamérica.",
                "#FF6B35",
            ),
            Personaje(
                "blanca.png",
                "Blanca Araúz",
                "Blanca Aráuz (1909–1933) fue una telegrafista y revolucionaria nicaragüense, declarada oficialmente la primera Heroína Nacional de su país. Jugó un papel clave en la lucha contra la ocupación estadounidense organizando las comunicaciones del (EDSN) y apoyando las negociaciones de paz",
                "#FF6B35",
            ),
            Personaje(
                "benjamin.png",
                "Benjamín Francísco Zeledón",
                "Benjamín Francisco Zeledón Rodríguez (1879-1912) fue un abogado, político, militar y patriota nicaragüense reconocido como Héroe Nacional por su defensa de la soberanía y su resistencia frente a la intervención estadounidense en 1912.",
                "#FF6B35",
            ),
        ]
        for col, pj in enumerate(personajes_destacados):
            self._crear_tarjeta(personajes, pj.imagen, pj.nombre, pj.descripcion, pj.color, col)

        ctk.CTkButton(
            self,
            text = "Volver al inicio",
            command = lambda: controller.show_frame("DashboardScreen")
            ).grid(row = 2, column = 0, pady = 20)
    def _crear_tarjeta(self, parent, imagen, nombre, descripcion, color, col):

       card = ctk.CTkFrame(
           parent,
           width = 180,
           height = 300,
           fg_color = color,
           corner_radius = 15
           )
       card.grid(
           row = 0,
           column = col,
           padx = 10
           )
       card.grid_propagate(False)

       img = Image.open(os.path.join(IMG_DIR, imagen))

       img = img.resize((120, 120))

       foto = ctk.CTkImage(
           light_image = img,
           dark_image = img,
           size = (120, 120)
           )
       lbl = ctk.CTkLabel(
           card,
           image = foto,
           text = ""
           )
       lbl.image = foto
       lbl.pack(pady=15)

       ctk.CTkLabel(
           card,
           text = descripcion,
           font = ("Arial", 14, "bold"),
           wraplength = 150
           ).pack(padx=10) 


# =====================================================================
# DATOS: ficha de dato histórico (antes tupla posicional)
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


@dataclass
class OpcionQuiz:
    """Una alternativa de respuesta del quiz rápido (Dashboard) o del acto (Aventura)."""
    letra: str
    texto: str
    es_correcta: bool


# =====================================================================
# PANTALLA DE AVENTURA
# =====================================================================
class AventuraScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent", scrollbar_button_color="#0E9A91")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._build_navigation()

    # ──────────────────────────────────────────────────────
    def _build_header(self):
        banner_img = make_chapter_banner(900, 90)
        banner_ctk = ctk.CTkImage(light_image=banner_img, dark_image=banner_img, size=(900, 90))

        header = ctk.CTkFrame(self, fg_color="#4A1525", corner_radius=16, height=90)
        header.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        header.pack_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Barra de acento izquierda
        accent = ctk.CTkFrame(header, fg_color="#0E9A91", corner_radius=8, width=6)
        accent.grid(row=0, column=0, sticky="ns", padx=(14, 10), pady=10)

        txt_col = ctk.CTkFrame(header, fg_color="transparent")
        txt_col.grid(row=0, column=1, sticky="w", pady=12)

        ctk.CTkLabel(txt_col, text="Capítulo 3  ·  La Independencia de Centroamérica",
                     font=("Arial", 20, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(txt_col, text="🗓 15 de Septiembre de 1821  ·  Ciudad de Guatemala",
                     font=("Arial", 12), text_color="#B39DDB").pack(anchor="w", pady=(2, 0))

        # Chips de capítulo
        chips = ctk.CTkFrame(header, fg_color="transparent")
        chips.grid(row=0, column=2, padx=16)
        for chip_txt, chip_fg in [("Acto 2 / 5", "#0A3A3B"), ("42% completado", "#1A5E5A")]:
            c = ctk.CTkFrame(chips, fg_color=chip_fg, corner_radius=8)
            c.pack(side="left", padx=4)
            ctk.CTkLabel(c, text=chip_txt, font=("Arial", 10, "bold"),
                         text_color="#80CBC4").pack(padx=10, pady=5)

    # ──────────────────────────────────────────────────────
    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=6)
        body.grid_columnconfigure(1, weight=4)

        # ── Columna izquierda: historia + timeline ──
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.grid_columnconfigure(0, weight=1)

        # Imagen de la escena
        hist_img = Image.open(os.path.join(IMG_DIR, "cap3.png")).convert("RGB")
        hist_img = hist_img.resize((600, 240))
        self.hist_ctk = ctk.CTkImage(light_image = hist_img, dark_image = hist_img, size=(600, 240))
        hist_ctk = self.hist_ctk
        img_frame = ctk.CTkFrame(left, fg_color="#1A0A10", corner_radius=14)
        img_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        ctk.CTkLabel(img_frame, image=hist_ctk, text="").pack(padx=8, pady=8)
        ctk.CTkLabel(img_frame,
                     text="🖼  La firma del Acta de Independencia Centroamericana, 1821",
                     font=("Arial", 10, "italic"), text_color="#B39DDB").pack(pady=(0, 8))

        # Texto narrativo
        narrative = ctk.CTkFrame(left, fg_color="#1E1E2E", corner_radius=14)
        narrative.grid(row=1, column=0, sticky="nsew", pady=(0, 12))

        ctk.CTkLabel(narrative, text="⚔️  Acto 2: La Firma del Acta",
                     font=("Arial", 15, "bold"), text_color="#FFD700").pack(anchor="w", padx=18, pady=(14, 4))

        story_text = (
            "El 15 de septiembre de 1821, en el Palacio Real de la Ciudad de Guatemala, "
            "representantes de las provincias centroamericanas se reunieron para deliberar "
            "sobre el futuro de la región. Tras intensas negociaciones, firmaron el Acta de "
            "Independencia que liberaba a Centroamérica del dominio español.\n\n"
            "Nicaragua, junto a Guatemala, El Salvador, Honduras y Costa Rica, se convertía "
            "en nación libre. Sin embargo, los desafíos apenas comenzaban: ¿quiénes serían "
            "los nuevos líderes? ¿Cómo se organizaría el nuevo Estado?"
        )
        ctk.CTkLabel(narrative, text=story_text, font=("Arial", 12), text_color="#C8D0DC",
                     justify="left", wraplength=560).pack(anchor="w", padx=18, pady=(0, 14))

        # Timeline
        tl_frame = ctk.CTkFrame(left, fg_color="#0A2223", corner_radius=14)
        tl_frame.grid(row=2, column=0, sticky="nsew")
        ctk.CTkLabel(tl_frame, text="📅  Línea de tiempo",
                     font=("Arial", 14, "bold"), text_color="#0E9A91").pack(anchor="w", padx=18, pady=(12, 8))

        events = [
            EventoHistorico("1811", "🔔", "Primer Grito de Independencia en El Salvador", True,  "#0E9A91"),
            EventoHistorico("1820", "⚔️", "Levantamientos en toda Centroamérica",          False, "#4A1525"),
            EventoHistorico("1821", "✍️", "Firma del Acta de Independencia",               True,  "#FFD700"),
            EventoHistorico("1823", "🏛️", "Creación de las Provincias Unidas",             False, "#1A5E5A"),
        ]
        for evento in events:
            row_ev = ctk.CTkFrame(tl_frame,
                                  fg_color="#1A4A4B" if evento.destacado else "transparent",
                                  corner_radius=10)
            row_ev.pack(fill="x", padx=14, pady=3)

            dot = ctk.CTkFrame(row_ev, fg_color=evento.color, corner_radius=10, width=12, height=12)
            dot.pack(side="left", padx=(10, 8), pady=12)
            dot.pack_propagate(False)

            ctk.CTkLabel(row_ev, text=evento.fecha, font=("Arial", 11, "bold"),
                         text_color=evento.color, width=38).pack(side="left")
            ctk.CTkLabel(row_ev, text=evento.icono, font=("Arial", 16)).pack(side="left", padx=(4, 6))
            ctk.CTkLabel(row_ev, text=evento.descripcion, font=("Arial", 11),
                         text_color="#FFFFFF" if evento.destacado else "#80CBC4").pack(side="left", pady=12)

        ctk.CTkFrame(tl_frame, fg_color="transparent", height=8).pack()

        # ── Columna derecha: personajes + datos ──
        right = ctk.CTkFrame(body, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        # Personajes clave
        chars_card = ctk.CTkFrame(right, fg_color="#1A0A20", corner_radius=14)
        chars_card.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        ctk.CTkLabel(chars_card, text="👥  Personajes clave",
                     font=("Arial", 13, "bold"), text_color="#FFE57F").pack(anchor="w", padx=14, pady=(12, 6))

        characters = [
            PersonajeClave("GM", "#1C3A6E", "#87CEEB", "Gabino Gaínza",     "Capitán General,\nlíder de la firma"),
            PersonajeClave("JC", "#8B1A1A", "#FF8A65", "José Cecilio",      "Prócer hondureño,\nfirmante del Acta"),
            PersonajeClave("MP", "#1A5E1A", "#81C784", "Miguel Larreynaga", "Representante\nde Nicaragua"),
        ]
        for pj in characters:
            av_img = make_avatar(pj.iniciales, pj.color_fondo, pj.color_texto, 48)
            av_ctk = ctk.CTkImage(light_image=av_img, dark_image=av_img, size=(48, 48))

            char_row = ctk.CTkFrame(chars_card, fg_color="#2A1030", corner_radius=10)
            char_row.pack(fill="x", padx=12, pady=4)
            ctk.CTkLabel(char_row, image=av_ctk, text="").pack(side="left", padx=(10, 8), pady=8)
            info = ctk.CTkFrame(char_row, fg_color="transparent")
            info.pack(side="left", pady=8)
            ctk.CTkLabel(info, text=pj.nombre, font=("Arial", 12, "bold"),
                         text_color="#FFFFFF").pack(anchor="w")
            ctk.CTkLabel(info, text=pj.rol, font=("Arial", 10),
                         text_color="#B39DDB", justify="left").pack(anchor="w")

        ctk.CTkFrame(chars_card, fg_color="transparent", height=8).pack()

        # Datos históricos
        data_card = ctk.CTkFrame(right, fg_color="#062A2B", corner_radius=14)
        data_card.grid(row=1, column=0, sticky="nsew", pady=(0, 12))
        ctk.CTkLabel(data_card, text="📊  Datos históricos",
                     font=("Arial", 13, "bold"), text_color="#0E9A91").pack(anchor="w", padx=14, pady=(12, 6))

        datos_historicos = [
            DatoHistorico("📅", "Fecha", "15 Sep 1821"),
            DatoHistorico("📍", "Lugar", "Guatemala"),
            DatoHistorico("✍️", "Firmantes", "22 personas"),
            DatoHistorico("🌎", "Territorio", "~500,000 km²"),
        ]
        for dato in datos_historicos:
            r = ctk.CTkFrame(data_card, fg_color="#0A3A3B", corner_radius=8)
            r.pack(fill="x", padx=12, pady=3)
            ctk.CTkLabel(r, text=dato.icono + "  " + dato.etiqueta,
                         font=("Arial", 11), text_color="#80CBC4").pack(side="left", padx=10, pady=7)
            ctk.CTkLabel(r, text=dato.valor, font=("Arial", 11, "bold"),
                         text_color="#FFFFFF").pack(side="right", padx=10)

        ctk.CTkFrame(data_card, fg_color="transparent", height=8).pack()

        # Quiz integrado en aventura
        self._build_quiz(right)

    # ──────────────────────────────────────────────────────
    def _build_quiz(self, parent):
        self.quiz_card = ctk.CTkFrame(parent, fg_color="#2D1040", corner_radius=14)
        self.quiz_card.grid(row=2, column=0, sticky="nsew")
        self.selected_answer = tk.StringVar(value="")
        self.answered = False

        quiz_deco = make_quiz_deco(80, 80)
        deco_ctk  = ctk.CTkImage(light_image=quiz_deco, dark_image=quiz_deco, size=(80, 80))

        qhdr = ctk.CTkFrame(self.quiz_card, fg_color="#3D1A58", corner_radius=12)
        qhdr.pack(fill="x", padx=16, pady=(14, 8))
        qhdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(qhdr, image=deco_ctk, text="").grid(row=0, column=0, padx=10, pady=6)
        title_col = ctk.CTkFrame(qhdr, fg_color="transparent")
        title_col.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(title_col, text="❓  Pregunta del acto",
                     font=("Arial", 14, "bold"), text_color="#FFE57F").pack(anchor="w")
        ctk.CTkLabel(title_col, text="Responde y gana XP",
                     font=("Arial", 10), text_color="#B39DDB").pack(anchor="w")

        xp_chip = ctk.CTkFrame(qhdr, fg_color="#7A6A1A", corner_radius=8)
        xp_chip.grid(row=0, column=2, padx=12)
        ctk.CTkLabel(xp_chip, text="⭐ +50 XP",
                     font=("Arial", 10, "bold"), text_color="#FFE57F").pack(padx=8, pady=4)

        ctk.CTkLabel(
            self.quiz_card,
            text="¿Cuándo ocurrió la independencia de Centroamérica?",
            font=("Arial", 14, "bold"), text_color="#FFFFFF", justify="left"
        ).pack(anchor="w", padx=20, pady=(14, 10))

        self.option_buttons = {}
        opciones = [
            OpcionQuiz("A", "1821", True),
            OpcionQuiz("B", "1990", False),
            OpcionQuiz("C", "1512", False),
            OpcionQuiz("D", "1856", False),
        ]
        opts_frame = ctk.CTkFrame(self.quiz_card, fg_color="transparent")
        opts_frame.pack(fill="x", padx=16, pady=(0, 16))
        opts_frame.grid_columnconfigure((0, 1), weight=1)

        for i, opcion in enumerate(opciones):
            row_i = i // 2
            col_i = i % 2
            btn_frame = ctk.CTkFrame(opts_frame, fg_color="#4A1525", corner_radius=12,
                                     border_color="#6A1535", border_width=1)
            btn_frame.grid(row=row_i, column=col_i, padx=6, pady=6, sticky="nsew")

            inner = ctk.CTkFrame(btn_frame, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=12, pady=10)

            letter_badge = ctk.CTkFrame(inner, fg_color="#6A1535", corner_radius=8,
                                        width=30, height=30)
            letter_badge.pack(side="left", padx=(0, 10))
            letter_badge.pack_propagate(False)
            ctk.CTkLabel(letter_badge, text=opcion.letra, font=("Arial", 12, "bold"),
                         text_color="#FFFFFF").place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(inner, text=opcion.texto, font=("Arial", 13, "bold"),
                         text_color="#FFFFFF").pack(side="left")

            self.option_buttons[opcion.letra] = (btn_frame, letter_badge, opcion)

            btn_frame.bind("<Button-1>", lambda e, l=opcion.letra: self._select_answer(l))
            inner.bind("<Button-1>", lambda e, l=opcion.letra: self._select_answer(l))
            for child in inner.winfo_children():
                child.bind("<Button-1>", lambda e, l=opcion.letra: self._select_answer(l))

        self.confirm_btn = ctk.CTkButton(
            self.quiz_card, text="Confirmar respuesta",
            font=("Arial", 13, "bold"), fg_color="#0E9A91",
            text_color="#FFFFFF", hover_color="#0A7A73",
            corner_radius=10, height=40, state="disabled",
            command=self._confirm_answer
        )
        self.confirm_btn.pack(fill="x", padx=16, pady=(0, 8))

        self.feedback_frame = ctk.CTkFrame(self.quiz_card, fg_color="transparent")
        self.feedback_frame.pack(fill="x", padx=16, pady=(0, 12))

    def _select_answer(self, letter):
        if self.answered:
            return
        self.selected_answer.set(letter)
        for l, (frame, badge, opcion) in self.option_buttons.items():
            if l == letter:
                frame.configure(fg_color="#1A5A55", border_color="#0E9A91")
                badge.configure(fg_color="#0E9A91")
            else:
                frame.configure(fg_color="#4A1525", border_color="#6A1535")
                badge.configure(fg_color="#6A1535")
        self.confirm_btn.configure(state="normal")

    def _confirm_answer(self):
        if self.answered:
            return
        self.answered = True
        chosen = self.selected_answer.get()
        self.confirm_btn.configure(state="disabled", text="✔ Respondido")

        correct_letter = "A"
        is_correct = (chosen == correct_letter)

        for l, (frame, badge, opcion) in self.option_buttons.items():
            if l == correct_letter:
                frame.configure(fg_color="#1B5E20", border_color="#4CAF50")
                badge.configure(fg_color="#2E7D32")
            elif l == chosen and not is_correct:
                frame.configure(fg_color="#7A1515", border_color="#F44336")
                badge.configure(fg_color="#C62828")

        for w in self.feedback_frame.winfo_children():
            w.destroy()

        if is_correct:
            fb = ctk.CTkFrame(self.feedback_frame, fg_color="#1B5E20", corner_radius=12)
            fb.pack(fill="x", pady=4)
            ctk.CTkLabel(fb,
                         text="✅  ¡Correcto! La independencia se proclamó el 15 de septiembre de 1821.",
                         font=("Arial", 11, "bold"), text_color="#A5D6A7",
                         justify="left", wraplength=700).pack(padx=14, pady=8)
        else:
            fb = ctk.CTkFrame(self.feedback_frame, fg_color="#7A1515", corner_radius=12)
            fb.pack(fill="x", pady=4)
            ctk.CTkLabel(fb,
                         text="❌  Incorrecto. La respuesta correcta es A) 1821.",
                         font=("Arial", 11, "bold"), text_color="#FFCDD2",
                         justify="left").pack(padx=14, pady=8)

        ctk.CTkButton(
            self.feedback_frame, text="Continuar →  Acto 3: Los primeros años de la República",
            font=("Arial", 12, "bold"), fg_color="#0E9A91",
            text_color="#FFFFFF", hover_color="#0A7A73", corner_radius=10, height=38
        ).pack(fill="x", pady=(6, 0))

    # ──────────────────────────────────────────────────────
    def _build_navigation(self):
        nav = ctk.CTkFrame(self, fg_color=self.controller.COLOR_OSCURO, corner_radius=16, height=65)
        nav.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
        nav.pack_propagate(False)
        nav.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            nav, text="← Acto anterior", font=("Arial", 11, "bold"),
            fg_color="#0A3A3B", text_color="#80CBC4", hover_color="#0E4A4B",
            corner_radius=10, width=140, height=36
        ).grid(row=0, column=0, padx=16, pady=14)

        acts_frame = ctk.CTkFrame(nav, fg_color="transparent")
        acts_frame.grid(row=0, column=1, sticky="ew", padx=8)
        acts_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        actos = [
            ("Acto 1\nPrólogo",          True,  True),
            ("Acto 2\nLa firma",         True,  False),
            ("Acto 3\nLas juntas",       False, False),
            ("Acto 4\nCelebración",      False, False),
            ("Acto 5\nLa nueva nación",  False, False),
        ]
        for i, (label, done, current) in enumerate(actos):
            if current:
                bg = "#0E9A91"
                tc = "#FFFFFF"
            elif done:
                bg = "#1E4D4A"
                tc = "#80CBC4"
            else:
                bg = "#0A2223"
                tc = "#546E7A"
            pill = ctk.CTkFrame(acts_frame, fg_color=bg, corner_radius=8, height=38)
            pill.grid(row=0, column=i, padx=3, sticky="ew")
            pill.pack_propagate(False)
            ctk.CTkLabel(pill, text=label, font=("Arial", 8, "bold"),
                         text_color=tc, justify="center").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(
            nav, text="Acto siguiente →", font=("Arial", 11, "bold"),
            fg_color="#0E9A91", text_color="#FFFFFF", hover_color="#0A7A73",
            corner_radius=10, width=140, height=36
        ).grid(row=0, column=2, padx=16, pady=14)

#-----------------------------------------------------------------------------
#Quiz
#-----------------------------------------------------------------------------

class QuizPrecolombino(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A0A00", corner_radius=0)
        self.controller = controller

        self.pregunta_actual  = 0
        self.puntaje          = 0
        self.tiempo_restante  = TIEMPO_INICIAL
        self.timer_id         = None
        self.respondiendo     = False
        self.feedback_id      = None

        self._preparar_preguntas()
        self._crear_widgets()

    # Se llama cada vez que se entra a esta pantalla
    def on_show(self):
        self._cancelar_cronometro()
        if self.feedback_id is not None:
            self.after_cancel(self.feedback_id)
            self.feedback_id = None
        self.frame_final.place_forget()
        self._ocultar_feedback()
        self.pregunta_actual = 0
        self.puntaje = 0
        self._preparar_preguntas()
        self._mostrar_pregunta()

    def _preparar_preguntas(self):
        self.preguntas_mezcladas = []
        for q in PREGUNTAS:
            indices = list(range(len(q.opciones)))
            random.shuffle(indices)
            nuevas_opciones = [q.opciones[i] for i in indices]
            nueva_correcta  = indices.index(q.correcta)
            self.preguntas_mezcladas.append(
                Pregunta(
                    pregunta=q.pregunta,
                    opciones=nuevas_opciones,
                    correcta=nueva_correcta,
                )
            )

    def _crear_widgets(self):
        self.canvas_img = tk.Canvas(
            self, width=400, height=720,
            bg="#1A0A00", highlightthickness=0
        )
        self.canvas_img.place(x=0, y=0)
        self._dibujar_arte_precolombino()

        self.panel = tk.Frame(self, bg=COLOR_PANEL, width=880, height=720)
        self.panel.place(x=400, y=0)
        self.panel.pack_propagate(False)

        # Barra superior con botón de volver
        top_bar = tk.Frame(self.panel, bg=COLOR_PANEL)
        top_bar.pack(fill="x", padx=20, pady=(14, 0))

        btn_volver = tk.Button(
            top_bar, text="← Volver al inicio",
            font=("Helvetica", 11, "bold"),
            fg="white", bg=COLOR_OPCION_BG,
            activebackground=COLOR_OPCION_HOVER,
            relief="flat", cursor="hand2",
            command=self._volver_inicio
        )
        btn_volver.pack(side="left", ipadx=10, ipady=4)

        lbl_titulo = tk.Label(
            self.panel,
            text="🏺  QUIZ PRECOLOMBINO DE NICARAGUA  🏺",
            font=("Georgia", 16, "bold"),
            fg=COLOR_TITULO, bg=COLOR_PANEL
        )
        lbl_titulo.pack(pady=(10, 4))

        sep = tk.Canvas(self.panel, height=3, bg=COLOR_OPCION_BORDE,
                        highlightthickness=0, width=820)
        sep.pack()

        fila_info = tk.Frame(self.panel, bg=COLOR_PANEL)
        fila_info.pack(fill="x", padx=30, pady=(10, 0))

        self.lbl_numero = tk.Label(
            fila_info, text="Pregunta 1 / 7",
            font=("Helvetica", 12, "bold"),
            fg=COLOR_PREGUNTA, bg=COLOR_PANEL
        )
        self.lbl_numero.pack(side="left")

        self.lbl_score = tk.Label(
            fila_info, text="Puntaje: 0",
            font=("Helvetica", 12, "bold"),
            fg=COLOR_TITULO, bg=COLOR_PANEL
        )
        self.lbl_score.pack(side="left", padx=30)

        self.canvas_timer = tk.Canvas(
            fila_info, width=80, height=80,
            bg=COLOR_PANEL, highlightthickness=0
        )
        self.canvas_timer.pack(side="right", padx=10)
        self._dibujar_timer(TIEMPO_INICIAL)

        self.lbl_pregunta = tk.Label(
            self.panel, text="",
            font=("Georgia", 17, "bold"),
            fg=COLOR_PREGUNTA, bg=COLOR_PANEL,
            wraplength=800, justify="center"
        )
        self.lbl_pregunta.pack(pady=(22, 18))

        self.frame_opciones = tk.Frame(self.panel, bg=COLOR_PANEL)
        self.frame_opciones.pack(fill="x", padx=40)

        self.botones = []
        for i in range(3):
            btn = tk.Button(
                self.frame_opciones, text="",
                font=("Helvetica", 14, "bold"),
                fg=COLOR_TEXTO_OPC, bg=COLOR_OPCION_BG,
                activebackground=COLOR_OPCION_HOVER,
                activeforeground="white",
                relief="flat", bd=0, cursor="hand2",
                wraplength=760, justify="center", height=2,
                command=lambda idx=i: self._seleccionar_opcion(idx)
            )
            btn.pack(fill="x", pady=6, ipady=8)
            btn.configure(highlightbackground=COLOR_OPCION_BORDE, highlightthickness=2)
            btn.bind("<Enter>", lambda e, b=btn: self._hover_on(b))
            btn.bind("<Leave>", lambda e, b=btn: self._hover_off(b))
            self.botones.append(btn)

        self.frame_feedback = tk.Frame(self.panel, bg=COLOR_CORRECTO, width=880, height=720)
        self.lbl_feedback = tk.Label(
            self.frame_feedback, text="",
            font=("Georgia", 60, "bold"),
            fg="white", bg=COLOR_CORRECTO
        )
        self.lbl_feedback.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_final = tk.Frame(self, bg="#1A0A00", width=1280, height=720)
        self.lbl_final = tk.Label(
            self.frame_final, text="",
            font=("Georgia", 30, "bold"),
            fg=COLOR_TITULO, bg="#1A0A00", justify="center"
        )
        self.lbl_final.place(relx=0.5, rely=0.4, anchor="center")

        self.btn_reiniciar = tk.Button(
            self.frame_final, text="🔄  Jugar de nuevo",
            font=("Helvetica", 16, "bold"),
            fg="white", bg=COLOR_OPCION_BG,
            activebackground=COLOR_OPCION_HOVER,
            relief="flat", cursor="hand2",
            command=self._reiniciar
        )
        self.btn_reiniciar.place(relx=0.5, rely=0.65, anchor="center", width=260, height=55)

        btn_volver_final = tk.Button(
            self.frame_final, text="← Volver al inicio",
            font=("Helvetica", 13, "bold"),
            fg="white", bg=COLOR_OPCION_BG,
            activebackground=COLOR_OPCION_HOVER,
            relief="flat", cursor="hand2",
            command=self._volver_inicio
        )
        btn_volver_final.place(relx=0.5, rely=0.78, anchor="center", width=220, height=44)

    def _volver_inicio(self):
        self._cancelar_cronometro()
        if self.feedback_id is not None:
            self.after_cancel(self.feedback_id)
            self.feedback_id = None
        self.frame_final.place_forget()
        self._ocultar_feedback()
        self.controller.show_frame("DashboardScreen")

    # ─── (resto de métodos sin cambios, usando self.after / self en vez de self.root) ───
    def _dibujar_arte_precolombino(self):
        c = self.canvas_img
        c.delete("all")
        W, H = 400, 720
        colores_fondo = ["#1A0A00","#200C00","#260E00","#2C1000","#321200"]
        fila_h = H // len(colores_fondo)
        for i, col in enumerate(colores_fondo):
            c.create_rectangle(0, i*fila_h, W, (i+1)*fila_h, fill=col, outline="")
        c.create_rectangle(385, 0, 400, H, fill="#C8860A", outline="")
        for y in range(0, H, 40):
            c.create_rectangle(385, y, 400, y+20, fill="#8B5E00", outline="")
        cx, cy = 200, 200
        for r, col in [(120,"#4A2800"),(100,"#6B3A00"),(80,"#8B5000"),
                       (60,"#C8860A"),(40,"#FFD700"),(20,"#FFF8DC")]:
            c.create_oval(cx-r, cy-r, cx+r, cy+r, fill=col, outline="")
        num_rayos = 12
        for k in range(num_rayos):
            ang = math.radians(k * 360 / num_rayos)
            ang2 = math.radians(k * 360 / num_rayos + 15)
            x1 = cx + 125 * math.cos(ang)
            y1 = cy + 125 * math.sin(ang)
            x2 = cx + 125 * math.cos(ang2)
            y2 = cy + 125 * math.sin(ang2)
            x3 = cx + 145 * math.cos(ang + math.radians(7.5))
            y3 = cy + 145 * math.sin(ang + math.radians(7.5))
            c.create_polygon(x1,y1, x2,y2, x3,y3, fill="#C8860A", outline="#FFD700")
        c.create_oval(cx-10, cy-10, cx+10, cy+10, fill="#1A0A00", outline="")
        c.create_oval(cx-5,  cy-5,  cx+5,  cy+5,  fill="#FFFFFF", outline="")
        puntos_serpiente = []
        for t in range(0, 360, 5):
            r2 = 165 + 15 * math.sin(math.radians(t * 3))
            ang = math.radians(t)
            px = cx + r2 * math.cos(ang)
            py = cy + r2 * math.sin(ang)
            puntos_serpiente.extend([px, py])
        c.create_line(*puntos_serpiente, fill="#228B22", width=4, smooth=True)
        c.create_oval(175, 340, 225, 390, fill="#C8860A", outline="#FFD700", width=2)
        c.create_line(200, 390, 200, 460, fill="#C8860A", width=4)
        c.create_line(160, 410, 240, 410, fill="#C8860A", width=4)
        c.create_line(200, 460, 170, 500, fill="#C8860A", width=4)
        c.create_line(200, 460, 230, 500, fill="#C8860A", width=4)
        for ang_p in range(-60, 61, 20):
            rad = math.radians(ang_p - 90)
            px = 200 + 35 * math.cos(rad)
            py = 365 + 35 * math.sin(rad)
            c.create_line(200, 340, px, py, fill="#228B22", width=2)
        self._dibujar_rombo(c, 80, 560, 55, "#C8860A", "#FFD700")
        self._dibujar_rombo(c, 320, 560, 55, "#8B5000", "#C8860A")
        self._dibujar_espiral(c, 200, 620, 50, "#FFD700")
        self._dibujar_greca(c, 10, 10, W-15, 70, "#C8860A", "#8B5000")
        c.create_text(200, 700, text="Nicaragua Ancestral", font=("Georgia", 11, "italic"), fill="#C8860A")

    def _dibujar_rombo(self, c, cx, cy, tam, color_relleno, color_borde):
        pts = [cx, cy-tam, cx+tam, cy, cx, cy+tam, cx-tam, cy]
        c.create_polygon(*pts, fill=color_relleno, outline=color_borde, width=2)
        inner = tam * 0.5
        pts2 = [cx, cy-inner, cx+inner, cy, cx, cy+inner, cx-inner, cy]
        c.create_polygon(*pts2, fill=color_borde, outline="")

    def _dibujar_espiral(self, c, cx, cy, radio_max, color):
        puntos = []
        vueltas = 3
        pasos   = 200
        for i in range(pasos):
            t   = vueltas * 2 * math.pi * i / pasos
            r   = radio_max * i / pasos
            px  = cx + r * math.cos(t)
            py  = cy + r * math.sin(t)
            puntos.extend([px, py])
        if len(puntos) >= 4:
            c.create_line(*puntos, fill=color, width=3, smooth=True)

    def _dibujar_greca(self, c, x0, y0, x1, y1, col1, col2):
        c.create_rectangle(x0, y0, x1, y1, fill=col2, outline="")
        paso = 30
        x = x0
        while x < x1:
            c.create_rectangle(x, y0+2, x+20, y0+22, fill=col1, outline="")
            c.create_rectangle(x+5, y0+7, x+15, y0+17, fill=col2, outline="")
            x += paso

    def _dibujar_timer(self, segundos):
        c = self.canvas_timer
        c.delete("all")
        W = 80
        if segundos > 20:
            color_arco = COLOR_TIMER_OK
        elif segundos > 10:
            color_arco = COLOR_TIMER_WARN
        else:
            color_arco = COLOR_TIMER_DANGER
        c.create_oval(4, 4, W-4, W-4, fill="#1A0A00", outline="#555555", width=2)
        extent = -360 * (segundos / TIEMPO_INICIAL)
        c.create_arc(8, 8, W-8, W-8, start=90, extent=extent, fill=color_arco, outline="")
        c.create_text(W//2, W//2, text=str(segundos), font=("Helvetica", 18, "bold"), fill="white")

    def _mostrar_pregunta(self):
        if self.pregunta_actual >= len(self.preguntas_mezcladas):
            self._mostrar_resultado_final()
            return
        q = self.preguntas_mezcladas[self.pregunta_actual]
        self.lbl_numero.config(text=f"Pregunta {self.pregunta_actual + 1} / {len(self.preguntas_mezcladas)}")
        self.lbl_score.config(text=f"Puntaje: {self.puntaje}")
        self.lbl_pregunta.config(text=q.pregunta)
        letras = ["A", "B", "C"]
        for i, btn in enumerate(self.botones):
            btn.config(text=f"  {letras[i]})  {q.opciones[i]}", bg=COLOR_OPCION_BG, fg=COLOR_TEXTO_OPC, state="normal")
        self.tiempo_restante = TIEMPO_INICIAL
        self._dibujar_timer(TIEMPO_INICIAL)
        self.respondiendo = False
        self._iniciar_cronometro()

    def _iniciar_cronometro(self):
        self._cancelar_cronometro()
        self._tick()

    def _cancelar_cronometro(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def _tick(self):
        if self.respondiendo:
            return
        self._dibujar_timer(self.tiempo_restante)
        if self.tiempo_restante <= 0:
            self.respondiendo = True
            self._mostrar_feedback("⏰  Se acabó\nel tiempo", COLOR_INCORRECTO)
            return
        self.tiempo_restante -= 1
        self.timer_id = self.after(1000, self._tick)

    def _seleccionar_opcion(self, idx_seleccionado: int):
        if self.respondiendo:
            return
        self.respondiendo = True
        self._cancelar_cronometro()
        q = self.preguntas_mezcladas[self.pregunta_actual]
        es_correcta = (idx_seleccionado == q.correcta)
        for i, btn in enumerate(self.botones):
            btn.config(state="disabled")
            if i == q.correcta:
                btn.config(bg="#1B7F00", fg="white")
            elif i == idx_seleccionado:
                btn.config(bg="#8B0000", fg="white")
        if es_correcta:
            self.puntaje += 1
            self._mostrar_feedback("✔  CORRECTO", COLOR_CORRECTO)
        else:
            self._mostrar_feedback("✘  INCORRECTO", COLOR_INCORRECTO)

    def _mostrar_feedback(self, mensaje: str, color_fondo: str):
        if self.feedback_id is not None:
            self.after_cancel(self.feedback_id)
        self.frame_feedback.config(bg=color_fondo)
        self.lbl_feedback.config(text=mensaje, bg=color_fondo, font=("Georgia", 52, "bold"))
        self.frame_feedback.place(x=0, y=0, width=880, height=720)
        self.frame_feedback.lift()
        self.feedback_id = self.after(1800, self._siguiente_pregunta)

    def _ocultar_feedback(self):
        self.frame_feedback.place_forget()

    def _siguiente_pregunta(self):
        self._ocultar_feedback()
        self.pregunta_actual += 1
        self._mostrar_pregunta()

    def _mostrar_resultado_final(self):
        self._cancelar_cronometro()
        total = len(self.preguntas_mezcladas)
        porcentaje = int(self.puntaje / total * 100)
        if porcentaje >= 80:
            calificacion = "¡Excelente! 🏆\nEres un experto en historia precolombina."
        elif porcentaje >= 50:
            calificacion = "¡Bien hecho! 👍\nSigue aprendiendo sobre nuestra historia."
        else:
            calificacion = "Sigue intentándolo 📚\nHay mucho por descubrir."
        texto_final = (
            f"🏺  Quiz Terminado  🏺\n\n"
            f"Respuestas correctas: {self.puntaje} / {total}\n"
            f"Porcentaje: {porcentaje}%\n\n"
            f"{calificacion}"
        )
        self.lbl_final.config(text=texto_final)
        self.frame_final.place(x=0, y=0, width=1280, height=720)
        self.frame_final.lift()

    def _reiniciar(self):
        self.frame_final.place_forget()
        self._ocultar_feedback()
        self.pregunta_actual = 0
        self.puntaje = 0
        self._preparar_preguntas()
        self._mostrar_pregunta()

    def _hover_on(self, btn: tk.Button):
        if btn["state"] != "disabled":
            btn.config(bg=COLOR_OPCION_HOVER)

    def _hover_off(self, btn: tk.Button):
        if btn["state"] != "disabled" and btn["bg"] == COLOR_OPCION_HOVER:
            btn.config(bg=COLOR_OPCION_BG)

# -------- AJUSTES --------

class AjustesScreen(ctk.CTkFrame):
    def _cerrar_sesion(self):
        #destruye toda la app y la reinicia
        self.controller.reiniciar_sesion()

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.modo_oscuro = False

        self.bg_actual = "#F5F5F5"
        self.fg_actual = "black"

        self._crear_switch_func = self._crear_switch  # alias interno

        self.frame = tk.Frame(self, bg=self.bg_actual)
        self.frame.pack(fill="both", expand=True, padx=30, pady=20)

        self._build_ui()

    # ──────────────────────────────────────────────
    def _crear_switch(self, parent, estado=True, comando=None):
        canvas = tk.Canvas(
            parent, width=52, height=28,
            bg=parent["bg"], highlightthickness=0
        )
        valor = {"estado": estado}

        def dibujar():
            canvas.delete("all")
            if valor["estado"]:
                color = "#1976D2"
                x = 27
            else:
                color = "#C7C7C7"
                x = 3
            canvas.create_oval(2, 2, 50, 26, fill=color, outline=color)
            canvas.create_oval(x, 4, x+20, 24, fill="white", outline="white")

        def cambiar(event=None):
            valor["estado"] = not valor["estado"]
            dibujar()
            if comando:
                comando(valor["estado"])

        canvas.bind("<Button-1>", cambiar)
        dibujar()
        return canvas

    # ──────────────────────────────────────────────
    def _cambiar_modo(self, estado):
        self.modo_oscuro = estado

        if estado:
            self.bg_actual = "#2D2D2D"
            self.fg_actual = "white"
        else:
            self.bg_actual = "#F5F5F5"
            self.fg_actual = "black"

        self.frame.configure(bg=self.bg_actual)
        self._actualizar_colores(self.frame, self.bg_actual, self.fg_actual)

    def _actualizar_colores(self, contenedor, bg, fg):
        for widget in contenedor.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except Exception:
                pass
            # Recursivo para sub-frames (filas)
            if isinstance(widget, tk.Frame):
                self._actualizar_colores(widget, bg, fg)

    # ──────────────────────────────────────────────
    def _build_ui(self):
        frame = self.frame

        # Título
        titulo = tk.Label(
            frame, text="⚙ Ajustes",
            bg="#F8E56A", font=("Arial", 16, "bold"),
            padx=10, pady=5
        )
        titulo.pack(anchor="center", pady=10)

        # Accesibilidad
        tk.Label(frame, text="Accesibilidad", font=("Arial", 13, "bold"),
                 bg=self.bg_actual, fg=self.fg_actual).pack(anchor="w", pady=(15, 5))

        tk.Label(frame, text="Tamaño de fuente",
                 bg=self.bg_actual, fg=self.fg_actual).pack(anchor="w")

        fuente = tk.Scale(frame, from_=8, to=24, orient="horizontal", length=250)
        fuente.set(12)
        fuente.pack(anchor="w", pady=5)

        fila = tk.Frame(frame, bg=self.bg_actual)
        fila.pack(fill="x")
        tk.Label(fila, text="Subtítulos", bg=self.bg_actual, fg=self.fg_actual,
                 font=("Arial", 11)).pack(side="left")
        self._crear_switch(fila, True).pack(side="left")

        # Juego
        tk.Label(frame, text="Juego", font=("Arial", 13, "bold"),
                 bg=self.bg_actual, fg=self.fg_actual).pack(anchor="w", pady=(20, 5))

        fila2 = tk.Frame(frame, bg=self.bg_actual)
        fila2.pack(fill="x")
        tk.Label(fila2, text="Respuestas de alta retroalimentación",
                 bg=self.bg_actual, fg=self.fg_actual,
                 font=("Arial", 11)).pack(side="left")
        self._crear_switch(fila2, True).pack(side="left")

        # Personalización
        tk.Label(frame, text="Personalización", font=("Arial", 13, "bold"),
                 bg=self.bg_actual, fg=self.fg_actual).pack(anchor="w", pady=(20, 5))

        tk.Button(
            frame, text="Editar perfil",
            command=lambda: messagebox.showinfo(
                "Perfil", "Aquí se abriría la edición del perfil."
            )
        ).pack(anchor="w", pady=5)

        tk.Label(frame, text="Volumen",
                 bg=self.bg_actual, fg=self.fg_actual).pack(anchor="w")

        vol = tk.Scale(frame, from_=0, to=100, orient="horizontal", length=250)
        vol.set(50)
        vol.pack(anchor="w", pady=5)

        fila3 = tk.Frame(frame, bg=self.bg_actual)
        fila3.pack(fill="x")
        tk.Label(fila3, text="Modo oscuro", bg=self.bg_actual, fg=self.fg_actual,
                 font=("Arial", 11)).pack(side="left")
        self._crear_switch(fila3, False, self._cambiar_modo).pack(side="left")

        # Idioma
        tk.Label(frame, text="Idioma", bg=self.bg_actual, fg=self.fg_actual,
                 font=("Arial", 11)).pack(anchor="w", pady=(20, 5))

        idioma = ttk.Combobox(
            frame, values=["Español", "Miskito"],
            state="readonly", width=18
        )
        idioma.current(0)
        idioma.pack(anchor="w")

        def seleccionar(event):
            messagebox.showinfo("Idioma", f"Idioma seleccionado: {idioma.get()}")

        idioma.bind("<<ComboboxSelected>>", seleccionar)

        # Botón volver
        tk.Button(
            frame, text="Volver al inicio",
            bg="#F8E56A", font=("Arial", 11, "bold"),
            width=20,
            command=lambda: self.controller.show_frame("DashboardScreen")
        ).pack(pady=40)

        # Volver al inicio
        tk.Button(
            frame, text = "🔒 Cerrar Sesión",
            bg = "#C0392B", fg = "white",
            font = ("Arial", 11, "bold"),
            width = 20,
            command = self._cerrar_sesion
            ).pack(pady=(10, 40))