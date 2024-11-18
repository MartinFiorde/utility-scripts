import os
import shutil
from tkinter import Tk, filedialog, messagebox

def start() :
    
    print("hello world")
    file_path = pick_and_copy_file()
    if not file_path: return
    

def pick_and_copy_file():
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop") # Establece el directorio inicial en el Escritorio del usuario
    original_file_path = filedialog.askopenfilename(
        initialdir=desktop_dir,
        title="Selecciona un archivo",
        filetypes=(("Archivos permitidos", "*.reg *.log *.txt"),)
    ) # Abre el cuadro de diálogo para seleccionar un archivo
    
    if not original_file_path:
        print("No file selected")
        return None
    
    filename, extension = os.path.splitext(os.path.basename(original_file_path)) # Obtiene el nombre y extension del archivo
    input_folder_path = input_folder() # Crea/ obtiene el path al directorio de input
    new_file_path = os.path.join(input_folder_path, f"{filename}{extension}") # Crear el path inicial
    
    i = 1
    while os.path.exists(new_file_path): # Incrementar el sufijo si el archivo ya existe
        new_file_path = os.path.join(input_folder_path, f"{filename} ({i}){extension}")
        i += 1

    shutil.copy(original_file_path, new_file_path) # Copiar el archivo al nuevo path

    # Imprime la ruta del archivo seleccionado (o None si no se seleccionó nada)
    print("Archivo seleccionado:", original_file_path)
    print("Archivo copiado:", new_file_path)
    return new_file_path


def input_folder():
    # Obtener el directorio raíz del proyecto (el directorio actual)
    project_root = os.getcwd()
    
    # Crear la carpeta "input" en el root del proyecto si no existe
    input_folder = os.path.join(project_root, "input")
    os.makedirs(input_folder, exist_ok=True)
    return input_folder
