import os

# Caminho para o arquivo de configuração
CONFIG_FILE = os.path.expanduser("~/.xfreerdp_config")

def load_config():
    """Carrega as configurações do arquivo"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = {}
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config[key] = value.strip('"')
            return (
                config.get("SERVER_IP", "192.168.0.10"),
                config.get("DOMAIN", ""),
                config.get("LAST_USER", ""),
                config.get("ENABLE_USB", "no"),
                config.get("ENABLE_SOUND", "no"),
                config.get("ENABLE_PRINTER", "no"),
                config.get("ENABLE_DRIVES", "no"),
                config.get("PROTOCOL", "xfreerdp")
            )
    else:
        # Configurações padrão
        return "192.168.0.10", "", "", "no", "no", "no", "no", "xfreerdp"

def save_config(server_ip, domain, last_user, enable_usb, enable_sound, enable_printer, enable_drives, protocol):
    """Salva as configurações no arquivo"""
    with open(CONFIG_FILE, "w") as f:
        f.write(f'SERVER_IP="{server_ip}"\n')
        f.write(f'DOMAIN="{domain}"\n')
        f.write(f'LAST_USER="{last_user}"\n')
        f.write(f'ENABLE_USB="{enable_usb}"\n')
        f.write(f'ENABLE_SOUND="{enable_sound}"\n')
        f.write(f'ENABLE_PRINTER="{enable_printer}"\n')
        f.write(f'ENABLE_DRIVES="{enable_drives}"\n')
        f.write(f'PROTOCOL="{protocol}"\n')
