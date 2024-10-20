import tkinter as tk
from tkinter import messagebox  # Importando o messagebox
from config_manager import load_config, save_config
from gui_utils import center_window, close_window
from connection import connect_to_server
from actions import shutdown_system, reboot_system
import subprocess

def run_vnc_server():
    try:
        # Executa o comando como root
        command = "sudo vncserver-x11-serviced"
        subprocess.run(command, shell=True, check=True)
        print("vncserver-x11 iniciado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")

# Chama a função para rodar o comando
run_vnc_server()


def connect():
    server_ip, domain, last_user, enable_usb, enable_sound, enable_printer, enable_drives, protocol = load_config()

    connect_window = tk.Toplevel()
    connect_window.title("Conectar ao Servidor")
    center_window(connect_window, width=270, height=82)  # Ajustando o tamanho da janela
    connect_window.resizable(False, False)  # Desativa o redimensionamento para manter o tamanho fixo

    tk.Label(connect_window, text="Usuário").grid(row=0, column=0)
    tk.Label(connect_window, text="Senha").grid(row=1, column=0)

    user_entry = tk.Entry(connect_window)
    user_entry.grid(row=0, column=1)
    user_entry.insert(0, last_user)

    password_entry = tk.Entry(connect_window, show="*")
    password_entry.grid(row=1, column=1)

    def submit():
        user = user_entry.get()
        password = password_entry.get()
        if not user or not password:
            messagebox.showerror("Erro", "Usuário ou senha não pode estar vazio!")
            return
        connect_to_server(server_ip, domain, last_user, enable_usb, enable_sound, enable_printer, enable_drives, protocol, user, password)
        close_window(connect_window)

    tk.Button(connect_window, text="Conectar", command=submit).grid(row=2, column=0)
    tk.Button(connect_window, text="Voltar", command=lambda: close_window(connect_window)).grid(row=2, column=1)

    connect_window.grab_set()


# Função de autenticação antes de permitir acessar as configurações
def authenticate():
    auth_window = tk.Toplevel()
    auth_window.title("Autenticação")
    center_window(auth_window, width=250, height=100)
    auth_window.resizable(False, False)

    tk.Label(auth_window, text="Usuário").grid(row=0, column=0)
    tk.Label(auth_window, text="Senha").grid(row=1, column=0)

    user_entry = tk.Entry(auth_window)
    user_entry.grid(row=0, column=1)

    password_entry = tk.Entry(auth_window, show="*")
    password_entry.grid(row=1, column=1)

    def check_credentials():
        username = user_entry.get()
        password = password_entry.get()

        # Substitua pelos dados reais de autenticação
        if username == "admin" and password == "Qaz172839":
           # messagebox.showinfo("Sucesso", "Autenticação bem-sucedida!")
            close_window(auth_window)  # Fecha a janela de autenticação
            configure_server()  # Abre a janela de configuração
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!",  parent=auth_window)
            # Mantém a janela de autenticação aberta para tentar novamente

    tk.Button(auth_window, text="Entrar", command=check_credentials).grid(row=2, column=0, columnspan=2)
    auth_window.grab_set()


def configure_server():
    server_ip, domain, last_user, enable_usb, enable_sound, enable_printer, enable_drives, protocol = load_config()

    config_window = tk.Toplevel()
    config_window.title("Configurar Servidor")
    center_window(config_window, width=290, height=330)  # Janela ajustada para o tamanho dos botões
    config_window.resizable(False, False)  # Desativa o redimensionamento para manter o tamanho fixo

    tk.Label(config_window, text="IP do Servidor").grid(row=0, column=0)
    tk.Label(config_window, text="Domínio (opcional)").grid(row=1, column=0)
    tk.Label(config_window, text="Habilitar USB").grid(row=2, column=0)
    tk.Label(config_window, text="Habilitar Som").grid(row=3, column=0)
    tk.Label(config_window, text="Habilitar Impressoras").grid(row=4, column=0)
    tk.Label(config_window, text="Habilitar Drives").grid(row=5, column=0)
    tk.Label(config_window, text="Protocolo").grid(row=6, column=0)

    ip_entry = tk.Entry(config_window)
    ip_entry.grid(row=0, column=1)
    ip_entry.insert(0, server_ip)

    domain_entry = tk.Entry(config_window)
    domain_entry.grid(row=1, column=1)
    domain_entry.insert(0, domain)

    usb_var = tk.StringVar(value=enable_usb)
    sound_var = tk.StringVar(value=enable_sound)
    printer_var = tk.StringVar(value=enable_printer)
    drives_var = tk.StringVar(value=enable_drives)
    protocol_var = tk.StringVar(value=protocol)

    usb_check = tk.Checkbutton(config_window, text="Ativar", variable=usb_var, onvalue="yes", offvalue="no")
    usb_check.grid(row=2, column=1)

    sound_check = tk.Checkbutton(config_window, text="Ativar", variable=sound_var, onvalue="yes", offvalue="no")
    sound_check.grid(row=3, column=1)

    printer_check = tk.Checkbutton(config_window, text="Ativar", variable=printer_var, onvalue="yes", offvalue="no")
    printer_check.grid(row=4, column=1)

    drives_check = tk.Checkbutton(config_window, text="Ativar", variable=drives_var, onvalue="yes", offvalue="no")
    drives_check.grid(row=5, column=1)

    protocol_options = ["xfreerdp", "vnc", "nomachine"]
    protocol_menu = tk.OptionMenu(config_window, protocol_var, *protocol_options)
    protocol_menu.grid(row=6, column=1)

    def submit():
        new_server_ip = ip_entry.get()
        new_domain = domain_entry.get()
        new_enable_usb = usb_var.get()
        new_enable_sound = sound_var.get()
        new_enable_printer = printer_var.get()
        new_enable_drives = drives_var.get()
        new_protocol = protocol_var.get()

        if new_server_ip:
            save_config(new_server_ip, new_domain, last_user, new_enable_usb, new_enable_sound, new_enable_printer, new_enable_drives, new_protocol)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            close_window(config_window)

    tk.Button(config_window, text="Salvar", command=submit).grid(row=7, column=0)
    tk.Button(config_window, text="Voltar", command=lambda: close_window(config_window)).grid(row=7, column=1)

    config_window.grab_set()

def show_main_window():
    root = tk.Tk()
    root.title("Menu Principal")

    center_window(root, width=740, height=460)

    welcome_label = tk.Label(root, text="Bem-vindo ao servidor de terminal da RIOPARAISO/BABYBEEF", font=("Arial", 14))
    welcome_label.pack(pady=10)

    from tkinter import PhotoImage

    logo_image = PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo_image)
    logo_label.pack(pady=20)

    btn_connect = tk.Button(root, text="Conectar", command=connect)
    btn_connect.pack(fill="x", padx=20, pady=5)

    btn_configure = tk.Button(root, text="Configurar Servidor", command=authenticate)
    btn_configure.pack(fill="x", padx=20, pady=5)

    btn_shutdown = tk.Button(root, text="Desligar", command=shutdown_system)
    btn_shutdown.pack(fill="x", padx=20, pady=5)

    btn_reboot = tk.Button(root, text="Reiniciar", command=reboot_system)
    btn_reboot.pack(fill="x", padx=20, pady=5)

    root.mainloop()

if __name__ == "__main__":
    show_main_window()


