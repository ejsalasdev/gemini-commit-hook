#!/bin/bash

# Script de instalación global para gemini-commit-hook

GLOBAL_INSTALL_DIR="$HOME/.local/share/gemini-commit-hook"
GLOBAL_BIN_DIR="$HOME/.local/bin"
GLOBAL_VENV_DIR="$GLOBAL_INSTALL_DIR/venv"

function error_exit() {
    echo "Error: $1" >&2
    exit 1
}

echo "Iniciando instalación global de gemini-commit-hook..."

mkdir -p "$GLOBAL_INSTALL_DIR" || error_exit "No se pudo crear el directorio de instalación: $GLOBAL_INSTALL_DIR"
mkdir -p "$GLOBAL_BIN_DIR" || error_exit "No se pudo crear el directorio bin: $GLOBAL_BIN_DIR"

echo "Directorios creados/verificados."

echo "Creando entorno virtual en $GLOBAL_VENV_DIR..."
if [ -d "$GLOBAL_VENV_DIR" ]; then
    echo "El entorno virtual ya existe. Saltando la creación y la instalación de dependencias."
else
    python3 -m venv "$GLOBAL_VENV_DIR" || error_exit "No se pudo crear el entorno virtual."
    echo "Instalando 'requests' en el entorno virtual..."
    "$GLOBAL_VENV_DIR/bin/pip" install requests || error_exit "No se pudo instalar 'requests'."
fi

echo "Entorno virtual configurado."

echo "Copiando scripts a $GLOBAL_INSTALL_DIR..."
cp "src/gemini_hook/main.py" "$GLOBAL_INSTALL_DIR/main.py" || error_exit "No se pudo copiar main.py."
cp "src/gemini_hook/prompt_guide.md" "$GLOBAL_INSTALL_DIR/prompt_guide.md" || error_exit "No se pudo copiar prompt_guide.md."

echo "Actualizando shebang en $GLOBAL_INSTALL_DIR/main.py..."
sed -i "1s|.*|#!$GLOBAL_VENV_DIR/bin/python3|" "$GLOBAL_INSTALL_DIR/main.py" || error_exit "No se pudo actualizar el shebang."

echo "Actualizando rutas en src/install_repo_hook..."
TEMP_INSTALL_HOOK_SCRIPT=$(mktemp)
sed "s|HOOK_SCRIPT_SRC=.*|HOOK_SCRIPT_SRC=\"$GLOBAL_INSTALL_DIR/main.py\"|" "src/install_repo_hook" > "$TEMP_INSTALL_HOOK_SCRIPT"
sed -i "s|PROMPT_GUIDE_SRC=.*|PROMPT_GUIDE_SRC=\"$GLOBAL_INSTALL_DIR/prompt_guide.md\"|" "$TEMP_INSTALL_HOOK_SCRIPT"
cp "$TEMP_INSTALL_HOOK_SCRIPT" "src/install_repo_hook" || error_exit "No se pudo actualizar install_repo_hook."
rm "$TEMP_INSTALL_HOOK_SCRIPT"

echo "Copiando install_repo_hook a $GLOBAL_BIN_DIR..."
cp "src/install_repo_hook" "$GLOBAL_BIN_DIR/install_repo_hook" || error_exit "No se pudo copiar install_repo_hook a ~/.local/bin."

echo "Haciendo scripts ejecutables..."
chmod +x "$GLOBAL_INSTALL_DIR/main.py" || error_exit "No se pudo hacer ejecutable main.py."
chmod +x "$GLOBAL_BIN_DIR/install_repo_hook" || error_exit "No se pudo hacer ejecutable install_repo_hook."

# Verificar si ~/.local/bin está en el PATH
if [[ ":$PATH:" != *":$GLOBAL_BIN_DIR:"* ]]; then
    echo ""
    echo "¡Advertencia: '$GLOBAL_BIN_DIR' no está en tu variable de entorno PATH!"
    echo "Para poder ejecutar 'install_repo_hook' directamente, necesitas añadirlo."
    echo "Puedes hacerlo añadiendo la siguiente línea a tu archivo de configuración de shell (por ejemplo, ~/.zshrc o ~/.bashrc):"
    echo ""
    echo "    export PATH=\"$GLOBAL_BIN_DIR:\$PATH\""
    echo ""
    echo "Luego, recarga tu shell con 'source ~/.zshrc' (o el archivo correspondiente) o abre una nueva terminal."
    echo ""
fi

echo "Instalación global completada exitosamente."
echo ""
echo "Para usarlo, asegúrate de que '$GLOBAL_BIN_DIR' esté en tu PATH."
echo "Luego, en cualquier repositorio Git, puedes ejecutar:"
echo "install_repo_hook"

echo "¡No olvides configurar tu clave API de Gemini en la variable de entorno GEMINI_API_KEY!"
