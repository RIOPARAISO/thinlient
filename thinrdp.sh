#/bin/bash#
# configure o teclado  o time zone e relogio
#
#

apt update
apt install xserver-xorg yad xinit lightdm-remote-session-freerdp2 gpm ntpdate
https://raw.githubusercontent.com/RIOPARAISO/thinlient/main/.xinitrc
echo startx  >> /home/pi/.bashrc
echo exit >> /home/pi/.bashrc
