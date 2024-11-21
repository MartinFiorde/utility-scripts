#!/bin/bash

# Detectar si 'python' está disponible y es Python 3
if command -v python &>/dev/null && python --version 2>&1 | grep -q "Python 3"; then
    python -m src.main
# Detectar si 'python3' está disponible
elif command -v python3 &>/dev/null; then
    python3 -m src.main
else
    echo "Error: Python no está instalado en este sistema."
    echo "Por favor, instala Python desde https://www.python.org/downloads/"
    echo "O utiliza el administrador de paquetes de tu sistema (e.g., apt, yum, brew)."
    exit 1
fi

$PYTHON_CMD -m src.main

echo "Script terminado. Presiona Enter para cerrar..."
read