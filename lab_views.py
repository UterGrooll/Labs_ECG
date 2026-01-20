import math
import tkinter as tk
from tkinter import ttk, messagebox

from labs_data import LAB1, LAB2, LAB3
from ui_config import (
    COLOR_CANVAS,
    COLOR_TEXT,
    COLOR_GRID,
    COLOR_ACCENT,
    FONT_MENU,
    FONT_TASK,
    FONT_TITLE,
    LEFT_W,
    RIGHT_W,
    RIGHT_H,
    P_LEFT,
    P_RIGHT,
    P_TOP,
    P_BOTTOM,
)


def draw_grid_and_axes_custom(canvas, width, height, x_min, x_max, y_min, y_max):
    grid_color = COLOR_GRID
    text_color = COLOR_TEXT
    axes_color = COLOR_TEXT

    for i in range(11):
        cx = P_LEFT + i * (width - P_LEFT - P_RIGHT) / 10
        canvas.create_line(cx, P_TOP, cx, height - P_BOTTOM, fill=grid_color, dash=(2, 2))
    for i in range(11):
        cy = P_TOP + i * (height - P_TOP - P_BOTTOM) / 10
        canvas.create_line(P_LEFT, cy, width - P_RIGHT, cy, fill=grid_color, dash=(2, 2))

    for i in range(11):
        x = x_min + i * (x_max - x_min) / 10
        cx = P_LEFT + i * (width - P_LEFT - P_RIGHT) / 10
        canvas.create_text(cx, height - P_BOTTOM + 18, text=f"{x:.2f}", font=("Arial", 10), fill=text_color)

    for i in range(11):
        y = y_max - i * (y_max - y_min) / 10
        cy = P_TOP + i * (height - P_TOP - P_BOTTOM) / 10
        canvas.create_text(P_LEFT - 12, cy, text=f"{y:.2f}", font=("Arial", 10), fill=text_color, anchor="e")

    canvas.create_line(
        P_LEFT,
        height - P_BOTTOM,
        width - P_RIGHT,
        height - P_BOTTOM,
        fill=axes_color,
        width=2,
        arrow=tk.LAST,
    )
    canvas.create_line(
        P_LEFT,
        height - P_BOTTOM,
        P_LEFT,
        P_TOP,
        fill=axes_color,
        width=2,
        arrow=tk.FIRST,
    )

    canvas.create_text(
        width - P_RIGHT + 12,
        height - P_BOTTOM + 5,
        text="x",
        font=("Arial", 12, "bold"),
        fill=axes_color,
    )
    canvas.create_text(
        P_LEFT - 20,
        P_TOP - 35,
        text="y",
        font=("Arial", 12, "bold"),
        fill=axes_color,
    )


class Lab1View:
    def __init__(self, root: tk.Tk, controller):
        self.root = root
        self.controller = controller
        self.lab1_canvas = None
        self.lab1_status = tk.StringVar(value="Готов к построению")
        self._build()

    def _build(self):
        container = ttk.Frame(self.root, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(container)
        top.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(top, text="< В меню", command=self.controller.show_menu).pack(side=tk.LEFT)
        ttk.Label(top, text="Лабораторная работа №1", font=FONT_MENU).pack(side=tk.TOP)

        body = ttk.Frame(container)
        body.pack(fill=tk.X)

        left = ttk.Frame(body, width=LEFT_W)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        ttk.Label(left, text="Задание", font=FONT_MENU).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            left,
            text="График заданных функций в одной системе координат",
            font=FONT_TASK,
            justify=tk.LEFT,
            wraplength=LEFT_W - 10,
        ).pack(anchor="w", pady=(0, 14))

        ttk.Label(left, text="Вариант 5", font=FONT_MENU).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            left,
            text="y1 = e^(-x)\n"
                 "y2 = 10^(-x)\n"
                 "x ∈ [1; 2]",
            font=FONT_TASK,
            justify=tk.LEFT,
        ).pack(anchor="w", pady=(0, 16))

        ttk.Label(left, text="Параметры построения", font=FONT_MENU).pack(anchor="w", pady=(0, 6))

        form = ttk.Frame(left)
        form.pack(anchor="w", pady=(0, 12))

        self.lab1_x1 = tk.DoubleVar(value=LAB1["x1"])
        self.lab1_x2 = tk.DoubleVar(value=LAB1["x2"])

        ttk.Label(form, text="Начало (x1):", font=FONT_TASK).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(form, textvariable=self.lab1_x1, width=10, font=FONT_TASK).grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(form, text="Конец (x2):", font=FONT_TASK).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(form, textvariable=self.lab1_x2, width=10, font=FONT_TASK).grid(row=1, column=1, sticky="w", pady=6)

        btns = ttk.Frame(left)
        btns.pack(anchor="w", pady=(10, 0))
        ttk.Button(btns, text="Построить", command=self.lab1_plot).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(btns, text="Очистить", command=self.lab1_clear).grid(row=0, column=1)

        right = ttk.Frame(body, width=RIGHT_W, height=RIGHT_H)
        right.pack(side=tk.RIGHT, padx=(15, 0))
        right.pack_propagate(False)

        self.lab1_canvas = tk.Canvas(
            right,
            width=RIGHT_W,
            height=RIGHT_H,
            bg=COLOR_CANVAS,
            highlightthickness=2,
            highlightbackground=COLOR_ACCENT,
        )
        self.lab1_canvas.pack()

        bottom = ttk.Frame(self.root, padding=(15, 6))
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=3)

        audio_frame = self.controller.build_audio_controls(bottom)
        audio_frame.grid(row=0, column=0, sticky="w")
        ttk.Label(bottom, textvariable=self.lab1_status, font=FONT_TASK).grid(
            row=0, column=1, sticky="w", padx=(12, 0)
        )

        self.lab1_plot()

    def lab1_plot(self):
        try:
            self.lab1_canvas.delete("all")
            x1 = float(self.lab1_x1.get())
            x2 = float(self.lab1_x2.get())
            n = int(LAB1["points"])

            if x1 >= x2:
                raise ValueError("Начало (x1) должно быть меньше конца (x2)")

            width = RIGHT_W
            height = RIGHT_H

            x_values = [x1 + i * (x2 - x1) / (n - 1) for i in range(n)]
            y_sets = []
            for _, f in LAB1["functions"]:
                y_sets.append([f(x) for x in x_values])

            y_min = min(min(ys) for ys in y_sets)
            y_max = max(max(ys) for ys in y_sets)
            y_range = y_max - y_min

            if abs(y_range) < 1e-12:
                y_range = 1.0
                y_min -= 0.5
                y_max += 0.5
            else:
                y_min -= y_range * 0.10
                y_max += y_range * 0.10

            draw_grid_and_axes_custom(self.lab1_canvas, width, height, x1, x2, y_min, y_max)

            plot_w = width - P_LEFT - P_RIGHT
            plot_h = height - P_TOP - P_BOTTOM
            x_scale = plot_w / (x2 - x1)
            y_scale = plot_h / (y_max - y_min)

            def to_canvas(x, y):
                cx = P_LEFT + (x - x1) * x_scale
                cy = height - P_BOTTOM - (y - y_min) * y_scale
                return cx, cy

            colors = ["#2196F3", "#E91E63"]
            for idx, ys in enumerate(y_sets):
                pts = [to_canvas(x_values[i], ys[i]) for i in range(n)]
                self.lab1_canvas.create_line(pts, fill=colors[idx], width=2, smooth=True)

            self.lab1_canvas.create_text(
                width // 2,
                20,
                text="ЛР1 (вариант 5): графики двух функций",
                font=FONT_TITLE,
                fill=COLOR_TEXT,
            )

            legend_x = width - P_RIGHT - 210
            legend_y = 55
            for i, (name, _) in enumerate(LAB1["functions"]):
                y0 = legend_y + i * 20
                self.lab1_canvas.create_line(legend_x, y0, legend_x + 40, y0, fill=colors[i], width=3)
                self.lab1_canvas.create_text(legend_x + 55, y0, text=name, anchor="w", font=FONT_TASK, fill=COLOR_TEXT)

            self.lab1_status.set(f"Построено: 2 графика, x ∈ [{x1}; {x2}], точек: {n}")

        except Exception as e:
            self.lab1_status.set(f"Ошибка: {e}")
            messagebox.showerror("Ошибка", str(e))

    def lab1_clear(self):
        self.lab1_canvas.delete("all")
        self.lab1_status.set("Очищено")


class Lab2View:
    def __init__(self, root: tk.Tk, controller):
        self.root = root
        self.controller = controller
        self.lab2_canvas = None
        self.lab2_status = tk.StringVar(value="Готово")
        self.lab2_animating = False
        self.lab2_after_id = None
        self.lab2_anim_btn = None
        self._build()

    def dispose(self):
        if self.lab2_after_id:
            self.root.after_cancel(self.lab2_after_id)
            self.lab2_after_id = None
        self.lab2_animating = False

    def _build(self):
        container = ttk.Frame(self.root, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(container)
        top.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(top, text="< В меню", command=self.controller.show_menu).pack(side=tk.LEFT)
        ttk.Label(top, text="Лабораторная работа №2", font=FONT_MENU).pack(side=tk.TOP)

        body = ttk.Frame(container)
        body.pack(fill=tk.X)

        left = ttk.Frame(body, width=LEFT_W)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        ttk.Label(left, text="Управление", font=FONT_MENU).pack(anchor="w", pady=(0, 10))

        ttk.Label(left, text="Выберите фигуру:", font=FONT_TASK).pack(anchor="w", pady=(0, 6))
        self.lab2_shape = tk.StringVar(value=LAB2.get("shape", "triangle"))

        def add_rb(text, value):
            ttk.Radiobutton(left, text=text, variable=self.lab2_shape, value=value, command=self.lab2_draw_current).pack(
                anchor="w", pady=2
            )

        add_rb("Треугольник", "triangle")
        add_rb("Квадрат", "square")
        add_rb("Пятиугольник", "pentagon")
        add_rb("Шестиугольник", "hexagon")
        add_rb("Семиугольник", "heptagon")

        params = ttk.LabelFrame(left, text="Параметры вращения", padding=10)
        params.pack(fill=tk.X, pady=(12, 12))

        self.lab2_x0 = tk.DoubleVar(value=LAB2.get("x0", 0.0))
        self.lab2_y0 = tk.DoubleVar(value=LAB2.get("y0", 0.0))
        self.lab2_phi = tk.IntVar(value=LAB2.get("phi", 0))

        ttk.Label(params, text="Центр вращения X:", font=FONT_TASK).pack(anchor="w")
        ttk.Scale(
            params,
            from_=-5,
            to=5,
            orient="horizontal",
            variable=self.lab2_x0,
            command=lambda _=None: self.lab2_draw_current(),
        ).pack(fill=tk.X, pady=(2, 8))

        ttk.Label(params, text="Центр вращения Y:", font=FONT_TASK).pack(anchor="w")
        ttk.Scale(
            params,
            from_=-5,
            to=5,
            orient="horizontal",
            variable=self.lab2_y0,
            command=lambda _=None: self.lab2_draw_current(),
        ).pack(fill=tk.X, pady=(2, 8))

        ttk.Label(params, text="Угол вращения (°):", font=FONT_TASK).pack(anchor="w")
        ttk.Scale(
            params,
            from_=0,
            to=360,
            orient="horizontal",
            variable=self.lab2_phi,
            command=lambda _=None: self.lab2_draw_current(),
        ).pack(fill=tk.X, pady=(2, 0))

        btns = ttk.Frame(left)
        btns.pack(anchor="w", pady=(10, 0))
        self.lab2_anim_btn = ttk.Button(btns, text="Пуск", command=self.lab2_toggle_anim)
        self.lab2_anim_btn.grid(row=0, column=0)


        right = ttk.Frame(body, width=RIGHT_W, height=RIGHT_H)
        right.pack(side=tk.RIGHT, padx=(15, 0))
        right.pack_propagate(False)

        self.lab2_canvas = tk.Canvas(
            right,
            width=RIGHT_W,
            height=RIGHT_H,
            bg=COLOR_CANVAS,
            highlightthickness=2,
            highlightbackground=COLOR_ACCENT,
        )
        self.lab2_canvas.pack()

        bottom = ttk.Frame(self.root, padding=(15, 6))
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=3)

        audio_frame = self.controller.build_audio_controls(bottom)
        audio_frame.grid(row=0, column=0, sticky="w")
        ttk.Label(bottom, textvariable=self.lab2_status, font=FONT_TASK).grid(
            row=0, column=1, sticky="w", padx=(12, 0)
        )

        self.lab2_animating = False
        self.lab2_after_id = None

        self.lab2_draw_current()

    def lab2_toggle_anim(self):
        self.lab2_animating = not self.lab2_animating
        if self.lab2_anim_btn:
            self.lab2_anim_btn.config(text="Стоп" if self.lab2_animating else "Пуск")
        if self.lab2_animating:
            self.lab2_step_animation()
        elif self.lab2_after_id:
            self.root.after_cancel(self.lab2_after_id)
            self.lab2_after_id = None

    def lab2_step_animation(self):
        if not self.lab2_animating:
            return

        angle = int(self.lab2_phi.get())
        if angle >= 360:
            angle = 0
        self.lab2_phi.set(angle + 3)
        self.lab2_draw_current()
        self.lab2_after_id = self.root.after(25, self.lab2_step_animation)

    def lab2_draw_current(self):
        self.lab2_canvas.delete("all")

        x0 = float(self.lab2_x0.get())
        y0 = float(self.lab2_y0.get())
        phi = float(self.lab2_phi.get())
        shape = self.lab2_shape.get()

        pts = self._lab2_make_polygon(shape)
        pts_rot = self._lab2_rotate_polygon(pts, x0, y0, phi)

        all_x = [p[0] for p in pts] + [p[0] for p in pts_rot] + [x0]
        all_y = [p[1] for p in pts] + [p[1] for p in pts_rot] + [y0]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        dx = max_x - min_x
        dy = max_y - min_y
        if dx < 1e-9:
            dx = 1.0
        if dy < 1e-9:
            dy = 1.0

        min_x -= dx * 0.8
        max_x += dx * 0.8
        min_y -= dy * 0.8
        max_y += dy * 0.8

        draw_grid_and_axes_custom(self.lab2_canvas, RIGHT_W, RIGHT_H, min_x, max_x, min_y, max_y)

        plot_w = RIGHT_W - P_LEFT - P_RIGHT
        plot_h = RIGHT_H - P_TOP - P_BOTTOM
        x_scale = plot_w / (max_x - min_x)
        y_scale = plot_h / (max_y - min_y)

        def to_canvas(x, y):
            cx = P_LEFT + (x - min_x) * x_scale
            cy = RIGHT_H - P_BOTTOM - (y - min_y) * y_scale
            return cx, cy

        self._lab2_draw_polygon(
            self.lab2_canvas,
            [to_canvas(x, y) for x, y in pts],
            outline="#888888",
            dashed=True,
        )
        self._lab2_draw_polygon(
            self.lab2_canvas,
            [to_canvas(x, y) for x, y in pts_rot],
            outline="#2e7d32",
            dashed=False,
        )

        for x, y in pts_rot:
            cx, cy = to_canvas(x, y)
            r = 4
            self.lab2_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#ff5722", outline="#ff5722")

        cx0, cy0 = to_canvas(x0, y0)
        r = 6
        self.lab2_canvas.create_oval(cx0 - r, cy0 - r, cx0 + r, cy0 + r, fill="#1976d2", outline="#1976d2")

        title = f"Вращение {self._lab2_shape_name(shape)}"
        self.lab2_canvas.create_text(RIGHT_W // 2, 20, text=title, font=FONT_MENU, fill=COLOR_TEXT)
        self.lab2_status.set(f"{title} | φ = {phi:.0f}° | центр: ({x0:.2f}; {y0:.2f})")

    def _lab2_shape_name(self, shape: str) -> str:
        return {
            "triangle": "Треугольник",
            "square": "Квадрат",
            "pentagon": "Пятиугольник",
            "hexagon": "Шестиугольник",
            "heptagon": "Семиугольник",
        }.get(shape, "Многоугольник")

    def _lab2_make_polygon(self, shape: str):
        n = {"triangle": 3, "square": 4, "pentagon": 5, "hexagon": 6, "heptagon": 7}.get(shape, 3)
        r = 2.0
        pts = []
        start = -math.pi / 2
        for i in range(n):
            a = start + 2 * math.pi * i / n
            pts.append((r * math.cos(a), r * math.sin(a)))
        return pts

    def _lab2_rotate_polygon(self, pts, x0, y0, phi_deg):
        phi = math.radians(phi_deg)
        c = math.cos(phi)
        s = math.sin(phi)
        out = []
        for x, y in pts:
            xr = x0 + (x - x0) * c - (y - y0) * s
            yr = y0 + (x - x0) * s + (y - y0) * c
            out.append((xr, yr))
        return out

    def _lab2_draw_polygon(self, canvas, pts_canvas, outline="black", dashed=False):
        flat = []
        for cx, cy in pts_canvas:
            flat.extend([cx, cy])
        dash = (4, 4) if dashed else None
        canvas.create_polygon(flat, outline=outline, width=2, fill="", dash=dash)


class Lab3View:
    def __init__(self, root: tk.Tk, controller):
        self.root = root
        self.controller = controller
        self.lab3_canvas = None
        self.lab3_status = None
        self.lab3_animating = False
        self.lab3_after_id = None
        self.lab3_anim_btn = None
        self._build()

    def _is_number(self, value: str):
        if value in ("", "-", ".", "-."):
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def dispose(self):
        if self.lab3_after_id:
            self.root.after_cancel(self.lab3_after_id)
            self.lab3_after_id = None
        self.lab3_animating = False

    def _build(self):
        container = ttk.Frame(self.root, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(container)
        top.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(top, text="< В меню", command=self.controller.show_menu).pack(side=tk.LEFT)
        ttk.Label(top, text="Лабораторная работа №4", font=FONT_MENU).pack(side=tk.TOP)

        body = ttk.Frame(container)
        body.pack(fill=tk.X)

        left = ttk.Frame(body, width=LEFT_W)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)

        ttk.Label(left, text="Задание", font=FONT_MENU).pack(anchor="w", pady=(0, 6))
        ttk.Label(
            left,
            text="Параллельная проекция куба\nи вращение вокруг произвольного вектора\nНаблюдение вдоль +Z",
            font=FONT_TASK,
            justify=tk.LEFT,
        ).pack(anchor="w", pady=(0, 10))

        params = ttk.LabelFrame(left, text="Повороты сцены", padding=10)
        params.pack(fill=tk.X, pady=(6, 10))

        vcmd = (self.root.register(self._is_number), "%P")

        self.lab3_alpha = tk.DoubleVar(value=LAB3["alpha_deg"])
        self.lab3_beta = tk.DoubleVar(value=LAB3["beta_deg"])

        ttk.Label(params, text="α вокруг X (°):", font=FONT_TASK).grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)
        ttk.Scale(
            params,
            from_=0,
            to=360,
            orient="horizontal",
            variable=self.lab3_alpha,
            command=lambda _=None: self.lab3_draw(),
        ).grid(row=0, column=1, sticky="we", pady=4)

        ttk.Label(params, text="β вокруг Y (°):", font=FONT_TASK).grid(row=1, column=0, sticky="w", padx=(0, 6), pady=4)
        ttk.Scale(
            params,
            from_=0,
            to=360,
            orient="horizontal",
            variable=self.lab3_beta,
            command=lambda _=None: self.lab3_draw(),
        ).grid(row=1, column=1, sticky="we", pady=4)

        axis_box = ttk.LabelFrame(left, text="Ось вращения", padding=10)
        axis_box.pack(fill=tk.X, pady=(6, 10))
        axis_box.columnconfigure(1, weight=1)
        axis_box.columnconfigure(2, weight=1)
        axis_box.columnconfigure(3, weight=1)

        ax, ay, az = LAB3["axis_point"]
        vx, vy, vz = LAB3["axis_dir"]
        self.lab3_ax = tk.DoubleVar(value=ax)
        self.lab3_ay = tk.DoubleVar(value=ay)
        self.lab3_az = tk.DoubleVar(value=az)
        self.lab3_vx = tk.DoubleVar(value=vx)
        self.lab3_vy = tk.DoubleVar(value=vy)
        self.lab3_vz = tk.DoubleVar(value=vz)
        self.lab3_angle = tk.DoubleVar(value=LAB3["angle_deg"])

        ax_entry = ttk.Entry(axis_box, textvariable=self.lab3_ax, width=6, font=FONT_TASK,
                             validate="key", validatecommand=vcmd)
        ay_entry = ttk.Entry(axis_box, textvariable=self.lab3_ay, width=6, font=FONT_TASK,
                             validate="key", validatecommand=vcmd)
        az_entry = ttk.Entry(axis_box, textvariable=self.lab3_az, width=6, font=FONT_TASK,
                             validate="key", validatecommand=vcmd)
        vx_entry = ttk.Entry(axis_box, textvariable=self.lab3_vx, width=6, font=FONT_TASK,
                             validate="key", validatecommand=vcmd)
        vy_entry = ttk.Entry(axis_box, textvariable=self.lab3_vy, width=6, font=FONT_TASK,
                             validate="key", validatecommand=vcmd)
        vz_entry = ttk.Entry(axis_box, textvariable=self.lab3_vz, width=6, font=FONT_TASK,
                             validate="key", validatecommand=vcmd)

        ttk.Label(axis_box, text="Точка A (x,y,z):", font=FONT_TASK).grid(row=0, column=0, sticky="w", pady=4)
        ax_entry.grid(row=0, column=1, sticky="w", padx=(6, 6), pady=4)
        ay_entry.grid(row=0, column=2, sticky="w", padx=(0, 6), pady=4)
        az_entry.grid(row=0, column=3, sticky="w", pady=4)

        ttk.Label(axis_box, text="Вектор v:", font=FONT_TASK).grid(row=1, column=0, sticky="w", pady=4)
        vx_entry.grid(row=1, column=1, sticky="w", padx=(6, 6), pady=4)
        vy_entry.grid(row=1, column=2, sticky="w", padx=(0, 6), pady=4)
        vz_entry.grid(row=1, column=3, sticky="w", pady=4)

        ttk.Label(axis_box, text="Угол (deg):", font=FONT_TASK).grid(row=2, column=0, sticky="w", pady=4)
        ttk.Scale(
            axis_box,
            from_=0,
            to=360,
            orient="horizontal",
            variable=self.lab3_angle,
            command=lambda _=None: self.lab3_draw(),
        ).grid(row=2, column=1, columnspan=3, sticky="we", pady=4)

        btns = ttk.Frame(left)
        btns.pack(anchor="w", pady=(6, 0))
        self.lab3_anim_btn = ttk.Button(btns, text="Пуск", command=self.lab3_toggle_anim)
        self.lab3_anim_btn.grid(row=0, column=0)

        for entry in (ax_entry, ay_entry, az_entry, vx_entry, vy_entry, vz_entry):
            entry.bind("<Return>", lambda _evt: self.lab3_draw())

        right = ttk.Frame(body, width=RIGHT_W, height=RIGHT_H)
        right.pack(side=tk.RIGHT, padx=(15, 0))
        right.pack_propagate(False)

        self.lab3_canvas = tk.Canvas(
            right,
            width=RIGHT_W,
            height=RIGHT_H,
            bg=COLOR_CANVAS,
            highlightthickness=2,
            highlightbackground=COLOR_ACCENT,
        )
        self.lab3_canvas.pack()

        bottom = ttk.Frame(self.root, padding=(15, 6))
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        audio_frame = self.controller.build_audio_controls(bottom)
        audio_frame.grid(row=0, column=0, sticky="w")
        ttk.Label(bottom, text="by UterGrooll", font=FONT_TASK).grid(row=0, column=1, sticky="e")

        self.lab3_draw()

    def lab3_draw(self):
        self.lab3_canvas.delete("all")
        try:
            cube_size = float(LAB3["cube_size"])
            alpha = math.radians(float(self.lab3_alpha.get()))
            beta = math.radians(float(self.lab3_beta.get()))

            ax = float(self.lab3_ax.get())
            ay = float(self.lab3_ay.get())
            az = float(self.lab3_az.get())
            vx = float(self.lab3_vx.get())
            vy = float(self.lab3_vy.get())
            vz = float(self.lab3_vz.get())
            angle = math.radians(float(self.lab3_angle.get()))

            cube_pts = self._cube_points(cube_size)
            rotated = [
                self._rotate_around_axis(p, (ax, ay, az), (vx, vy, vz), angle)
                for p in cube_pts
            ]
            rotated_scene = [self._rotate_y(self._rotate_x(p, alpha), beta) for p in rotated]
            projected = [(x, y) for x, y, _ in rotated_scene]

            bounds = self._compute_bounds_2d(projected)
            mapper = self._make_mapper_2d(bounds)

            for i1, i2 in self._cube_edges():
                p1 = projected[i1]
                p2 = projected[i2]
                if p1 is None or p2 is None:
                    continue
                x1, y1 = mapper(p1)
                x2, y2 = mapper(p2)
                self.lab3_canvas.create_line(x1, y1, x2, y2, fill=COLOR_TEXT)

            pass
        except Exception as e:
            pass
            if self.lab3_animating:
                self.lab3_toggle_anim()

    def _rotate_x(self, p, angle):
        x, y, z = p
        c = math.cos(angle)
        s = math.sin(angle)
        return (x, y * c - z * s, y * s + z * c)

    def _rotate_y(self, p, angle):
        x, y, z = p
        c = math.cos(angle)
        s = math.sin(angle)
        return (x * c + z * s, y, -x * s + z * c)

    def lab3_toggle_anim(self):
        self.lab3_animating = not self.lab3_animating
        if self.lab3_anim_btn:
            self.lab3_anim_btn.config(text="Стоп" if self.lab3_animating else "Пуск")
        if self.lab3_animating:
            self._lab3_step_anim()
        elif self.lab3_after_id:
            self.root.after_cancel(self.lab3_after_id)
            self.lab3_after_id = None

    def _lab3_step_anim(self):
        if not self.lab3_animating:
            return
        angle = float(self.lab3_angle.get())
        angle = (angle + 2.0) % 360.0
        self.lab3_angle.set(angle)
        self.lab3_draw()
        self.lab3_after_id = self.root.after(40, self._lab3_step_anim)

    def _cube_points(self, size):
        h = size / 2.0
        return [
            (-h, -h, -h),
            (h, -h, -h),
            (h, h, -h),
            (-h, h, -h),
            (-h, -h, h),
            (h, -h, h),
            (h, h, h),
            (-h, h, h),
        ]

    def _cube_edges(self):
        return [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]

    def _rotate_around_axis(self, p, axis_point, axis_dir, angle):
        px, py, pz = p
        ax, ay, az = axis_point
        vx, vy, vz = axis_dir

        vx, vy, vz = self._normalize(vx, vy, vz)
        x = px - ax
        y = py - ay
        z = pz - az

        c = math.cos(angle)
        s = math.sin(angle)

        rx = x * c + (vy * z - vz * y) * s + vx * (vx * x + vy * y + vz * z) * (1 - c)
        ry = y * c + (vz * x - vx * z) * s + vy * (vx * x + vy * y + vz * z) * (1 - c)
        rz = z * c + (vx * y - vy * x) * s + vz * (vx * x + vy * y + vz * z) * (1 - c)

        return (rx + ax, ry + ay, rz + az)

    def _project_points(self, points, eye, d):
        ex, ey, ez = eye
        forward = self._normalize(-ex, -ey, -ez)
        right = self._normalize(*self._cross(0.0, 1.0, 0.0, *forward))
        up = self._cross(*forward, *right)

        out = []
        for x, y, z in points:
            vx = x - ex
            vy = y - ey
            vz = z - ez
            cx = self._dot(vx, vy, vz, *right)
            cy = self._dot(vx, vy, vz, *up)
            cz = self._dot(vx, vy, vz, *forward)
            if cz <= 1e-6:
                out.append(None)
                continue
            X = d * cx / cz
            Y = d * cy / cz
            out.append((X, Y))
        return out

    def _compute_bounds_2d(self, points):
        xs = [p[0] for p in points if p is not None]
        ys = [p[1] for p in points if p is not None]
        if not xs or not ys:
            raise ValueError("Нет видимых точек")
        return min(xs), max(xs), min(ys), max(ys)

    def _make_mapper_2d(self, bounds):
        min_x, max_x, min_y, max_y = bounds
        plot_w = RIGHT_W - P_LEFT - P_RIGHT
        plot_h = RIGHT_H - P_TOP - P_BOTTOM
        scale_x = plot_w / (max_x - min_x)
        scale_y = plot_h / (max_y - min_y)
        scale = min(scale_x, scale_y)

        used_w = (max_x - min_x) * scale
        used_h = (max_y - min_y) * scale
        x0 = P_LEFT + (plot_w - used_w) / 2
        y0 = P_TOP + (plot_h - used_h) / 2

        def to_canvas(p):
            x, y = p
            sx = x0 + (x - min_x) * scale
            sy = y0 + (max_y - y) * scale
            return sx, sy

        return to_canvas

    def _normalize(self, x, y, z):
        n = math.sqrt(x * x + y * y + z * z)
        if n < 1e-9:
            return (0.0, 0.0, 1.0)
        return (x / n, y / n, z / n)

    def _dot(self, ax, ay, az, bx, by, bz):
        return ax * bx + ay * by + az * bz

    def _cross(self, ax, ay, az, bx, by, bz):
        return (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)
