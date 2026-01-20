import tkinter as tk
from tkinter import ttk

from ui_config import AUDIO_VOLUME_MAX, FONT_TASK


def build_audio_controls(parent, audio_player):
    frame = ttk.Frame(parent)

    if not audio_player.available:
        ttk.Label(frame, text="Нет звука", font=FONT_TASK).pack(side=tk.LEFT)
        return frame

    ttk.Label(frame, text="Громкость", font=FONT_TASK).pack(side=tk.LEFT, padx=(0, 6))

    volume_var = tk.DoubleVar(value=audio_player.volume)

    def on_volume_change(_=None):
        value = int(round(volume_var.get()))
        audio_player.set_volume(value)

    scale = ttk.Scale(
        frame,
        from_=0,
        to=AUDIO_VOLUME_MAX,
        orient="horizontal",
        variable=volume_var,
        command=on_volume_change,
        length=160,
    )
    scale.pack(side=tk.LEFT)
    return frame
