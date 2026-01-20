import tkinter as tk
from tkinter import ttk

from audio_controls import build_audio_controls
from audio_player import AudioPlayer
from lab_views import Lab1View, Lab2View, Lab3View
from menu_view import MenuView
from ui_config import (
    APP_W,
    APP_H,
    AUDIO_FILE,
    AUDIO_VOLUME_DEFAULT,
    AUDIO_VOLUME_MAX,
    COLOR_BG,
    COLOR_PANEL,
    COLOR_TEXT,
    COLOR_BUTTON_BG,
    COLOR_BUTTON_ACTIVE,
    COLOR_ACCENT,
    COLOR_ACCENT_2,
    COLOR_INPUT_BG,
    FONT_MENU,
    FONT_TASK,
)
from tkinter import messagebox


class AppController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Инженерная и компьютерная графика — Светлов Д.В. гр.1483-05")
        self.root.geometry(f"{APP_W}x{APP_H}")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        self.audio = AudioPlayer(AUDIO_FILE, volume=AUDIO_VOLUME_DEFAULT, max_volume=AUDIO_VOLUME_MAX)
        self.audio.start()
        if not self.audio.available:
            messagebox.showwarning("Музыка", f"Не удалось запустить музыку: {self.audio.error}")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=FONT_TASK)
        style.configure("TFrame", background=COLOR_BG)
        style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT)
        style.configure("TLabelframe", background=COLOR_BG, foreground=COLOR_TEXT)
        style.configure("TLabelframe.Label", background=COLOR_BG, foreground=COLOR_TEXT, font=FONT_TASK)
        style.configure(
            "TButton",
            font=FONT_MENU,
            background=COLOR_BUTTON_BG,
            foreground=COLOR_TEXT,
            relief="raised",
            borderwidth=2,
        )
        style.map(
            "TButton",
            background=[("active", COLOR_BUTTON_ACTIVE), ("pressed", COLOR_BUTTON_ACTIVE)],
            relief=[("pressed", "sunken"), ("active", "raised")],
        )
        style.configure("TRadiobutton", background=COLOR_BG, foreground=COLOR_TEXT)
        style.map("TRadiobutton", background=[("active", COLOR_BG)], foreground=[("active", COLOR_TEXT)])
        style.configure("TEntry", fieldbackground=COLOR_INPUT_BG, foreground=COLOR_TEXT)
        style.configure("Horizontal.TScale", background=COLOR_BG, troughcolor=COLOR_PANEL)
        style.map(
            "Horizontal.TScale",
            background=[("active", COLOR_BG)],
            troughcolor=[("active", COLOR_PANEL)],
        )
        style.configure("Neon.TButton", font=FONT_MENU, background=COLOR_ACCENT, foreground=COLOR_BG)
        style.map("Neon.TButton", background=[("active", COLOR_ACCENT_2), ("pressed", COLOR_ACCENT_2)])

        self.current_view = None
        self.show_menu()

    def build_audio_controls(self, parent):
        return build_audio_controls(parent, self.audio)

    def clear_root(self):
        if self.current_view and hasattr(self.current_view, "dispose"):
            self.current_view.dispose()
        for w in self.root.winfo_children():
            w.destroy()

    def show_menu(self):
        self.clear_root()
        self.current_view = MenuView(self.root, self)

    def show_lab1(self):
        self.clear_root()
        self.current_view = Lab1View(self.root, self)

    def show_lab2(self):
        self.clear_root()
        self.current_view = Lab2View(self.root, self)

    def show_lab3(self):
        self.clear_root()
        self.current_view = Lab3View(self.root, self)
