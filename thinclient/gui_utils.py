import tkinter as tk

def center_window(window, width=540, height=330):
    """Centraliza a janela na tela"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def close_window(window):
    """Fecha a janela atual"""
    window.destroy()
