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
    
    generate_outputs(file_path, filter_inputs) # Paso 2: Procesar el archivo y generar 
    
    input("Processing done. Press Enter to close...") 


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
        print("Last directory opened not found. Setting initial directory to Desktop.")
    return os.path.join(os.path.expanduser("~"), "Desktop")  # Valor predeterminad


def save_last_directory(directory):
    """Guarda el último directorio utilizado en el registro."""
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            winreg.SetValueEx(key, LAST_DIR_KEY, 0, winreg.REG_SZ, directory)
    except Exception as e:
        print(f"Error saving to registry: {e}")


def get_last_input():
    """Obtiene el último valor de entrada desde el registro."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ) as key:
            return winreg.QueryValueEx(key, LAST_INPUT_KEY)[0]
    except FileNotFoundError:
        return ""  # Devuelve una cadena vacía si no hay ningún valor guardado


def save_last_input(input_value):
    """Guarda el último valor de entrada en el registro."""
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            winreg.SetValueEx(key, LAST_INPUT_KEY, 0, winreg.REG_SZ, input_value)
    except Exception as e:
        print(f"Error saving to registry: {e}")


def get_filter_inputs():
    """Solicita al usuario los criterios de filtro y guarda el último valor ingresado."""
    last_input = get_last_input()
    if not last_input or last_input.strip() == "":
        last_input = "None"
    
    print("\nInput filter criteria. Format example: \"NVDA ASUS MSFT, INTL\" will generate a file with fix-msgs that contain first 3 items, and another one that contain the 4th one)")
    print(f"\nDo you want to apply filters? (Y/N, N by default)")
    filter_input = input()
    if len(filter_input) > 0 and str(filter_input[0]).lower() != "y":
        return dict()
    
    print(f"\nEnter filter criteria, \"{last_input}\" selected by default:")
    string_input = input()
    if not string_input:  # Si el input es vacío, usa el último valor
        string_input = last_input
        
    if string_input.strip() == "" or string_input == "None":  # Si hay un nuevo valor, guárdalo
        save_last_input("None")
        return dict()
    
    save_last_input(string_input)
    item_split_input = [item.strip().split() for item in string_input.split(",")]
    filtered_files_dict = {" ".join(key): [] for key in item_split_input}
    return filtered_files_dict


def generate_outputs(file_path: str, filters_dict: dict[str, list[tuple[int,str]]]) -> None:
    header = []
    unfiltered = []
    securitylist = []
    error_misc = []
    
    folder_path = get_output_folder(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    print("\nDo you want to process unfiltered lines? (Y/N, N by default)")
    unfiltered_input = input()
    generate_unfiltered = len(unfiltered_input) > 0 and str(unfiltered_input[0]).lower() == "y"
    


    with open(file_path, 'r') as file:
        lines = file.readlines()

        i = 0
        while i < len(lines):
            line = (i, lines[i].strip())
            
            if "35=y" in line[1]:
                securitylist.append(line)
                i += 1
                continue

            if "--------------- USER CON" in line[1]:
                if i > 0:
                    header.append((i - 1, lines[i - 1].strip()))
                if len(error_misc) > 0:
                    error_misc.pop()

                header.append(line)

                for j in range(1, 9):
                    if i + j < len(lines):
                        header.append((i + j, lines[i + j].strip()))
                i += 9
                continue

            is_done = False
            for key in filters_dict.keys():
                for filter in key.split():
                    if filter in line[1]:
                        filters_dict[key].append(line)
                        is_done = True
            if is_done: 
                i += 1
                continue

            if "8=FIXT.1.1" in line[1]:
                if generate_unfiltered:
                    unfiltered.append(line)
                i += 1
                continue

            error_misc.append(line)
            i += 1

    header_str = set_row_index(header, True)
    generate_file(folder_path, f"{file_name} - errors_misc", header_str, set_row_index(error_misc, True))
    generate_file(folder_path, f"{file_name} - securitylist", header_str, set_row_index(securitylist, True))
    for key in filters_dict.keys():
        generate_file(folder_path, f"{file_name} - filtered by {key}", header_str, set_row_index(filters_dict[key]))
    if generate_unfiltered:
        generate_file(folder_path, f"{file_name} - unfiltered", header_str, set_row_index(unfiltered))


def set_row_index(error_misc, jump_row = False):
    result = []
    prev_i = -1
    for i_line in error_misc:
        if jump_row and prev_i != -1 and i_line[0] != prev_i + 1:
            result.append("")
        result.append(f"{i_line[0]}.- {i_line[1]}")
        prev_i = i_line[0]
    return result


def get_output_folder(file_path):
    project_root = os.getcwd() # Obtener el directorio raíz del proyecto (el directorio actual)
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
        output_file.writelines("\n\n")
        output_file.writelines("\n".join(content))

if __name__ == "__main__":
    start()
