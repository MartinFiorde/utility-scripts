#!/bin/bash

if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python no está instalado en este sistema."
    echo "Por favor, instala Python desde https://www.python.org/downloads/"
    echo "O utiliza el administrador de paquetes de tu sistema (e.g., apt, yum, brew)."
    exit 1
fi

$PYTHON_CMD -m src.main

echo "Script terminado. Presiona Enter para cerrar..."
read