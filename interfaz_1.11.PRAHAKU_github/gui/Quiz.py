import flet as ft
import asyncio
import random
import flet as ft

from datos import (
    COLOR_TEAL, PREGUNTAS, Pregunta, TIEMPO_INICIAL,
    COLOR_OPCION_BG, COLOR_OPCION_HOVER, COLOR_OPCION_BORDE, COLOR_TEXTO_OPC,
    COLOR_TIMER_OK, COLOR_TIMER_WARN, COLOR_TIMER_DANGER, COLOR_CORRECTO, COLOR_INCORRECTO,
    COLOR_TITULO, COLOR_PANEL, COLOR_PREGUNTA,
)
from entidades import OpcionQuiz
from funciones import lbl, M, T, A, ctr, btn, borde, P, refrescar, Row, Col, px, _imagen_timer, _arte_precolombino, pil_img
# =====================================================================
# QUIZ RÁPIDO (tarjeta compartida por Dashboard y Aventura)
# En el original eran dos copias idénticas salvo radio, títulos y tamaños de fuente.
# =====================================================================
@ft.control
class QuizRapido(ft.Container):
    """Widget del quiz diario / pregunta del acto."""

    def _setup(self, radio, titulo, titulo_size, pregunta, pregunta_size):
        self.bgcolor = "#2D1040"
        self.border_radius = radio
        self._seleccion = ""          
        self._respondido = False      
        from funciones import make_quiz_deco
        # Header del quiz
        deco = pil_img(make_quiz_deco(80, 80), 80, 80)
        qhdr = ft.Container(
            bgcolor="#3D1A58", border_radius=12, margin=M(l=16, r=16, t=14, b=8),
            content=Row([
                ft.Container(content=deco, margin=M(l=10, r=10, t=6, b=6)),
                ft.Column(
                    controls=[
                        lbl(titulo, titulo_size, True, "#FFE57F", anchor="w",
                            height=None if "\n" in titulo else 28),
                        lbl("Responde y gana XP", 10, color="#B39DDB", anchor="w"),
                    ],
                    spacing=0, expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    bgcolor="#7A6A1A", border_radius=8, margin=M(l=12, r=12),
                    height=36, padding=P(l=8, r=8), alignment=A(0, 0),
                    content=T("⭐ +50 XP", 10, True, "#FFE57F"),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        )

        # Opciones
        self.option_buttons = {}
        opciones = [
            OpcionQuiz("A", "1821", True),
            OpcionQuiz("B", "1990", False),
            OpcionQuiz("C", "1512", False),
            OpcionQuiz("D", "1856", False),
        ]
        celdas = []
        for opcion in opciones:
            badge = ft.Container(
                width=30, height=30, bgcolor="#6A1535", border_radius=8,
                alignment=A(0, 0), margin=M(r=10),
                content=T(opcion.letra, 12, True, "#FFFFFF"),
            )
            frame = ft.Container(
                expand=1, margin=6, bgcolor="#4A1525", border_radius=12,
                border=borde(1, "#6A1535"), padding=P(l=12, t=10, r=12, b=10),
                on_click=lambda e, l=opcion.letra: self._select_answer(l),
                content=Row([badge, T(opcion.texto, 13, True, "#FFFFFF")],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER),
            )
            self.option_buttons[opcion.letra] = (frame, badge, opcion)
            celdas.append(frame)

        # Botón confirmar
        self.confirm_btn = btn(
            "Confirmar respuesta", self._confirm_answer, fg=COLOR_TEAL, hover="#0A7A73",
            size=13, bold=True, height=40, radius=10, activo=False,
            margin=M(l=16, r=16, b=8),
        )
        self.feedback_frame = Col([])

        self.content = Col([
            qhdr,
            lbl(pregunta, pregunta_size, True, "#FFFFFF", anchor="w", height=None,
                justify="left", m=M(l=20, r=20, t=14, b=10)),
            ft.Container(
                margin=M(l=16, r=16, b=16),
                content=Col([Row(celdas[0:2]), Row(celdas[2:4])]),
            ),
            self.confirm_btn,
            ft.Container(content=self.feedback_frame, margin=M(l=16, r=16, b=12)),
        ])
        return self

    def _select_answer(self, letter):
        if self._respondido:
            return
        self._seleccion = letter
        for l, (frame, badge, opcion) in self.option_buttons.items():
            if l == letter:
                frame.bgcolor = "#1A5A55"
                frame.border = borde(1, "#0E9A91")
                badge.bgcolor = "#0E9A91"
            else:
                frame.bgcolor = "#4A1525"
                frame.border = borde(1, "#6A1535")
                badge.bgcolor = "#6A1535"
        self.confirm_btn.configurar(activo=True)
        self.update()

    def _confirm_answer(self):
        if self._respondido:
            return
        self._respondido = True
        chosen = self._seleccion
        self.confirm_btn.configurar(texto="✔ Respondido", activo=False)

        correct_letter = next(l for l, (_, _, o) in self.option_buttons.items() if o.es_correcta)
        is_correct = (chosen == correct_letter)

        for l, (frame, badge, opcion) in self.option_buttons.items():
            if l == correct_letter:
                frame.bgcolor = "#1B5E20"
                frame.border = borde(1, "#4CAF50")
                badge.bgcolor = "#2E7D32"
            elif l == chosen and not is_correct:
                frame.bgcolor = "#7A1515"
                frame.border = borde(1, "#F44336")
                badge.bgcolor = "#C62828"

        if is_correct:
            fb = ft.Container(
                bgcolor="#1B5E20", border_radius=12, margin=M(t=4, b=4),
                padding=P(l=14, t=8, r=14, b=8),
                content=T("✅  ¡Correcto! La independencia se proclamó el 15 de septiembre de 1821.",
                          11, True, "#A5D6A7", justify="left"),
            )
        else:
            fb = ft.Container(
                bgcolor="#7A1515", border_radius=12, margin=M(t=4, b=4),
                padding=P(l=14, t=8, r=14, b=8),
                content=T("❌  Incorrecto. La respuesta correcta es A) 1821.",
                          11, True, "#FFCDD2", justify="left"),
            )
        self.feedback_frame.controls = [
            fb,
            btn("Continuar →  Acto 3: Los primeros años de la República", None,
                fg=COLOR_TEAL, hover="#0A7A73", size=12, bold=True, height=38, radius=10,
                margin=M(t=6)),
        ]
        self.update()



# =====================================================================
# QUIZ PRECOLOMBINO
# =====================================================================
@ft.control
class QuizPrecolombino(ft.Container):
    """pantalla de quiz precolombino"""

    @classmethod
    def crear(cls, controller):
        pantalla = cls()
        pantalla._controller = controller
        return pantalla

    def init(self):
        self.bgcolor = "#1A0A00"
        self.expand = True
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self._controller = None

        self.pregunta_actual = 0
        self.puntaje = 0
        self.tiempo_restante = TIEMPO_INICIAL
        self.respondiendo = False
        self._gen_timer = 0        # antes timer_id
        self._gen_feedback = 0     # antes feedback_id

        self._preparar_preguntas()
        self._crear_widgets()

    # Se llama cada vez que se entra a esta pantalla
    def on_show(self):
        self._cancelar_cronometro()
        self._gen_feedback += 1
        self.frame_final.visible = False
        self._ocultar_feedback(actualizar=False)
        self.pregunta_actual = 0
        self.puntaje = 0
        self._preparar_preguntas()
        self._mostrar_pregunta()

    def _preparar_preguntas(self):
        self._preguntas_mezcladas = []
        for q in PREGUNTAS:
            indices = list(range(len(q.opciones)))
            random.shuffle(indices)
            nuevas_opciones = [q.opciones[i] for i in indices]
            nueva_correcta = indices.index(q.correcta)
            self._preguntas_mezcladas.append(
                Pregunta(
                    pregunta=q.pregunta,
                    opciones=nuevas_opciones,
                    correcta=nueva_correcta,
                )
            )

    def _crear_widgets(self):
        # ── Arte lateral (antes tk.Canvas 400x720 en x=0, y=0) ──
        self.canvas_img = pil_img(_arte_precolombino(), 400, 720, left=0, top=0)
        texto_arte = ft.Container(
            left=0, bottom=10, width=400, alignment=A(0, 0),
            content=T("Nicaragua Ancestral", px(11), italic=True, color="#C8860A",
                      familia="Georgia"),
        )

        # ── Barra superior con botón de volver ──
        btn_volver = btn(
            "← Volver al inicio", self._volver_inicio, fg=COLOR_OPCION_BG, hover=None,
            color="white", size=px(11), bold=True, height=None, radius=0,
            padding=P(l=12, t=5, r=12, b=5),
        )
        top_bar = ft.Container(margin=M(l=20, r=20, t=14), content=Row([btn_volver]))

        lbl_titulo = ft.Container(
            margin=M(t=6, b=2), alignment=A(0, 0),
            content=T("🏺  QUIZ PRECOLOMBINO DE NICARAGUA  🏺", px(15), True, COLOR_TITULO,
                      familia="Georgia"),
        )
        sep = ctr(ft.Container(expand=True, height=3, bgcolor=COLOR_OPCION_BORDE))

        # ── Fila de info: número, puntaje y cronómetro ──
        self.lbl_numero = T("Pregunta 1 / 7", px(12), True, COLOR_PREGUNTA)
        self.lbl_score = T("Puntaje: 0", px(12), True, COLOR_TITULO)
        self.timer_img = pil_img(_imagen_timer(TIEMPO_INICIAL, COLOR_TIMER_OK), 80, 80,
                                 gapless_playback=True)
        self.timer_txt = T(str(TIEMPO_INICIAL), px(18), True, "white")
        self.canvas_timer = ft.Stack(
            controls=[
                self.timer_img,
                ft.Container(left=0, top=0, right=0, bottom=0, alignment=A(0, 0),
                             content=self.timer_txt),
            ],
            width=80, height=80,
        )
        fila_info = ft.Container(
            margin=M(l=30, r=30, t=10),
            content=Row([
                self.lbl_numero,
                ft.Container(content=self.lbl_score, margin=M(l=30, r=30)),
                ft.Container(expand=True),
                ft.Container(content=self.canvas_timer, margin=M(l=10, r=10)),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        )

        # ── Pregunta ──
        self.lbl_pregunta = T("", px(17), True, COLOR_PREGUNTA, justify="center",
                              familia="Georgia")
        lbl_pregunta = ft.Container(
            margin=M(t=10, b=10), alignment=A(0, 0),
            content=ft.Container(content=self.lbl_pregunta),   # wraplength=800
        )

        # ── Opciones ──
        self.botones = []
        for i in range(3):
            b = btn(
                "", lambda idx=i: self._seleccionar_opcion(idx),
                fg=COLOR_OPCION_BG, hover=COLOR_OPCION_HOVER, color=COLOR_TEXTO_OPC,
                size=px(13), bold=True, height=50, radius=8, color_off="#A3A3A3",
                border=borde(2, COLOR_OPCION_BORDE), margin=M(t=4, b=4),
            )
            self.botones.append(b)
        self.frame_opciones = ft.Container(margin=M(l=40, r=40), content=Col(self.botones))

        self.panel = ft.Container(
            bgcolor=COLOR_PANEL, expand=True,
            content=ft.Column(
                controls=[top_bar, lbl_titulo, sep, fila_info, lbl_pregunta, self.frame_opciones],
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
            ),
        )

        # ── Overlay de feedback sobre el panel (place x=0,y=0 dentro del panel) ──
        self.lbl_feedback = T("", px(52), True, "white", justify="center", familia="Georgia")
        self.frame_feedback = ft.Container(
            bgcolor=COLOR_CORRECTO, visible=False, expand=True,
            alignment=A(0, 0), content=self.lbl_feedback,
        )

        # ── Pantalla final (1280 x 720) ──
        self.lbl_final = T("", px(30), True, COLOR_TITULO, justify="center", familia="Georgia")
        self.btn_reiniciar = btn(
            "🔄  Jugar de nuevo", self._reiniciar, fg=COLOR_OPCION_BG, hover=None,
            color="white", size=px(16), bold=True, height=55, radius=0, width=260,
            left=640 - 130, top=468 - 27.5,
        )
        btn_volver_final = btn(
            "← Volver al inicio", self._volver_inicio, fg=COLOR_OPCION_BG, hover=None,
            color="white", size=px(13), bold=True, height=44, radius=0, width=220,
            left=640 - 110, top=561.6 - 22,
        )

        self.frame_final = ft.Container(
            bgcolor="#1A0A00", visible=False, expand=True,
            content=ft.Stack(
                controls=[
                    ft.Container(
                    alignment=A(0, 0), content=self.lbl_final, expand=True),
                    self.btn_reiniciar,
                    btn_volver_final,
                ],
                expand=True
            ),
        )

        # Crear una fila responsiva para la vista principal
        vista_principal = ft.Row(
            controls=[
                ft.Stack([self.canvas_img, texto_arte], width=400),
                self.panel
            ],
            expand=True,
            spacing=0
        )

        # Envolver todo en un Stack que se expanda al tamaño de la ventana
        self.content = ft.Stack(
            controls=[vista_principal, self.frame_feedback, self.frame_final],
            expand=True,
        )

    def _volver_inicio(self):
        self._cancelar_cronometro()
        self._gen_feedback += 1
        self.frame_final.visible = False
        self._ocultar_feedback(actualizar=False)
        self._controller.show_frame("DashboardScreen")

    # ─── Cronómetro (disco con sector + número) ───
    def _dibujar_timer(self, segundos, actualizar=True):
        from funciones import pil_to_base64, _imagen_timer
        if segundos > 20:
            color_arco = COLOR_TIMER_OK
        elif segundos > 10:
            color_arco = COLOR_TIMER_WARN
        else:
            color_arco = COLOR_TIMER_DANGER
        self.timer_img.src = pil_to_base64(_imagen_timer(segundos, color_arco))
        self.timer_txt.value = str(segundos)
        if actualizar:
            refrescar(self.canvas_timer)

    def _mostrar_pregunta(self):
        if self.pregunta_actual >= len(self._preguntas_mezcladas):
            self._mostrar_resultado_final()
            return
        q = self._preguntas_mezcladas[self.pregunta_actual]
        self.lbl_numero.value = f"Pregunta {self.pregunta_actual + 1} / {len(self._preguntas_mezcladas)}"
        self.lbl_score.value = f"Puntaje: {self.puntaje}"
        self.lbl_pregunta.value = q.pregunta
        letras = ["A", "B", "C"]
        for i, b in enumerate(self.botones):
            b.configurar(texto=f"  {letras[i]})  {q.opciones[i]}", activo=True,
                         fondo=COLOR_OPCION_BG, color_texto=COLOR_TEXTO_OPC)
        self.tiempo_restante = TIEMPO_INICIAL
        self._dibujar_timer(TIEMPO_INICIAL, actualizar=False)
        self.respondiendo = False
        self.update()
        self._iniciar_cronometro()

    def _iniciar_cronometro(self):
        self._cancelar_cronometro()
        self.page.run_task(self._tick_loop, self._gen_timer)

    def _cancelar_cronometro(self):
        self._gen_timer += 1

    async def _tick_loop(self, gen):
        """Equivale a _tick() reprogramado con after(1000, ...)."""
        while gen == self._gen_timer:
            if self.respondiendo:
                return
            self._dibujar_timer(self.tiempo_restante)
            if self.tiempo_restante <= 0:
                self.respondiendo = True
                self._mostrar_feedback("⏰  Se acabó\nel tiempo", COLOR_INCORRECTO)
                return
            self.tiempo_restante -= 1
            await asyncio.sleep(1)

    def _seleccionar_opcion(self, idx_seleccionado: int):
        if self.respondiendo:
            return
        self.respondiendo = True
        self._cancelar_cronometro()
        q = self._preguntas_mezcladas[self.pregunta_actual]
        es_correcta = (idx_seleccionado == q.correcta)
        for i, b in enumerate(self.botones):
            b.configurar(activo=False)
            if i == q.correcta:
                b.configurar(fondo="#1B7F00", color_texto="white")
            elif i == idx_seleccionado:
                b.configurar(fondo="#8B0000", color_texto="white")
        if es_correcta:
            self.puntaje += 1
            self._mostrar_feedback("✔  CORRECTO", COLOR_CORRECTO)
        else:
            self._mostrar_feedback("✘  INCORRECTO", COLOR_INCORRECTO)

    def _mostrar_feedback(self, mensaje: str, color_fondo: str):
        self._gen_feedback += 1                       # cancela el feedback anterior
        gen = self._gen_feedback
        self.frame_feedback.bgcolor = color_fondo
        self.lbl_feedback.value = mensaje
        self.frame_feedback.visible = True
        self.update()
        self.page.run_task(self._esperar_feedback, gen)   # after(1800, ...)

    async def _esperar_feedback(self, gen):
        await asyncio.sleep(1.8)
        if gen == self._gen_feedback:
            self._siguiente_pregunta()

    def _ocultar_feedback(self, actualizar=True):
        self.frame_feedback.visible = False
        if actualizar:
            refrescar(self.frame_feedback)

    def _siguiente_pregunta(self):
        self._ocultar_feedback(actualizar=False)
        self.pregunta_actual += 1
        self._mostrar_pregunta()

    def _mostrar_resultado_final(self):
        self._cancelar_cronometro()
        total = len(self._preguntas_mezcladas)
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
        self.lbl_final.value = texto_final
        self.frame_final.visible = True
        self.update()

    def _reiniciar(self):
        self.frame_final.visible = False
        self._ocultar_feedback(actualizar=False)
        self.pregunta_actual = 0
        self.puntaje = 0
        self._preparar_preguntas()
        self._mostrar_pregunta()
