import os
from tkinter import Tk, filedialog

# Oculta la ventana principal de Tkinter
root = Tk()
root.withdraw()

# Establece el directorio inicial en el Escritorio del usuario
desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

# Abre el cuadro de diálogo para seleccionar un archivo
file_path = filedialog.askopenfilename(
    initialdir=desktop_dir,
    title="Selecciona un archivo",
    filetypes=(("Archivos permitidos", "*.reg *.log *.txt"),)
)

# Imprime la ruta del archivo seleccionado (o None si no se seleccionó nada)
print("Archivo seleccionado:", file_path)