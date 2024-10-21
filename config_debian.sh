#!/bin/bash

# Verifique se o script está sendo executado como root
if [ "$(id -u)" != "0" ]; then
    echo "Este script deve ser executado como root ou com sudo!" 1>&2
    exit 1
fi

# Atualizar repositórios e pacotes
echo "Atualizando os pacotes do sistema..."
apt update && apt upgrade -y

# 1. Instalação do RealVNC Server
echo "Instalando o RealVNC Server..."
wget https://www.realvnc.com/download/file/vnc.files/VNC-Server-6.7.2-Linux-x64.deb -O /tmp/VNC-Server.deb
dpkg -i /tmp/VNC-Server.deb
apt --fix-broken install -y  # Corrigir dependências, se necessário

# 2. Instalação do Python3
echo "Instalando Python 3..."
apt install -y python3 python3-pip

# 3. Instalação do LXDE e LXDM (para gerenciar login gráfico)
echo "Instalando o LXDE e LXDM (gerenciador de login leve)..."
apt install -y lxde lxdm

# 4. Configuração do teclado para Português ABNT2
echo "Configurando o teclado para Português (ABNT2)..."
localectl set-keymap br-abnt2

# 5. Configuração do fuso horário para São Paulo
echo "Configurando o fuso horário para São Paulo (Brasil)..."
timedatectl set-timezone America/Sao_Paulo

# 6. Pedir para o usuário o nome e a senha do novo usuário
read -p "Digite o nome do novo usuário: " USERNAME
read -sp "Digite a senha para o usuário $USERNAME: " PASSWORD
echo

# Verifica se o usuário já existe
if id "$USERNAME" &>/dev/null; then
    echo "O usuário $USERNAME já existe."
else
    echo "Criando o usuário $USERNAME..."
    useradd -m -s /bin/bash "$USERNAME"

    # Configura a senha do usuário
    echo "$USERNAME:$PASSWORD" | chpasswd

    # Adiciona o usuário ao grupo sudo
    usermod -aG sudo "$USERNAME"

    echo "Usuário $USERNAME criado com sucesso com permissões de sudo!"
fi

# 7. Habilitar o VNC Server
echo "Habilitando e iniciando o VNC Server..."
systemctl enable vncserver-x11-serviced.service
systemctl start vncserver-x11-serviced.service

# 8. Configuração de autologin no LXDM para o usuário 'pi'
echo "Configurando o autologin no LXDM para o usuário 'pi'..."
sed -i 's/# autologin=.*/autologin=pi/' /etc/lxdm/lxdm.conf

# 9. Criar atalho para autostart com o endereço /home/pi/thinclient/main.py
AUTOSTART_DIR="/home/pi/.config/autostart"
mkdir -p "$AUTOSTART_DIR"
echo "Criando atalho de autostart para /home/pi/thinclient/main.py..."

cat <<EOL > "$AUTOSTART_DIR/thinclient.desktop"
[Desktop Entry]
Type=Application
Exec=python3 /home/pi/thinclient/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=ThinClient
Comment=Autostart ThinClient application
EOL

# Corrigir permissões para o diretório autostart e arquivo .desktop
chown -R pi:pi "$AUTOSTART_DIR"
chmod +x "$AUTOSTART_DIR/thinclient.desktop"

# Exibe as configurações
echo ""
echo "================================================"
echo "Configurações aplicadas:"
echo "Teclado: Português (ABNT2)"
echo "Fuso horário: $(timedatectl | grep 'Time zone')"
echo "Usuário criado: $USERNAME"
echo "RealVNC Server: Instalado e Ativo"
echo "Python 3: $(python3 --version)"
echo "LXDE: Instalado"
echo "LXDM: Instalado e autologin configurado para o usuário 'pi'"
echo "Autostart: Script /home/pi/thinclient/main.py configurado"
echo "================================================"
