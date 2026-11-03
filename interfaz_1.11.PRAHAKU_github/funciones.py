from PIL import Image, ImageDraw, ImageFont
import base64
import io
import math
import asyncio
import inspect
import flet as ft
from datos import TIEMPO_INICIAL
from datos import img as ruta_img  # helper de datos.py: devuelve "Imagenes/<nombre>"
# Compatibilidad entre versiones de Flet (ImageFit en <0.80, BoxFit en >=0.80)
_BoxFit = getattr(ft, "BoxFit", None) or getattr(ft, "ImageFit")
FIT_FILL = _BoxFit.FILL


# =====================================================================
# HELPERS DE TRADUCCIÓN CTk / tk  →  Flet
# =====================================================================
FONT = "Arial"
_SIN = object()          # centinela: "no cambiar este valor"


_JUST = {"left": ft.TextAlign.LEFT, "center": ft.TextAlign.CENTER, "right": ft.TextAlign.RIGHT}




# =====================================================================
# CONTROLES REUTILIZABLES
# =====================================================================
@ft.control
class Boton(ft.Container):
    

    def _setup(self, texto, comando, fg, hover, color, size, bold, familia, anchor,
               activo, color_off):
        self._cmd = comando
        self._color_fondo = fg
        self._color_hover = hover
        self._color_texto = color
        self._color_texto_off = color_off
        self._activo = activo
        self._etiqueta = T(texto, size, bold, color if activo else color_off,
                           justify="center", familia=familia)
        self.content = self._etiqueta
        self.alignment = A(-1, 0) if anchor == "w" else A(0, 0)
        self.bgcolor = fg
        self.on_click = self._clic
        self.on_hover = self._al_pasar
        return self

    def configurar(self, texto=None, activo=None, fondo=_SIN, color_texto=None, hover=_SIN):
        
        if texto is not None:
            self._etiqueta.value = texto
        if activo is not None:
            self._activo = activo
        if fondo is not _SIN:
            self._color_fondo = fondo
            self.bgcolor = fondo
        if color_texto is not None:
            self._color_texto = color_texto
        if hover is not _SIN:
            self._color_hover = hover
        self._etiqueta.color = self._color_texto if self._activo else self._color_texto_off
        refrescar(self)

    def _clic(self, e):
        if self._activo and self._cmd:
            self._cmd()

    def _al_pasar(self, e):
        if not self._activo or not self._color_hover:
            return
        dentro = str(e.data).lower() == "true"
        self.bgcolor = self._color_hover if dentro else self._color_fondo
        self.update()



@ft.control
class Interruptor(ft.Container):
    

    def _setup(self, estado=True, comando=None):
        self._estado = estado
        self._comando = comando
        self._pista = ft.Container(left=2, top=2, width=48, height=24, border_radius=12)
        self._perilla = ft.Container(top=4, width=20, height=20, border_radius=10,
                                     bgcolor="white")
        self.width = 52
        self.height = 28
        self.content = ft.Stack(controls=[self._pista, self._perilla], width=52, height=28)
        self.on_click = self._cambiar
        self._dibujar()
        return self

    def _dibujar(self):
        self._pista.bgcolor = "#1976D2" if self._estado else "#C7C7C7"
        self._perilla.left = 27 if self._estado else 3

    def _cambiar(self, e):
        self._estado = not self._estado
        self._dibujar()
        self.update()
        if self._comando:
            self._comando(self._estado)

# =====================================================================
# ILUSTRACIONES DEL QUIZ (antes tk.Canvas) — generadas con Pillow
# =====================================================================
_LANCZOS = getattr(Image, "Resampling", Image).LANCZOS


# =====================================================================
# PUENTE PIL -> FLET
# =====================================================================

def pil_to_base64(imagen: Image.Image, formato: str = "PNG") -> str:
    """Convierte una imagen PIL en una cadena base64 (sin prefijo data:)."""
    buffer = io.BytesIO()
    imagen.save(buffer, format=formato)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def pil_to_flet(imagen, width=None, height=None, fit=None, **kwargs):
    return ft.Image(
        src=pil_to_base64(imagen),   # en Flet 1.x src acepta base64
        width=width if width is not None else imagen.width,
        height=height if height is not None else imagen.height,
        fit=fit if fit is not None else FIT_FILL,
        **kwargs,
    )
# =====================================================================
# HELPERS DE IMÁGENES GENERADAS POR CÓDIGO
# =====================================================================

def make_hero_image(w=420, h=190):
    """Ilustración del banner hero: cielo, volcán, ciudad colonial, personaje."""
    img = Image.new("RGB", (w, h), "#1B5E5A")
    draw = ImageDraw.Draw(img)

    for y in range(h):
        t = y / h
        r = int(27 + (96 - 27) * t)
        g = int(94 + (180 - 94) * t)
        b = int(90 + (120 - 90) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    volcano_pts = [(260, 190), (320, 70), (380, 190)]
    draw.polygon(volcano_pts, fill="#2D4A3E")
    draw.polygon([(310, 72), (320, 60), (330, 72)], fill="#FF6B35")
    draw.polygon([(313, 73), (320, 63), (327, 73)], fill="#FF9500")

    draw.polygon([(180, 190), (230, 100), (280, 190)], fill="#1E3D30")

    draw.ellipse([160, 155, 380, 195], fill="#1A7A8A")
    draw.ellipse([165, 158, 375, 193], fill="#0E9A91")

    draw.rectangle([60, 120, 160, 185], fill="#C4A882")
    draw.rectangle([85, 100, 135, 125], fill="#B8956A")
    draw.polygon([(85, 100), (110, 80), (135, 100)], fill="#A07850")
    draw.rectangle([70, 135, 85, 155], fill="#5B8FAA")
    draw.rectangle([92, 135, 107, 155], fill="#5B8FAA")
    draw.rectangle([115, 135, 130, 155], fill="#5B8FAA")
    draw.rectangle([138, 135, 153, 155], fill="#5B8FAA")

    px, py = 55, 95
    draw.ellipse([px + 8, py, px + 22, py + 14], fill="#F5C68A")
    draw.rectangle([px + 5, py + 14, px + 25, py + 45], fill="#8B4513")
    draw.rectangle([px, py + 15, px + 10, py + 42], fill="#6B3410")
    draw.rectangle([px + 20, py + 15, px + 30, py + 42], fill="#6B3410")
    draw.rectangle([px + 7, py + 45, px + 14, py + 65], fill="#4A3728")
    draw.rectangle([px + 16, py + 45, px + 23, py + 65], fill="#4A3728")
    draw.rectangle([px + 20, py + 22, px + 34, py + 36], fill="#E8D5A0")
    draw.line([(px + 27, py + 22), (px + 27, py + 36)], fill="#8B7355", width=1)

    for cx, cy, cr in [(330, 35, 18), (350, 28, 14), (360, 38, 12), (80, 25, 16), (95, 20, 12)]:
        draw.ellipse([cx - cr, cy - cr // 2, cx + cr, cy + cr // 2], fill="#FFFFFF80")

    return img


def make_chapter_image(w=110, h=90, chapter=3):
    img = Image.new("RGB", (w, h), "#4A1525")
    draw = ImageDraw.Draw(img)

    if chapter == 3:
        for y in range(h):
            t = y / h
            r = int(74 - 30 * t)
            g = int(21 + 10 * t)
            b = int(37 + 20 * t)
            draw.line([(0, y), (w, y)], fill=(r, g, b))

        draw.ellipse([w // 2 - 20, 10, w // 2 + 20, 50], fill="#FF9500")
        draw.ellipse([w // 2 - 14, 16, w // 2 + 14, 44], fill="#FFD060")

        figures = [(15, 55), (30, 50), (50, 48), (70, 52), (88, 56)]
        for fx, fy in figures:
            draw.ellipse([fx, fy - 10, fx + 10, fy], fill="#1A0A10")
            draw.rectangle([fx - 2, fy, fx + 12, fy + 25], fill="#1A0A10")
        draw.line([(50, 48), (50, 25)], fill="#C0C0C0", width=2)
        draw.polygon([(50, 25), (68, 30), (50, 35)], fill="#0033A0")
        draw.polygon([(50, 30), (68, 35), (50, 40)], fill="#FFFFFF")

    return img


def make_map_slot_image(w=95, h=85, chapter_num=1, locked=False):
    img = Image.new("RGB", (w, h), "#0A2223")
    draw = ImageDraw.Draw(img)

    if locked:
        for y in range(0, h, 8):
            for x in range(0, w, 8):
                draw.ellipse([x, y, x + 2, y + 2], fill="#1A3A3B")
        return img

    palettes = {
        1: ("#2D5A1B", "#4A8C2A", "#8BC34A"),
        2: ("#8B4513", "#C4A882", "#FFD700"),
        3: ("#1A3A6B", "#2E6DBF", "#87CEEB"),
        6: ("#1B5E5A", "#0E9A91", "#80CBC4"),
    }
    cols = palettes.get(chapter_num, ("#1E4D4A", "#2D7A74", "#4DB8B0"))

    for y in range(h):
        t = y / h
        r = int(int(cols[0][1:3], 16) * (1 - t) + int(cols[1][1:3], 16) * t)
        g = int(int(cols[0][3:5], 16) * (1 - t) + int(cols[1][3:5], 16) * t)
        b = int(int(cols[0][5:7], 16) * (1 - t) + int(cols[1][5:7], 16) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    if chapter_num == 1:
        draw.polygon([(w//2 - 20, h - 20), (w//2, h//2 - 5), (w//2 + 20, h - 20)], fill=cols[2])
        draw.rectangle([w//2 - 15, h - 20, w//2 + 15, h - 10], fill=cols[2])
    elif chapter_num == 2:
        draw.rectangle([w//2 - 18, h//2, w//2 + 18, h - 10], fill=cols[2])
        draw.polygon([(w//2 - 18, h//2), (w//2, h//2 - 18), (w//2 + 18, h//2)], fill=cols[1])
        draw.rectangle([w//2 - 5, h//2 + 8, w//2 + 5, h//2 + 22], fill=cols[0])
    elif chapter_num == 3:
        draw.rectangle([w//2, h//2 - 18, w//2 + 2, h//2 + 18], fill="#C0C0C0")
        draw.polygon([(w//2, h//2 - 18), (w//2 + 22, h//2 - 8), (w//2, h//2 + 2)], fill="#0033A0")
    elif chapter_num == 6:
        for bx in [10, 25, 42, 58, 72]:
            bh = 15 + (bx % 3) * 8
            draw.rectangle([bx, h - bh - 5, bx + 12, h - 5], fill=cols[2])
            for wy in range(h - bh, h - 8, 6):
                draw.rectangle([bx + 2, wy, bx + 5, wy + 3], fill="#FFD700")

    return img


def make_hex_badge(emoji_char, color_fill, size=52):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy, r = size // 2, size // 2, size // 2 - 2
    pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=color_fill)

    r2 = r - 3
    pts2 = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        pts2.append((cx + r2 * math.cos(angle), cy + r2 * math.sin(angle)))
    draw.polygon(pts2, fill=color_fill)

    return img


def make_avatar(initials, color_bg, color_text, size=58):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, size - 2, size - 2], fill=color_bg, outline="#0E9A91", width=3)
    draw.ellipse([0, 0, size, size], outline="#0E9A91", width=2)

    font_size = size // 3
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initials, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((size - tw) / 2, (size - th) / 2 - 2), initials, fill=color_text, font=font)

    return img


def make_user_avatar(size=68):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, size, size], fill="#FFE57F", outline="#FFFFFF", width=3)

    cx = size // 2
    draw.ellipse([cx - 12, 12, cx + 12, 36], fill="#F5A623")
    draw.ellipse([cx - 20, 38, cx + 20, 62], fill="#E8943A")

    return img


def make_quiz_deco(w=80, h=80):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rectangle([5, 15, 55, 70], fill="#FFF8E7", outline="#FFD700", width=2)
    draw.rectangle([5, 15, 14, 70], fill="#FFD700")
    for ly in range(25, 65, 8):
        draw.line([(17, ly), (50, ly)], fill="#FFD700", width=1)

    draw.polygon([(58, 10), (75, 5), (65, 40)], fill="#FFD700")
    draw.polygon([(58, 10), (65, 40), (56, 35)], fill="#FFA500")
    draw.line([(65, 40), (50, 68)], fill="#8B6914", width=2)

    draw.polygon([(68, 55), (70, 48), (72, 55), (79, 55), (73, 59), (76, 66),
                  (70, 62), (64, 66), (67, 59), (61, 55)], fill="#FFD700")

    return img


def make_logo(size=62) -> ft.Image:
    """Logo cuadrado"""
    return ft.Image(
        src=ruta_img("logo.png"),
        width=size,
        height=size,
        fit=FIT_FILL,
    )


def make_historia_image(w=310, h=220):
    img = Image.new("RGB", (w, h), "#3B1020")
    draw = ImageDraw.Draw(img)

    for y in range(h):
        t = y / h
        r = int(80 + (140 - 80) * (1 - t))
        g = int(30 + (70 - 30) * (1 - t))
        b = int(20 + (50 - 20) * (1 - t))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    draw.rectangle([w - 100, 10, w - 20, 110], fill="#87CEEB")
    draw.rectangle([w - 98, 12, w - 22, 108], fill="#B0E0FF")
    draw.line([(w - 60, 12), (w - 60, 108)], fill="#8B6914", width=4)
    draw.line([(w - 98, 60), (w - 22, 60)], fill="#8B6914", width=4)

    draw.polygon([(20, 145), (w - 20, 145), (w - 40, h - 10), (40, h - 10)], fill="#6B3A1F")
    draw.polygon([(20, 145), (w - 20, 145), (w - 20, 155), (20, 155)], fill="#8B5E3C")

    draw.rectangle([w // 2 - 55, 118, w // 2 + 55, 148], fill="#FFFDE7")
    draw.rectangle([w // 2 - 53, 120, w // 2 + 53, 146], fill="#FFF9C4")
    for lx in range(w // 2 - 48, w // 2 + 48, 7):
        draw.line([(lx, 125), (lx, 143)], fill="#C8B400", width=1)
    draw.ellipse([w // 2 + 30, 127, w // 2 + 50, 143], fill="#CC0000", outline="#880000", width=1)

    draw.ellipse([w // 2 - 80, 130, w // 2 - 60, 150], fill="#1A0A05", outline="#4A2810", width=2)
    draw.ellipse([w // 2 - 78, 131, w // 2 - 62, 145], fill="#0D0705")
    draw.polygon([(w // 2 - 70, 132), (w // 2 - 50, 90), (w // 2 - 65, 130)], fill="#F5F0DC")
    draw.polygon([(w // 2 - 70, 132), (w // 2 - 55, 95), (w // 2 - 60, 128)], fill="#E8D9A0")

    figure_data = [
        (40,  70, "#1C3A6E", "#2E5BA8"),
        (90,  60, "#8B1A1A", "#C0392B"),
        (155, 55, "#1A1A1A", "#3A3A3A"),
        (220, 62, "#1C3A6E", "#2E5BA8"),
        (270, 72, "#4A3000", "#7A5000"),
    ]
    for fx, fy, body_col, shadow_col in figure_data:
        draw.ellipse([fx, fy - 18, fx + 18, fy], fill="#F5C890")
        draw.polygon([(fx - 5, fy), (fx + 23, fy), (fx + 20, fy + 55), (fx - 2, fy + 55)], fill=body_col)
        draw.polygon([(fx - 5, fy), (fx + 23, fy), (fx + 19, fy + 30), (fx - 1, fy + 30)], fill=shadow_col)
        if fx == 155:
            draw.line([(fx + 18, fy + 15), (fx + 55, fy + 55)], fill=body_col, width=6)
            draw.line([(fx + 55, fy + 55), (fx + 65, fy + 58)], fill="#F5C890", width=5)

    draw.ellipse([30, 138, 100, 148], fill="#3A1A0A")
    draw.ellipse([230, 138, 300, 148], fill="#3A1A0A")

    draw.rectangle([0, 0, w - 1, h - 1], outline="#8B6914", width=6)
    draw.rectangle([4, 4, w - 5, h - 5], outline="#C8A840", width=2)

    return img


def make_chapter_banner(w=900, h=90):
    img = Image.new("RGB", (w, h), "#4A1525")
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(74 * (1 - t * 0.4))
        g = int(21 * (1 - t * 0.2))
        b = int(37 * (1 - t * 0.3))
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    draw.rectangle([0, 0, 6, h], fill="#0E9A91")
    return img


def make_login_bg(w=1360, h=880):
    """Fondo ilustrado para la pantalla de login"""
    img = Image.new("RGB", (w, h), "#062A2B")
    draw = ImageDraw.Draw(img)

    # Degradado de fondo oscuro con tono teal
    for y in range(h):
        t = y / h
        r = int(6  + (20 - 6)  * t)
        g = int(42 + (70 - 42) * t)
        b = int(43 + (65 - 43) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Volcán grande fondo derecho
    draw.polygon([(w - 300, h), (w - 100, h // 2 - 80), (w + 80, h)], fill="#0A3A3B")
    draw.polygon([(w - 100, h // 2 - 80), (w - 100, h // 2 - 72), (w - 88, h // 2 - 60),
                  (w - 112, h // 2 - 60)], fill="#FF6B35")

    # Segundo volcán izquierdo
    draw.polygon([(-80, h), (180, h // 2 + 20), (420, h)], fill="#082E2F")

    # Lago espejo en la base
    draw.ellipse([200, h - 160, w - 200, h + 40], fill="#0E4A4B")
    draw.ellipse([220, h - 145, w - 220, h + 20], fill="#0A5A5B")

    # Línea de acento horizontal
    draw.rectangle([0, 0, w, 6], fill="#0E9A91")

    # Estrellas / partículas de fondo
    import random
    rng = random.Random(42)
    for _ in range(120):
        sx = rng.randint(0, w)
        sy = rng.randint(0, h // 2)
        sr = rng.randint(1, 3)
        alpha = rng.randint(80, 200)
        draw.ellipse([sx, sy, sx + sr, sy + sr], fill=(255, 255, 255, alpha))

    return img


def make_login_bg_control(w=1360, h=880) -> ft.Stack:
    """Fondo de login + bandera superpuesta.

    Uso: page.add(make_login_bg_control()) o como primer hijo de un ft.Stack mayor.
    """
    return ft.Stack(
        controls=[
            pil_to_flet(make_login_bg(w, h), width=w, height=h),
            ft.Image(
                src=ruta_img("bandera.png"),
                width=100,
                height=60,
                fit=FIT_FILL,
                left=30,
                top=40,
            ),
        ],
        width=w,
        height=h,
    )

    
def px(pt):
    """Los widgets tk.* usan puntos; Flet usa píxeles (1 pt = 4/3 px a 96 dpi)"""
    return round(pt * 4 / 3)


def M(l=0, t=0, r=0, b=0):
    """funcion auxiliar para crear márgenes de forma más cómoda"""
    return ft.Margin.only(left=l, top=t, right=r, bottom=b)


def P(l=0, t=0, r=0, b=0):
    """funcion auxiliar para crear padding de forma más cómoda"""
    return ft.Padding.only(left=l, top=t, right=r, bottom=b)


def borde(ancho, color):
    
    return ft.Border.all(ancho, color)


def A(x, y):
    """funcion auxiliar para crear alineaciones de forma más cómoda"""
    return ft.Alignment(x, y)

_ANCLA = {"w": A(-1, 0), "e": A(1, 0), "center": A(0, 0)}

def rgba(color, alfa_255):
    """Convierte un color hexadecimal en un color RGBA con opacidad."""
    return ft.Colors.with_opacity(alfa_255 / 255, color)


def Row(controls, spacing=0, **kw):
    """funcion auxiliar para crear un Row con alineación vertical centrada"""
    return ft.Row(controls=controls, spacing=spacing, **kw)


def Col(controls, spacing=0, **kw):
    """funcion auxiliar para crear un Column con alineación horizontal stretch"""
    kw.setdefault("horizontal_alignment", ft.CrossAxisAlignment.STRETCH)
    return ft.Column(controls=controls, spacing=spacing, **kw)


def T(texto, size=12, bold=False, color="#1A1A1A", italic=False, justify=None,
      familia=FONT, **kw):
    """funcion auxiliar para crear un Text con alineación y estilo de fuente"""
    return ft.Text(
        value=texto, size=size,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic, color=color,
        text_align=_JUST.get(justify), font_family=familia, **kw
    )


def lbl(texto, size=12, bold=False, color="#1A1A1A", anchor="center", height=28,
        width=None, justify=None, italic=False, m=None, familia=FONT):
    """Equivale a un CTkLabel (alto mínimo de 28 px, texto centrado en vertical).
    Usa height=None para textos multilínea o de fuente grande."""
    if justify is None:
        justify = {"w": "left", "e": "right"}.get(anchor, "center")
    return ft.Container(
        content=T(texto, size, bold, color, italic, justify, familia),
        height=height, width=width, alignment=_ANCLA[anchor], margin=m,
    )


def ctr(control, m=None):
    """funcion auxiliar para crear un Container con alineación centrada y margen opcional"""

    return ft.Container(content=control, alignment=A(0, 0), margin=m)


def esp(alto=0, ancho=None):
    """Frame vacío usado como separador/espaciador."""
    return ft.Container(height=alto, width=ancho)


def pil_img(imagen, ancho, alto, **kw):
    """funcion auxiliar para crear un ft.Image a partir de una imagen PIL, con tamaño fijo y fit=FILL"""
    return ft.Image(src=pil_to_base64(imagen), width=ancho, height=alto,
                    fit=ft.BoxFit.FILL, **kw)


def grad_barra(valor, color, fondo):
    """Barra de progreso con degradado"""
    v = max(0.0, min(1.0, valor))
    return ft.LinearGradient(
        begin=A(-1, 0), end=A(1, 0),
        colors=[color, color, fondo, fondo], stops=[0.0, v, v, 1.0],
    )


def barra_progreso(valor, alto, fondo, color, radio, ancho=None, **kw):
    """funcion auxiliar para crear un Container con un gradiente que simula una barra de progreso"""
    return ft.Container(
        width=ancho, height=alto, border_radius=radio,
        gradient=grad_barra(valor, color, fondo), **kw
    )


def refrescar(ctrl):
    """update() tolerante: ignora el caso de un control ya desmontado."""
    try:
        ctrl.update()
    except (RuntimeError, AssertionError):
        pass


def despues(page, ms, fn):
    """Equivale a widget.after(ms, fn)."""
    async def _esperar():
        await asyncio.sleep(ms / 1000)
        r = fn()
        if inspect.isawaitable(r):
            await r
    return page.run_task(_esperar)


async def enfocar(ctrl):
    """focus() es síncrono o asíncrono según la versión de Flet."""
    r = ctrl.focus()
    if inspect.isawaitable(r):
        await r


def msgbox(page, titulo, mensaje):
    """funcion auxiliar para mostrar un cuadro de diálogo modal con un mensaje y un botón Aceptar"""
    dlg = ft.AlertDialog(
        title=ft.Text(value=titulo), content=ft.Text(value=mensaje),
        actions=[ft.TextButton("Aceptar", on_click=lambda e: page.pop_dialog())],
    )
    page.show_dialog(dlg)

def btn(texto, comando=None, fg=None, hover=None, color="#FFFFFF", size=13, bold=False,
        familia=FONT, anchor="center", activo=True, color_off="#BDBDBD",
        height=28, radius=6, **kw):
    """Fábrica de Boton. Valores por defecto de: alto 28, radio 6."""
    b = Boton(height=height, border_radius=radius, **kw)
    return b._setup(texto, comando, fg, hover, color, size, bold, familia, anchor,
                    activo, color_off)

def _arte_precolombino(W=400, H=720, S=2):
    """Genera una ilustración de estilo precolombino, con un sol central, rayos, serpiente y rombos."""
    img = Image.new("RGB", (W * S, H * S), "#1A0A00")
    d = ImageDraw.Draw(img)

    def rect(x0, y0, x1, y1, fill):
        d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill)

    def oval(x0, y0, x1, y1, fill, outline=None, ancho=1):
        d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=outline,
                  width=ancho * S if outline else 0)

    def poli(pts, fill, outline=None, ancho=1):
        pts = [(x * S, y * S) for x, y in pts]
        d.polygon(pts, fill=fill)
        if outline:
            d.line(pts + [pts[0]], fill=outline, width=ancho * S, joint="curve")

    def linea(pts, fill, ancho):
        d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(ancho * S),
               joint="curve")

    colores_fondo = ["#1A0A00", "#200C00", "#260E00", "#2C1000", "#321200"]
    fila_h = H // len(colores_fondo)
    for i, col in enumerate(colores_fondo):
        rect(0, i * fila_h, W, (i + 1) * fila_h, col)
    rect(385, 0, 400, H, "#C8860A")
    for y in range(0, H, 40):
        rect(385, y, 400, y + 20, "#8B5E00")

    cx, cy = 200, 200
    for r, col in [(120, "#4A2800"), (100, "#6B3A00"), (80, "#8B5000"),
                   (60, "#C8860A"), (40, "#FFD700"), (20, "#FFF8DC")]:
        oval(cx - r, cy - r, cx + r, cy + r, col)

    num_rayos = 12
    for k in range(num_rayos):
        ang = math.radians(k * 360 / num_rayos)
        ang2 = math.radians(k * 360 / num_rayos + 15)
        poli([
            (cx + 125 * math.cos(ang), cy + 125 * math.sin(ang)),
            (cx + 125 * math.cos(ang2), cy + 125 * math.sin(ang2)),
            (cx + 145 * math.cos(ang + math.radians(7.5)),
             cy + 145 * math.sin(ang + math.radians(7.5))),
        ], "#C8860A", "#FFD700")
    oval(cx - 10, cy - 10, cx + 10, cy + 10, "#1A0A00")
    oval(cx - 5, cy - 5, cx + 5, cy + 5, "#FFFFFF")

    serpiente = []
    for t in range(0, 360, 5):
        r2 = 165 + 15 * math.sin(math.radians(t * 3))
        ang = math.radians(t)
        serpiente.append((cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)))
    linea(serpiente, "#228B22", 4)

    oval(175, 340, 225, 390, "#C8860A", "#FFD700", 2)
    linea([(200, 390), (200, 460)], "#C8860A", 4)
    linea([(160, 410), (240, 410)], "#C8860A", 4)
    linea([(200, 460), (170, 500)], "#C8860A", 4)
    linea([(200, 460), (230, 500)], "#C8860A", 4)
    for ang_p in range(-60, 61, 20):
        rad = math.radians(ang_p - 90)
        linea([(200, 340), (200 + 35 * math.cos(rad), 365 + 35 * math.sin(rad))], "#228B22", 2)

    def rombo(cx_, cy_, tam, relleno, borde_):
        poli([(cx_, cy_ - tam), (cx_ + tam, cy_), (cx_, cy_ + tam), (cx_ - tam, cy_)],
             relleno, borde_, 2)
        i = tam * 0.5
        poli([(cx_, cy_ - i), (cx_ + i, cy_), (cx_, cy_ + i), (cx_ - i, cy_)], borde_)

    rombo(80, 560, 55, "#C8860A", "#FFD700")
    rombo(320, 560, 55, "#8B5000", "#C8860A")

    espiral = []
    pasos = 200
    for i in range(pasos):
        t = 3 * 2 * math.pi * i / pasos
        r = 50 * i / pasos
        espiral.append((200 + r * math.cos(t), 620 + r * math.sin(t)))
    linea(espiral, "#FFD700", 3)

    # greca superior
    rect(10, 10, W - 15, 70, "#8B5000")
    x = 10
    while x < W - 15:
        rect(x, 12, x + 20, 32, "#C8860A")
        rect(x + 5, 17, x + 15, 27, "#8B5000")
        x += 30

    return img.resize((W, H), _LANCZOS)


def _imagen_timer(segundos, color_arco, W=80, S=4):
    """Disco del cronómetro: círculo oscuro + sector que representa el tiempo restante."""
    img = Image.new("RGBA", (W * S, W * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4 * S, 4 * S, (W - 4) * S, (W - 4) * S], fill="#1A0A00",
              outline="#555555", width=2 * S)
    frac = max(0.0, min(1.0, segundos / TIEMPO_INICIAL))
    caja = [8 * S, 8 * S, (W - 8) * S, (W - 8) * S]
    if frac >= 1.0:
        d.ellipse(caja, fill=color_arco)
    elif frac > 0:
        d.pieslice(caja, start=-90, end=-90 + 360 * frac, fill=color_arco)
    return img.resize((W, W), _LANCZOS)

def interruptor(estado=True, comando=None):
    return Interruptor()._setup(estado, comando)


