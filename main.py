import tkinter as tk
from tkinter import messagebox

from app import AppController
from ui_config import APP_W, APP_H


def main():
    root = tk.Tk()
    AppController(root)

    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - APP_W) // 2
    y = (sh - APP_H) // 2
    root.geometry(f"{APP_W}x{APP_H}+{x}+{y}")

    def on_close():
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
