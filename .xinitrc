#!/bin/bash

# Arquivo para salvar as configurações
CONFIG_FILE="$HOME/.xfreerdp_config"

# Função para coletar informações do usuário com YAD
collect_info() {
    response=$(yad --center --form --height=200 --width=400 \
        --title="Conectar com Servidor" \
        --field="Usuário ":CE \
        --field="Senha":H \
        "" "")

    # Checar se o usuário cancelou o diálogo
    if [ $? -ne 0 ]; then
        echo "Operação cancelada."
        exit 1
    fi

    # Separar as respostas do YAD
    IFS="|" read -r USER PASSWORD <<< "$response"
}

# Função para configurar o servidor e salvar em um arquivo
configure_server() {
    # Pedir a senha para acessar as configurações
    PASS=$(yad --center --entry --hide-text --text="Digite a senha para acessar as configurações" --title="Autenticação")
    
    if [ "$PASS" != "minhasenha" ]; then
        yad --center --text="Senha incorreta!" --title="Erro" --button=OK
        exit 1
    fi

    # Coletar as novas configurações
    config_response=$(yad --center --form --height=200 --width=400 \
        --title="Configurar Servidor" \
        --field="IP do Servidor" \
        --field="Domínio (opcional)" \
        "192.168.0.10" "")

    if [ $? -ne 0 ]; then
        echo "Operação de configuração cancelada."
        exit 1
    fi

    # Separar as respostas do YAD
    IFS="|" read -r SERVER_IP DOMAIN <<< "$config_response"

    # Salvar as configurações em um arquivo protegido
    echo "SERVER_IP=\"$SERVER_IP\"" > "$CONFIG_FILE"
    echo "DOMAIN=\"$DOMAIN\"" >> "$CONFIG_FILE"

    yad --center --text="Configurações salvas com sucesso!" --title="Sucesso" --button=OK
}

# Função para carregar as configurações do arquivo
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    else
        # Se o arquivo de configuração não existir, usar valores padrão
        SERVER_IP="192.168.0.10"
        DOMAIN=""
    fi
}

# Menu principal para escolher entre conectar ou configurar
main_menu() {
    choice=$(yad --center --list --radiolist --column="Opção" --column="Ação" TRUE "Conectar ao servidor" FALSE "Configurar servidor" --height=200 --width=400 --title="Menu Principal")

    if [ $? -ne 0 ]; then
        echo "Operação cancelada."
        exit 1
    fi

    case $choice in
        "Conectar ao servidor")
            collect_info
            ;;
        "Configurar servidor")
            configure_server
            exit 0
            ;;
        *)
            echo "Opção inválida."
            exit 1
            ;;
    esac
}

# Carregar as configurações
load_config

# Exibir o menu principal
main_menu

# Montar o comando xfreerdp com as informações coletadas
xfreerdp /v:"$SERVER_IP" /u:"$USER" /p:"$PASSWORD" /f /cert-ignore +clipboard +fonts /gdi:hw
