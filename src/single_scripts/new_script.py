import os
import shutil
from tkinter import Tk, filedialog, messagebox

def start() :
    file_path = pick_and_copy_file() # Paso 0: Abrir el archivo a procesar
    if not file_path: return
    
    filter_inputs = get_filter_inputs() # Paso 1: Solicitar criterios de filtro
    

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
    input_folder_path = get_input_folder() # Crea/ obtiene el path al directorio de input
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


def get_input_folder():
    # Obtener el directorio raíz del proyecto (el directorio actual)
    project_root = os.getcwd()
    
    # Crear la carpeta "input" en el root del proyecto si no existe
    folder = os.path.join(project_root, "input")
    os.makedirs(folder, exist_ok=True)
    return folder

def get_filter_inputs():
    print("Input filter criteria (Format example: \"NVDA ASUS MSFT, INTL\" will generate a file with msgs that contain first 3 items, and another one that contain INTL)")
    string_input = input() 
    print(string_input)
    item_split_input = [item.strip().split() for item in string_input.split(",")]
    print(item_split_input)
    return item_split_input

