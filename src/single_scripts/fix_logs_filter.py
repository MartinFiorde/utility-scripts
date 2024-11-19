import os
import shutil
import winreg
from tkinter import filedialog

REGISTRY_PATH = r"SOFTWARE\\JavaSoft\\Prefs\\filterScript"
LAST_DIR_KEY = "LastUsedDir"

def start() :
    file_path = pick_and_copy_file() # Paso 0: Abrir el archivo a procesar
    if not file_path: return
    
    filter_inputs = get_filter_inputs() # Paso 1: Solicitar criterios de filtro
    
    generate_outputs(file_path, filter_inputs) # Paso 2: Solicitar criterios de filtro
    
    input("Done. Press Enter to close...") 


def pick_and_copy_file():
    initial_dir = get_last_directory()
    
    original_file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="Selecciona un archivo",
        filetypes=(("Archivos permitidos", "*.reg *.log *.txt"),)
    ) # Abre el cuadro de diálogo para seleccionar un archivo
    
    if not original_file_path:
        print("No file selected")
        return None
    
    save_last_directory(os.path.dirname(original_file_path))
    
    filename, extension = os.path.splitext(os.path.basename(original_file_path)) # Obtiene el nombre y extension del archivo
    input_folder_path = get_input_folder() # Crea/ obtiene el path al directorio de input
    new_file_path = os.path.join(input_folder_path, f"{filename}{extension}") # Crear el path inicial
    
    i = 1
    while os.path.exists(new_file_path): # Incrementar el sufijo si el archivo ya existe
        new_file_path = os.path.join(input_folder_path, f"{filename} ({i}){extension}")
        i += 1

    shutil.copy(original_file_path, new_file_path) # Copiar el archivo al nuevo path

    return new_file_path


def get_last_directory():
    # os.path.join(os.path.expanduser("~"), "Desktop") # Establece el directorio inicial en el Escritorio del usuario
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ) as key:
            last_dir = winreg.QueryValueEx(key, LAST_DIR_KEY)[0]
            if os.path.exists(last_dir):  # Verificar que el directorio aún existe
                return last_dir
    except FileNotFoundError:
        print("Conection to SO winreg error. Setting initial directory to Desktop by default.")
    return os.path.join(os.path.expanduser("~"), "Desktop")  # Valor predeterminad


def save_last_directory(directory):
    """Guarda el último directorio utilizado en el registro."""
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            winreg.SetValueEx(key, LAST_DIR_KEY, 0, winreg.REG_SZ, directory)
    except Exception as e:
        print(f"Error saving to registry: {e}")


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
    item_split_input = [item.strip().split() for item in string_input.split(",")]
    return item_split_input


def generate_outputs(file_path, filters):
    header = []
    unfiltered = []
    securitylist = []
    error_misc = []
    filtered_files = {" ".join(key): [] for key in filters}
    if len(filtered_files) == 1 and "" in filtered_files: 
        filtered_files = dict()
    
    out_folder_path = get_out_folder(file_path)         

    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        i = 0
        while i < len(lines):
            line = f"{i}.- {lines[i].strip()}"
            
            if "35=y" in line:
                securitylist.append(line)
                i += 1
                continue
            
            if "--------------- USER CON" in line:
                if i > 0:
                    header.append(f"{i - 1}.- {lines[i - 1].strip()}")
                if len(error_misc) > 0:
                    error_misc.pop()

                header.append(line)
                
                for j in range(1, 9):
                    if i + j < len(lines):
                        header.append(f"{i + j}.- {lines[i + j].strip()}")
                i += 9
                continue

            is_done = False
            for key in filtered_files.keys():
                for filter in key.split():
                    if filter in line:
                        filtered_files[key].append(line)
                        is_done = True
            if is_done: 
                i += 1
                continue
                    
            if "8=FIXT.1.1" in line:
                unfiltered.append(line)
                i += 1
                continue

            error_misc.append(line)
            i += 1
            
    
    generate_file(out_folder_path, "errors_misc", header, error_misc)
    generate_file(out_folder_path, "securitylist", header, securitylist)
    generate_file(out_folder_path, "unfiltered", header, unfiltered)
    for key in filtered_files.keys():
        generate_file(out_folder_path, f"filtered by {key}", header, filtered_files[key])


def get_out_folder(file_path):
    # Obtener el directorio raíz del proyecto (el directorio actual)
    project_root = os.getcwd()
    
    # Crear la carpeta "input" en el root del proyecto si no existe
    folder = os.path.join(project_root, "out")
    folder = os.path.join(folder, os.path.basename(file_path))
    os.makedirs(folder, exist_ok=True)
    return folder

def generate_file(dir_path, name, header, content):
    print(f"LENGTH CONTENT {name}: {len(content)}")
    output_file_path = os.path.join(dir_path, f'{name}.log')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines("\n".join(header))
        output_file.writelines("\n")
        output_file.writelines("\n".join(content))
        
if __name__ == "__main__":
    start()
