import os
import sys


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)


FONT_MENU = ("Segoe UI Semibold", 11)
FONT_TASK = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI Semibold", 12)

APP_W = 1024
APP_H = 720

LEFT_W = 360
BOTTOM_H = 70

RIGHT_W = APP_W - LEFT_W - 40
RIGHT_H = APP_H - BOTTOM_H - 40

P_LEFT = 80
P_RIGHT = 30
P_TOP = 85
P_BOTTOM = 50

AUDIO_FILE = "Nightcall-_16-Bit-Remix.mp3"
AUDIO_VOLUME_MAX = 10
AUDIO_VOLUME_DEFAULT = 5

COLOR_BG = "#120b1e"
COLOR_PANEL = "#1a102a"
COLOR_TEXT = "#f3e8ff"
COLOR_BUTTON_BG = "#2b1845"
COLOR_BUTTON_ACTIVE = "#3a1f5c"
COLOR_ACCENT = "#ff3cac"
COLOR_ACCENT_2 = "#00e5ff"
COLOR_GRID = "#2c1b46"
COLOR_CANVAS = "#0b0814"
COLOR_INPUT_BG = "#1f1433"
