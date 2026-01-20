import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageOps, ImageTk, ImageSequence

from ui_config import COLOR_ACCENT, COLOR_CANVAS, FONT_MENU, FONT_TASK, LEFT_W, RIGHT_W, RIGHT_H, resource_path


class MenuView:
    def __init__(self, root: tk.Tk, controller):
        self.root = root
        self.controller = controller
        self.menu_image = None
        self._gif_frames = []
        self._gif_index = 0
        self._gif_after_id = None
        self._gif_delay_ms = 80
        self._preview_canvas = None
        self._preview_image_id = None
        self._build()

    def dispose(self):
        if self._gif_after_id:
            self.root.after_cancel(self._gif_after_id)
            self._gif_after_id = None

    def _build(self):
        container = ttk.Frame(self.root, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(container, width=LEFT_W)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)
        info_lines = [
            "Инженерная и компьютерная графика",
            "Группа: 1483-05",
            "Выполнил: UterGrooll"
            "Преподаватель: Николаев В.В.",
        ]
        for line in info_lines:
            ttk.Label(left, text=line, font=FONT_TASK).pack(anchor="w", pady=2)
        ttk.Frame(left).pack(fill=tk.BOTH, expand=True)

        buttons = ttk.Frame(left)
        buttons.pack(fill=tk.X)
        ttk.Label(buttons, text="Выберите лабораторную работу:", font=FONT_MENU).pack(anchor="w", pady=(0, 6))
        ttk.Button(buttons, text="Лабораторная работа №1", command=self.controller.show_lab1).pack(fill=tk.X, pady=8)
        ttk.Button(buttons, text="Лабораторная работа №2", command=self.controller.show_lab2).pack(fill=tk.X, pady=8)
        ttk.Button(buttons, text="Лабораторная работа №4", command=self.controller.show_lab3).pack(fill=tk.X, pady=8)
        ttk.Frame(left).pack(fill=tk.BOTH, expand=True)

        right = ttk.Frame(container, width=RIGHT_W, height=RIGHT_H)
        right.pack(side=tk.RIGHT, padx=(15, 0))
        right.pack_propagate(False)

        preview_canvas = tk.Canvas(
            right,
            width=RIGHT_W,
            height=RIGHT_H,
            bg=COLOR_CANVAS,
            highlightthickness=2,
            highlightbackground=COLOR_ACCENT,
        )
        preview_canvas.pack()
        self._preview_canvas = preview_canvas

        try:
            img = Image.open(resource_path("nightcar.gif"))
            self._gif_delay_ms = int(img.info.get("duration", 80))
            frames = []
            for frame in ImageSequence.Iterator(img):
                resized = ImageOps.fit(frame, (RIGHT_W, RIGHT_H), Image.LANCZOS, centering=(0.5, 0.5))
                frames.append(ImageTk.PhotoImage(resized))
            if not frames:
                raise ValueError("Пустой GIF")
            self._gif_frames = frames
            self._gif_index = 0
            self._preview_image_id = preview_canvas.create_image(
                RIGHT_W // 2, RIGHT_H // 2, image=self._gif_frames[0], anchor="center"
            )
            self._schedule_gif()
        except Exception as e:
            preview_canvas.create_text(
                RIGHT_W // 2,
                RIGHT_H // 2,
                text=f"Не удалось загрузить nightcar.gif\n{e}",
                font=FONT_MENU,
            )

        bottom = ttk.Frame(self.root, padding=(15, 6))
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.columnconfigure(2, weight=1)

        audio_frame = self.controller.build_audio_controls(bottom)
        audio_frame.grid(row=0, column=0, sticky="w")

        ttk.Label(bottom, text="Год: 2026", font=FONT_MENU).grid(row=0, column=1)
        ttk.Button(bottom, text="Выход", command=self.root.quit).grid(row=0, column=2, sticky="e")

    def _schedule_gif(self):
        if not self._gif_frames or not self._preview_canvas:
            return
        self._gif_after_id = self.root.after(self._gif_delay_ms, self._step_gif)

    def _step_gif(self):
        if not self._gif_frames or not self._preview_canvas or self._preview_image_id is None:
            return
        self._gif_index = (self._gif_index + 1) % len(self._gif_frames)
        self._preview_canvas.itemconfigure(self._preview_image_id, image=self._gif_frames[self._gif_index])
        self._schedule_gif()
