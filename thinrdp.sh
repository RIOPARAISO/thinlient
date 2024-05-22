#/bin/bash#
# configure o teclado  o time zone e relogio
#
#

apt update
apt install xserver-xorg yad xinit lightdm-remote-session-freerdp2 gpm ntpdate
wget  https://raw.githubusercontent.com/RIOPARAISO/thinlient/main/.xinitrc?token=GHSAT0AAAAAACSUQPVBTIVAF4ZBUL4QSMACZSOB24Q
mv .xinitrc\?token\=GHSAT0AAAAAACSUQPVBTIVAF4ZBUL4QSMACZSOB24Q /home/pi/.xinitrc
echo sudo startx  >> /home/pi/.bashrc
echo exit >> /home/pi/.bashrc
