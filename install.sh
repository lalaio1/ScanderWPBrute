#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "Por favor, execute este script como root (sudo)." >&2
    exit 1
fi

command -v python3 >/dev/null 2>&1 || { echo "Python3 não está instalado."; exit 1; }
command -v pip >/dev/null 2>&1 || { echo "Pip não está instalado."; exit 1; }

REPO_URL="https://github.com/lalaio1/ScanderWPBrute"
INSTALL_DIR="/etc/ScanderWPBrute"
SCRIPT_NAME="ScanderWPBrute.sh"
BIN_NAME="ScanderWPBrute"
PYTHON_SCRIPT="ScanderWPBrute.py"
BIN_PATH="/usr/local/bin"


echo "[+] Clonando repositório..."
git clone "$REPO_URL" || { echo "Erro ao clonar o repositório."; exit 1; }

echo "[+] Criando diretório de instalação em $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR" || { echo "Erro ao criar diretório."; exit 1; }

echo "[+] Movendo arquivos para $INSTALL_DIR..."
mv ScanderWPBrute/* "$INSTALL_DIR" || { echo "Erro ao mover os arquivos."; exit 1; }
rm -rf ScanderWPBrute

echo "[+] Instalando dependências..."
cd "$INSTALL_DIR" || { echo "Erro ao acessar $INSTALL_DIR."; exit 1; }
pip install -r requirements.txt || { echo "Erro ao instalar dependências."; exit 1; }

echo "[+] Criando script de inicialização..."
cat <<'EOF' > "$INSTALL_DIR/$SCRIPT_NAME"
#!/bin/bash
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 não encontrado. Certifique-se de que está instalado e no PATH." >&2
    exit 1
fi

INSTALL_DIR="/etc/ScanderWPBrute"
PYTHON_SCRIPT="ScanderWPBrute.py"

python3 "$INSTALL_DIR/$PYTHON_SCRIPT" "$@"
EOF

chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

echo "[+] Movendo script para $BIN_PATH..."
mv "$INSTALL_DIR/$SCRIPT_NAME" "$BIN_PATH/$BIN_NAME" || { echo "Erro ao mover o binário."; exit 1; }

echo "[+] Configurando permissões..."
chmod +x "$BIN_PATH/$BIN_NAME"
chown root:root "$BIN_PATH/$BIN_NAME"
chmod 755 "$BIN_PATH/$BIN_NAME"

echo "[+] Comando 'ScanderWPBrute' instalado com sucesso! Execute-o com 'sudo ScanderWPBrute'."
