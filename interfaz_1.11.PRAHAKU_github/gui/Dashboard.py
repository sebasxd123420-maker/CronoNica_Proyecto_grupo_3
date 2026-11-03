import flet as ft
import flet as ft
from gui.Quiz import QuizRapido
from datos import (
    img as ruta_img,
)

from funciones import (
    make_map_slot_image, make_user_avatar, make_historia_image
)
from funciones import Col, Row, rgba,  esp, pil_img
from funciones import barra_progreso, lbl, M, T, A,  ctr, btn, borde, P
from entidades import Insignia, LogroReciente
# =====================================================================
# DASHBOARD PRINCIPAL
# =====================================================================
@ft.control
class DashboardScreen(ft.Column):
    """pantalla principal del dashboard: contiene el banner, el mapa de capítulos, estadísticas, historia del día, logros recientes, perfil y quiz diario."""

    @classmethod
    def crear(cls, controller):
        pantalla = cls()
        pantalla._controller = controller
        return pantalla

    def init(self):
        self.expand = True
        self.spacing = 0
        self.scroll = ft.ScrollMode.AUTO
        self._controller = None

        left = Col([])
        self._build_banner(left)
        self._build_chapter(left)
        self._build_map(left)
        self._build_bottom(left)

        right = Col([])
        self._build_profile(right)
        self._build_quiz(right)

        # grid: columnas con weight 7 y 3; la izquierda con padx=(0, 14)
        self.controls = [Row([
            ft.Container(content=left, expand=7, margin=M(r=14)),
            ft.Container(content=right, expand=3),
        ], vertical_alignment=ft.CrossAxisAlignment.START)]

    def _ir(self, nombre):
        return lambda: self._controller.show_frame(nombre)

    # ──────────────────────────────────────────────────────
    def _build_banner(self, parent):
        # Imagen (centrada y recortada, como el label de 900x205 original) + sombreado
        # izquierdo (alfa 220 → 0 en la primera mitad) + textos + botones.
        sombra = rgba("#062A2B", 220)
        sin_sombra = rgba("#062A2B", 0)
        capas = [
            ft.Image(src=ruta_img("banner.png"), fit=ft.BoxFit.COVER,
                     left=0, top=0, right=0, bottom=0),
            ft.Container(
                left=0, top=0, right=0, bottom=0,
                gradient=ft.LinearGradient(
                    begin=A(-1, 0), end=A(1, 0),
                    colors=[sombra, sin_sombra, sin_sombra], stops=[0.0, 0.5, 1.0]),
            ),
            # Texto lado izquierdo (antes dibujado con ImageDraw)
            T("¡Bienvenido de nuevo", 24, True, "#FFFFFF", left=160, top=22),
            T("Explorador!, ¡HOLA!", 24, True, "#FFFFFF", left=160, top=50),
            T("Continua tu aventura", 14, color="#FFFFFF", left=160, top=75),
            T("Por la historia de Nicaragua", 14, color="#FFFFFF", left=160, top=93),
            T("¡Hoy es un gran día para aprender!", 14, color="#FFFFFF", left=160, top=111),
            # Botones encima del banner
            Row([
                btn("▶  Continuar aventura", self._ir("Aventura"), fg="#0E9A91",
                    hover="#0A7A73", size=10, bold=True, height=38, radius=10, width=140,
                    margin=M(r=10)),
                 btn("📖  Ver biblioteca", self._ir("Biblioteca"), fg="#1A5E5A", hover="#1E7A74", size=12,
                    bold=True, height=38, radius=10, width=140),
                btn("🏺  Comenzar Quiz", self._ir("QuizPrecolombino"), fg="#FF9500",
                    hover="#CC7700", size=11, bold=True, height=38, radius=10, width=140,
                    margin=M(l=10)),
            ], tight=True, left=26, top=155),
        ]
        parent.controls.append(ft.Container(
            height=205, margin=M(b=14), clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Stack(controls=capas),
        ))

    # ──────────────────────────────────────────────────────
    def _build_chapter(self, parent):
        ch_img = ft.Image(src=ruta_img("cap3.png"), width=110, height=90, fit=ft.BoxFit.FILL)

        # Chips de info
        chips = Row([
            ft.Container(
                bgcolor=chip_color, border_radius=8, height=34, margin=M(r=6),
                padding=P(l=8, r=8), alignment=A(0, 0),
                content=T(chip_text, 10, True, "#FFFFFF"),
            )
            for chip_text, chip_color in [("📖 Capítulo 3", "#0E9A91"),
                                          ("⚔️ Independencia", "#4A1525"),
                                          ("★ 4.8", "#7A6A1A")]
        ])

        derecha = Col([
            ft.Container(content=chips, margin=M(r=16, t=14, b=2)),
            lbl("La Independencia de Centroamérica (1821)", 15, True, "#FFFFFF",
                anchor="w", m=M(r=16)),
            lbl("Explora los eventos que llevaron a la independencia de\n"
                "Centroamérica del Imperio Español.",
                11, color="#8A9BB0", anchor="w", height=None, justify="left",
                m=M(r=16, b=14)),
        ], horizontal_alignment=ft.CrossAxisAlignment.START)

        # Barra de progreso del capítulo
        prog = ft.Container(
            margin=M(l=16, r=16, b=14),
            content=Row([
                lbl("Progreso:", 11, True, "#8A9BB0", m=M(r=10)),
                ft.Container(expand=True,
                             content=barra_progreso(0.42, 10, "#2A2A3E", "#0E9A91", 6)),
                lbl("42%", 11, True, "#0E9A91", m=M(l=10)),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        )

        parent.controls.append(ft.Container(
            bgcolor="#1E1E2E", border_radius=16, margin=M(b=14),
            content=Col([
                Row([
                    ft.Container(content=ch_img, margin=M(l=16, t=14, r=16, b=14)),
                    ft.Container(content=derecha, expand=True),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                prog,
            ]),
        ))

    # ──────────────────────────────────────────────────────
    def _build_map(self, parent):
        """Mapa de viaje de capítulos."""
        chapters = [
            (1, "🌿 Precolombino",  "Civilizaciones\noriginarias", False, False),
            (2, "⛪ Colonial",       "El período\nespañol",         False, False),
            (3, "⚔️ Independencia", "La firma del\nActa de 1821",  True,  False),
            (4, "🏛️ República",     "Los primeros\naños libres",   False, True),
            (5, "🔫 Revolución",    "El siglo XX\nnicaragüense",   False, True),
            (6, "🏙️ Modernidad",   "Nicaragua\nhoy",              False, True),
        ]

        slots = []
        for ch_num, title, subtitle, current, locked in chapters:
            slot_img = make_map_slot_image(95, 85, chapter_num=ch_num, locked=locked)
            contenido = [
                ctr(pil_img(slot_img, 95, 85), M(t=10, b=4)),
                lbl(title, 10, True, "#FFFFFF" if not locked else "#546E7A"),
                lbl(subtitle, 8, color="#80CBC4" if not locked else "#37474F",
                    justify="center", m=M(t=2, b=8)),
            ]
            if locked:
                contenido.append(lbl("🔒", 14, color="#546E7A", m=M(b=8)))
            elif current:
                contenido.append(btn(
                    "▶ Continuar", self._ir("Aventura"), fg="#0E9A91", hover="#0A7A73",
                    size=9, bold=True, height=26, radius=8, margin=M(l=8, r=8, b=10)))

            slots.append(ft.Container(
                expand=1, margin=M(l=8, r=8, t=12, b=12),
                bgcolor="#1A4A4B" if current else ("#0A2223" if locked else "#102E2F"),
                border_radius=12,
                border=borde(2 if current else 1,
                             "#0E9A91" if current else ("#0A2223" if locked else "#1A4A4B")),
                content=Col(contenido),
            ))

        parent.controls.append(ft.Container(margin=M(b=14), content=Col([
            lbl("🗺️  Mapa de Aventura", 16, True, "#1A1A1A", anchor="w", m=M(b=8)),
            ft.Container(bgcolor="#0A2223", border_radius=16, content=Row(slots)),
        ])))

    # ──────────────────────────────────────────────────────
    def _build_bottom(self, parent):
        """Fila de cards: Estadísticas, Historia del día, Logros recientes.
        (El grid original estiraba las tres cards a la misma altura: 256 px.)"""
        ALTO = 256

        # ── Stats ──
        stats = [("🏅 XP Total", "2 450"), ("🔥 Racha", "7 días"),
                 ("✅ Capítulos", "2 / 6"), ("⭐ Estrellas", "14 / 30")]
        filas = [
            ft.Container(
                margin=M(l=14, r=14, t=2, b=2),
                content=Row([lbl(label, 11, color="#80CBC4"), lbl(val, 11, True, "#FFFFFF")],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            )
            for label, val in stats
        ]
        stats_card = ft.Container(
            expand=1, height=ALTO, margin=M(r=10), bgcolor="#062A2B", border_radius=14,
            content=Col([
                lbl("📊 Estadísticas", 13, True, "#0E9A91", anchor="w", m=M(l=14, r=14, t=12, b=6)),
                *filas,
                esp(10),
            ]),
        )

        # ── Historia del día ──
        hist_card = ft.Container(
            width=310, height=ALTO, margin=M(l=5, r=5), bgcolor="#1A0A20", border_radius=14,
            content=Col([
                ctr(pil_img(make_historia_image(310, 220), 290, 130), M(l=10, r=10, t=10, b=6)),
                lbl("📜 Historia del día", 13, True, "#FFD700", anchor="w", m=M(l=14, r=14)),
                lbl("La firma del Acta de Independencia\nCentroamericana, 15 Sep 1821.",
                    10, color="#D4B8A0", anchor="w", justify="left", m=M(l=14, r=14, t=4)),
                ft.Container(
                    alignment=A(-1, 0), margin=M(l=14, r=14, t=8, b=12),
                    content=btn("Leer más →", None, fg="#4A1525", hover="#6A1535",
                                color="#FFD700", size=10, bold=True, height=30, radius=8,
                                width=140),
                ),
            ]),
        )

        # ── Logros recientes ──
        logros = [
            LogroReciente("🥇", "Primer capítulo", "#FFD700", "#A37500"),
            LogroReciente("📖", "Lector ávido",    "#0E9A91", "#1B9A9C"),
            LogroReciente("⭐", "Racha de 7 días", "#FF9500", "#985503"),
        ]
        filas_logros = [
            ft.Container(
                bgcolor=logro.color_fondo, border_radius=10, margin=M(l=14, r=14, t=4, b=4),
                content=Row([
                    lbl(logro.icono, 20, m=M(l=10, r=8, t=8, b=8)),
                    lbl(logro.nombre, 9, True, "#FFFFFF", m=M(t=8, b=8)),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )
            for logro in logros
        ]
        logros_card = ft.Container(
            expand=1, height=ALTO, margin=M(l=10), bgcolor="#1A2030", border_radius=14,
            content=Col([
                lbl("🏆 Logros recientes", 13, True, "#FFE57F", anchor="w", m=M(l=14, r=14, t=12, b=6)),
                *filas_logros,
                esp(10),
            ]),
        )

        parent.controls.append(Row([stats_card, hist_card, logros_card],
                                   vertical_alignment=ft.CrossAxisAlignment.START))

    # ──────────────────────────────────────────────────────
    def _build_profile(self, parent):
        # Badges
        badge_data = [
            Insignia("🏅", "#FFD700", "#896304"),
            Insignia("⭐", "#0E9A91", "#188688"),
            Insignia("🔥", "#FF6B35", "#873F03"),
            Insignia("📖", "#6B3AC0", "#5622A3"),
        ]
        badges = Row([
            ft.Container(
                width=48, height=48, bgcolor=ins.color_fondo, border_radius=10,
                margin=M(l=4, r=4), alignment=A(0, 0), content=T(ins.icono, 20),
            )
            for ins in badge_data
        ], alignment=ft.MainAxisAlignment.CENTER)

        parent.controls.append(ft.Container(
            bgcolor="#FFFFFF", border_radius=16, border=borde(1, "#E0E0E0"), margin=M(b=14),
            content=Col([
                ctr(pil_img(make_user_avatar(68), 68, 68), M(t=16, b=4)),
                lbl("Ana García", 15, True, "#1A1A1A"),
                lbl("Exploradora Nivel 5", 11, color="#0E9A91", m=M(t=2, b=10)),
                # Barra de nivel
                ft.Container(
                    margin=M(l=18, r=18, b=4),
                    content=Row([lbl("Nivel 5", 10, True, "#1A1A1A"),
                                 lbl("2 450 / 3 000 XP", 10, color="#888888")],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ),
                ft.Container(margin=M(l=18, r=18, b=14),
                             content=barra_progreso(0.82, 8, "#E0E0E0", "#0E9A91", 6)),
                ft.Container(content=badges, margin=M(b=12)),
            ]),
        ))

    # ──────────────────────────────────────────────────────
    def _build_quiz(self, parent):
        """Widget del quiz diario."""
        self.quiz_card = QuizRapido()._setup(
            16, "Quiz \ndel día", 10,
            "¿Cuándo ocurrió la \n independencia de Centroamérica?", 12)
        parent.controls.append(self.quiz_card)
