import subprocess
from tkinter import messagebox
from config_manager import save_config

def connect_to_server(server_ip, domain, last_user, enable_usb, enable_sound, enable_printer, enable_drives, protocol, user, password):
    """Tenta conectar ao servidor com o protocolo escolhido"""
    save_config(server_ip, domain, last_user, enable_usb, enable_sound, enable_printer, enable_drives, protocol)

    command = []
    if protocol == "xfreerdp":
        command = ["xfreerdp", f"/v:{server_ip}", f"/u:{user}", f"/p:{password}", "/f", "/cert-ignore", "+clipboard", "+fonts", "/gdi:hw"]
        if enable_usb == "yes":
            command.append("/usb")
        if enable_sound == "yes":
            command.append("/sound:sys:alsa")
        if enable_printer == "yes":
            command.append("/printer")
        if enable_drives == "yes":
            command.append("/drive:media,/media")
    elif protocol == "vnc":
        command = ["vncviewer", server_ip]
    elif protocol == "nomachine":
        command = ["nxplayer", "--session", server_ip]

    try:
        with open("connection_output.log", "w") as log_file:
            subprocess.run(command, check=True, stdout=log_file, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", f"Falha ao conectar usando o protocolo {protocol}. Verifique as credenciais ou a conectividade caso persista contacte o TI.")
    except FileNotFoundError:
        messagebox.showerror("Erro", f"O comando para o protocolo {protocol} não foi encontrado. Verifique se ele está instalado.")
