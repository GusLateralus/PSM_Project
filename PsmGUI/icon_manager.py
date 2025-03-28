# Este archivo maneja los íconos de la GUI.
import os

def get_icon_path(icon_name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(BASE_DIR, "icons",icon_name)

