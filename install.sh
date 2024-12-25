#!/bin/bash

# Verificar se o script está sendo executado como root
if [[ $EUID -ne 0 ]]; then
    echo "Por favor, execute este script como root (sudo)." >&2
    exit 1
fi

command -v python3 >/dev/null 2>&1 || { echo "Python3 não está instalado."; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "Pip não está instalado."; exit 1; }

# Variáveis
REPO_URL="https://github.com/lalaio1/ScanderWPBrute"
INSTALL_DIR="/etc/ScanderWPBrute"
SCRIPT_NAME="ScanderWPBrute.sh"
BIN_NAME="ScanderWPBrute.bin"
PYTHON_SCRIPT="ScanderWPBrute.py"
BIN_PATH="/usr/local/bin"

# Clonar o repositório
echo "[+] Clonando repositório..."
git clone "$REPO_URL" || { echo "Erro ao clonar o repositório."; exit 1; }

# Criar o diretório de instalação
echo "[+] Criando diretório de instalação em $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR" || { echo "Erro ao criar diretório."; exit 1; }

# Mover os arquivos para o diretório de instalação
echo "[+] Movendo arquivos para $INSTALL_DIR..."
mv ScanderWPBrute/* "$INSTALL_DIR" || { echo "Erro ao mover os arquivos."; exit 1; }
rm -rf ScanderWPBrute

# Instalar dependências
echo "[+] Instalando dependências..."
cd "$INSTALL_DIR" || { echo "Erro ao acessar $INSTALL_DIR."; exit 1; }
pip install -r requirements.txt || { echo "Erro ao instalar dependências."; exit 1; }

# Criar o script de inicialização
echo "[+] Criando script de inicialização..."
cat <<'EOF' > "$SCRIPT_NAME"
#!/bin/bash
# Verificar se o Python3 está instalado
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 não encontrado. Certifique-se de que está instalado e no PATH." >&2
    exit 1
fi

INSTALL_DIR="/etc/ScanderWPBrute"
PYTHON_SCRIPT="ScanderWPBrute.py"

# Executar o script Python com os argumentos passados
python3 "$INSTALL_DIR/$PYTHON_SCRIPT" "$@"
EOF

chmod +x "$SCRIPT_NAME"

# Compilar o script para um binário usando `shc` (certifique-se de ter `shc` instalado)
echo "[+] Compilando o script em binário..."
apt-get install -y shc || { echo "Erro ao instalar o shc."; exit 1; }
shc -f "$SCRIPT_NAME" -o "$BIN_NAME" || { echo "Erro ao compilar o script."; exit 1; }

# Mover o binário para o PATH
echo "[+] Movendo binário para $BIN_PATH..."
mv "$BIN_NAME" "$BIN_PATH/ScanderWPBrute" || { echo "Erro ao mover o binário."; exit 1; }

# Configurar permissões para que apenas o sudo possa executar o binário
echo "[+] Configurando permissões..."
chmod +x "$BIN_PATH/ScanderWPBrute"
chown root:root "$BIN_PATH/ScanderWPBrute"
chmod 755 "$BIN_PATH/ScanderWPBrute"

# Finalizar
echo "[+] Comando 'ScanderWPBrute' instalado com sucesso! Execute-o com 'sudo ScanderWPBrute'."
