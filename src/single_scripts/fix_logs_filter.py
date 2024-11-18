import os
import shutil
from tkinter import Tk, filedialog, messagebox

def start() :
    file_path = pick_and_copy_file() # Paso 0: Abrir el archivo a procesar
    if not file_path: return
    
    filter_inputs = get_filter_inputs() # Paso 1: Solicitar criterios de filtro
    
    generate_outputs(file_path, filter_inputs) # Paso 2: Solicitar criterios de filtro


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
    item_split_input = [item.strip().split() for item in string_input.split(",")]
    return item_split_input

def generate_outputs(file_path, filters):
    header = []
    unfiltered = []
    filtered_files = {" ".join(key): [] for key in filters}
    if len(filtered_files) == 1 and "" in filtered_files: filtered_files = dict()
    securitylist = []
    error_misc = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if "35=y" in line:
                securitylist.append(line)
                i += 1
                continue
            
            if "- USER CONNECTION" in line:
                if i > 0:
                    header.append(lines[i - 1].strip())
                if len(error_misc) > 0:
                    error_misc.pop()

                header.append(line)
                
                for j in range(1, 9):
                    if i + j < len(lines):
                        header.append(lines[i + j].strip())
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
            
    out_folder_path = get_out_folder(file_path)         
    
    generate_file(out_folder_path, "errors_misc", header, error_misc)
    generate_file(out_folder_path, "securitylist", header, securitylist)
    generate_file(out_folder_path, "unfiltered", header, unfiltered)
    for key in filtered_files.keys():
        generate_file(out_folder_path, f"filtered by {key}", header, filtered_files[key])
    pass

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
