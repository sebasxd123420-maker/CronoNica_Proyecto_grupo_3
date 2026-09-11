from PIL import Image, ImageDraw, ImageFont
import math
import os
from datos import IMG_DIR
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


def make_logo(size=62):
    ruta_logo = os.path.join(IMG_DIR, "logo.png")
    img = Image.open(ruta_logo).convert("RGBA")
    img = img.resize((size, size))

    return img


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
    """Fondo ilustrado para la pantalla de login."""
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

    # Bandera estilizada arriba izquierda
    bandera = Image.open(os.path.join(IMG_DIR, "bandera.png")).convert("RGBA")
    bandera = bandera.resize((100, 60))
    img.paste(bandera, (30, 40), bandera)

    return img


