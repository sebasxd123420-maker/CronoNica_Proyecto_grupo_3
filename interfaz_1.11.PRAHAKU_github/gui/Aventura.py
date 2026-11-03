import flet as ft
import flet as ft
from datos import (
    img as ruta_img,
    COLOR_OSCURO
)
from funciones import make_avatar
from funciones import Col, Row, esp,pil_img
from funciones import  lbl, M, T, A, ctr, btn, P
from entidades import  EventoHistorico, PersonajeClave, DatoHistorico
# =====================================================================
# PANTALLA DE AVENTURA
# =====================================================================
@ft.control
class AventuraScreen(ft.Column):
    

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
        self.controls = [
            self._build_header(),
            self._build_body(),
            self._build_navigation(),
        ]

    # ──────────────────────────────────────────────────────
    def _build_header(self):
        
        chips = Row([
            ft.Container(
                bgcolor=chip_fg, border_radius=8, margin=M(l=4, r=4), height=38,
                padding=P(l=10, r=10), alignment=A(0, 0),
                content=T(chip_txt, 10, True, "#80CBC4"),
            )
            for chip_txt, chip_fg in [("Acto 2 / 5", "#0A3A3B"), ("42% completado", "#1A5E5A")]
        ])
        return ft.Container(
            height=90, bgcolor="#4A1525", border_radius=16, margin=M(b=12),
            content=Row([
                # Barra de acento izquierda
                ft.Container(width=6, height=70, bgcolor="#0E9A91", border_radius=8,
                             margin=M(l=14, r=10)),
                ft.Column(
                    controls=[
                        lbl("Capítulo 3  ·  La Independencia de Centroamérica", 20, True,
                            "#FFFFFF", anchor="w", height=None),
                        lbl("🗓 15 de Septiembre de 1821  ·  Ciudad de Guatemala", 12,
                            color="#B39DDB", anchor="w", m=M(t=2)),
                    ],
                    spacing=0, expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(content=chips, margin=M(l=16, r=16)),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        )

    # ──────────────────────────────────────────────────────
    def _build_body(self):
        # ── Columna izquierda: historia + timeline ──
        img_frame = ft.Container(
            bgcolor="#1A0A10", border_radius=14, margin=M(b=12),
            content=Col([
                ctr(ft.Image(src=ruta_img("cap3.png"), width=600, height=240,
                             fit=ft.BoxFit.FILL), M(l=8, t=8, r=8, b=8)),
                lbl("🖼  La firma del Acta de Independencia Centroamericana, 1821", 10,
                    color="#B39DDB", italic=True, m=M(b=8)),
            ]),
        )

        story_text = (
            "El 15 de septiembre de 1821, en el Palacio Real de la Ciudad de Guatemala, "
            "representantes de las provincias centroamericanas se reunieron para deliberar "
            "sobre el futuro de la región. Tras intensas negociaciones, firmaron el Acta de "
            "Independencia que liberaba a Centroamérica del dominio español.\n\n"
            "Nicaragua, junto a Guatemala, El Salvador, Honduras y Costa Rica, se convertía "
            "en nación libre. Sin embargo, los desafíos apenas comenzaban: ¿quiénes serían "
            "los nuevos líderes? ¿Cómo se organizaría el nuevo Estado?"
        )
        narrative = ft.Container(
            bgcolor="#1E1E2E", border_radius=14, margin=M(b=12),
            content=Col([
                lbl("⚔️  Acto 2: La Firma del Acta", 15, True, "#FFD700", anchor="w",
                    m=M(l=18, r=18, t=14, b=4)),
                ft.Container(
                    margin=M(l=18, r=18, b=14),
                    # wraplength=560
                    content=Row([ft.Container(
                        width=560,
                        content=T(story_text, 12, color="#C8D0DC", justify="left"))]),
                ),
            ]),
        )

        events = [
            EventoHistorico("1811", "🔔", "Primer Grito de Independencia en El Salvador", True,  "#0E9A91"),
            EventoHistorico("1820", "⚔️", "Levantamientos en toda Centroamérica",          False, "#4A1525"),
            EventoHistorico("1821", "✍️", "Firma del Acta de Independencia",               True,  "#FFD700"),
            EventoHistorico("1823", "🏛️", "Creación de las Provincias Unidas",             False, "#1A5E5A"),
        ]
        filas_ev = [
            ft.Container(
                bgcolor="#1A4A4B" if ev.destacado else None, border_radius=10,
                margin=M(l=14, r=14, t=3, b=3),
                content=Row([
                    ft.Container(width=12, height=12, bgcolor=ev.color, border_radius=10,
                                 margin=M(l=10, r=8, t=12, b=12)),
                    lbl(ev.fecha, 11, True, ev.color, width=38),
                    lbl(ev.icono, 16, m=M(l=4, r=6)),
                    lbl(ev.descripcion, 11,
                        color="#FFFFFF" if ev.destacado else "#80CBC4", m=M(t=12, b=12)),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )
            for ev in events
        ]
        tl_frame = ft.Container(
            bgcolor="#0A2223", border_radius=14,
            content=Col([
                lbl("📅  Línea de tiempo", 14, True, "#0E9A91", anchor="w",
                    m=M(l=18, r=18, t=12, b=8)),
                *filas_ev,
                esp(8),
            ]),
        )
        left = ft.Container(content=Col([img_frame, narrative, tl_frame]),
                            expand=6, margin=M(r=12))

        # ── Columna derecha: personajes + datos + quiz ──
        characters = [
            PersonajeClave("GM", "#1C3A6E", "#87CEEB", "Gabino Gaínza",     "Capitán General,\nlíder de la firma"),
            PersonajeClave("JC", "#8B1A1A", "#FF8A65", "José Cecilio",      "Prócer hondureño,\nfirmante del Acta"),
            PersonajeClave("MP", "#1A5E1A", "#81C784", "Miguel Larreynaga", "Representante\nde Nicaragua"),
        ]
        filas_pj = [
            ft.Container(
                bgcolor="#2A1030", border_radius=10, margin=M(l=12, r=12, t=4, b=4),
                content=Row([
                    ft.Container(
                        content=pil_img(make_avatar(pj.iniciales, pj.color_fondo,
                                                    pj.color_texto, 48), 48, 48),
                        margin=M(l=10, r=8, t=8, b=8)),
                    ft.Column(
                        controls=[
                            lbl(pj.nombre, 12, True, "#FFFFFF", anchor="w"),
                            lbl(pj.rol, 10, color="#B39DDB", anchor="w", height=None,
                                justify="left"),
                        ],
                        spacing=0, tight=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )
            for pj in characters
        ]
        chars_card = ft.Container(
            bgcolor="#1A0A20", border_radius=14, margin=M(b=12),
            content=Col([
                lbl("👥  Personajes clave", 13, True, "#FFE57F", anchor="w",
                    m=M(l=14, r=14, t=12, b=6)),
                *filas_pj,
                esp(8),
            ]),
        )

        datos_historicos = [
            DatoHistorico("📅", "Fecha", "15 Sep 1821"),
            DatoHistorico("📍", "Lugar", "Guatemala"),
            DatoHistorico("✍️", "Firmantes", "22 personas"),
            DatoHistorico("🌎", "Territorio", "~500,000 km²"),
        ]
        filas_datos = [
            ft.Container(
                bgcolor="#0A3A3B", border_radius=8, margin=M(l=12, r=12, t=3, b=3),
                content=Row([
                    lbl(dato.icono + "  " + dato.etiqueta, 11, color="#80CBC4",
                        m=M(l=10, r=10, t=7, b=7)),
                    lbl(dato.valor, 11, True, "#FFFFFF", m=M(r=10)),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )
            for dato in datos_historicos
        ]
        data_card = ft.Container(
            bgcolor="#062A2B", border_radius=14, margin=M(b=12),
            content=Col([
                lbl("📊  Datos históricos", 13, True, "#0E9A91", anchor="w",
                    m=M(l=14, r=14, t=12, b=6)),
                *filas_datos,
                esp(8),
            ]),
        )

    
        right = ft.Container(content=Col([chars_card, data_card]), expand=4)

        return Row([left, right], vertical_alignment=ft.CrossAxisAlignment.START)

    # ──────────────────────────────────────────────────────
    def _build_navigation(self):
        actos = [
            ("Acto 1\nPrólogo",          True,  True),
            ("Acto 2\nLa firma",         True,  False),
            ("Acto 3\nLas juntas",       False, False),
            ("Acto 4\nCelebración",      False, False),
            ("Acto 5\nLa nueva nación",  False, False),
        ]
        pills = []
        for label, done, current in actos:
            if current:
                bg, tc = "#0E9A91", "#FFFFFF"
            elif done:
                bg, tc = "#1E4D4A", "#80CBC4"
            else:
                bg, tc = "#0A2223", "#546E7A"
            pills.append(ft.Container(
                expand=1, height=38, bgcolor=bg, border_radius=8, margin=M(l=3, r=3),
                alignment=A(0, 0), content=T(label, 8, True, tc, justify="center"),
            ))

        return ft.Container(
            height=65, bgcolor=COLOR_OSCURO, border_radius=16, margin=M(b=8),
            content=Row([
                btn("← Acto anterior", None, fg="#0A3A3B", hover="#0E4A4B", color="#80CBC4",
                    size=11, bold=True, height=36, radius=10, width=140,
                    margin=M(l=16, t=14, r=16, b=14)),
                ft.Container(content=Row(pills), expand=True, margin=M(l=8, r=8)),
                btn("Acto siguiente →", None, fg="#0E9A91", hover="#0A7A73", size=11,
                    bold=True, height=36, radius=10, width=140,
                    margin=M(l=16, t=14, r=16, b=14)),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        )
