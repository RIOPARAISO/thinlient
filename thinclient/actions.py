import subprocess
from tkinter import messagebox

def shutdown_system():
    """Desliga o sistema"""
    if messagebox.askyesno("Confirmar Desligamento", "Você realmente deseja desligar o sistema?"):
        try:
            subprocess.run(["sudo", "shutdown", "now"], check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Erro", "Falha ao tentar desligar o sistema.")

def reboot_system():
    """Reinicia o sistema"""
    if messagebox.askyesno("Confirmar Reinício", "Você realmente deseja reiniciar o sistema?"):
        try:
            subprocess.run(["sudo", "reboot"], check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Erro", "Falha ao tentar reiniciar o sistema.")
