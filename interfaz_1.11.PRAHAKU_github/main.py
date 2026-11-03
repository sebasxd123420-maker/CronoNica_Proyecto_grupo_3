import os
os.system("cls")
import flet as ft
from datos import ASSETS_DIR
from gui.App import App

# =====================================================================
# PUNTO DE ENTRADA
# =====================================================================
def main(page: ft.Page):
    App(page)

if __name__ == "__main__":
    ft.run(
        main,
        assets_dir=ASSETS_DIR,
    )