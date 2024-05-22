#!/bin/bash

# Função para coletar informações do usuário com YAD
collect_info() {
    response=$(yad --form --height=100 --width=400 \
        --title="Conectar com Sevidor" \
        --field="Usuário ":CE \
        --field="Senha":H \
        "" "" "")
    # Checar se o usuário cancelou o diálogo
    if [ $? -ne 0 ]; then
        echo "Operação cancelada."
        exit 1
    fi

    # Separar as respostas do YAD
    IFS="|" read -r USER PASSWORD DOMAIN <<< "$response"
}

# Coletar informações do usuário
collect_info

# Montar o comando xfreerdp com as informações coletadas
xfreerdp /v:[192.168.0.10] /u:"$USER" /p:"$PASSWORD"  /f " > /home/pi/.xinit 
