#/bin/bash#
# configure o teclado  o time zone e relogio
#
#

apt update && apt install xserver-xorg yad xinit lightdm-remote-session-freerdp2 gpm ntpdate -y  
wget https://raw.githubusercontent.com/RIOPARAISO/thinlient/main/.xinitrc
chmod +x /home/pi/.xinitrc
echo startx  >> /home/pi/.bashrc
echo exit >> /home/pi/.bashrc

sudo adduser -m -s /bin/bash --home /home/adminsys adminsys 
password adminsys
