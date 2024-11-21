import os
import re
import shutil
import winreg
from datetime import datetime
from tkinter import Tk, filedialog


REGISTRY_PATH = r"SOFTWARE\\JavaSoft\\Prefs\\filterScript"
LAST_DIR_KEY = "LastUsedDir"
LAST_INPUT_KEY = "LastFilterInput"


MSG_TYPE_DICT = {
    "0": "Heartbeat",
    "1": "TestRequest",
    "2": "ResendRequest",
    "3": "Reject",
    "4": "SequenceReset",
    "5": "Logout",
    "6": "IOI",
    "7": "Advertisement",
    "8": "ExecutionReport",
    "9": "OrderCancelReject",
    "a": "QuoteStatusRequest",
    "A": "Logon",
    "AA": "DerivativeSecurityList",
    "AB": "NewOrderMultileg",
    "AC": "MultilegOrderCancelReplace",
    "AD": "TradeCaptureReportRequest",
    "AE": "TradeCaptureReport",
    "AF": "OrderMassStatusRequest",
    "AG": "QuoteRequestReject",
    "AH": "RFQRequest",
    "AI": "QuoteStatusReport",
    "AJ": "QuoteResponse",
    "AK": "Confirmation",
    "AL": "PositionMaintenanceRequest",
    "AM": "PositionMaintenanceReport",
    "AN": "RequestForPositions",
    "AO": "RequestForPositionsAck",
    "AP": "PositionReport",
    "AQ": "TradeCaptureReportRequestAck",
    "AR": "TradeCaptureReportAck",
    "AS": "AllocationReport",
    "AT": "AllocationReportAck",
    "AU": "Confirmation_Ack",
    "AV": "SettlementInstructionRequest",
    "AW": "AssignmentReport",
    "AX": "CollateralRequest",
    "AY": "CollateralAssignment",
    "AZ": "CollateralResponse",
    "b": "MassQuoteAcknowledgement",
    "B": "News",
    "BA": "CollateralReport",
    "BB": "CollateralInquiry",
    "BC": "NetworkCounterpartySystemStatusRequest",
    "BD": "NetworkCounterpartySystemStatusResponse",
    "BE": "UserRequest",
    "BF": "UserResponse",
    "BG": "CollateralInquiryAck",
    "BH": "ConfirmationRequest",
    "BI": "TradingSessionListRequest",
    "BJ": "TradingSessionList",
    "BK": "SecurityListUpdateReport",
    "BL": "AdjustedPositionReport",
    "BM": "AllocationInstructionAlert",
    "BN": "ExecutionAcknowledgement",
    "BO": "ContraryIntentionReport",
    "BP": "SecurityDefinitionUpdateReport",
    "c": "SecurityDefinitionRequest",
    "C": "Email",
    "d": "SecurityDefinition",
    "D": "NewOrderSingle",
    "e": "SecurityStatusRequest",
    "E": "NewOrderList",
    "f": "SecurityStatus",
    "F": "OrderCancelRequest",
    "g": "TradingSessionStatusRequest",
    "G": "OrderCancelReplaceRequest",
    "h": "TradingSessionStatus",
    "H": "OrderStatusRequest",
    "i": "MassQuote",
    "j": "BusinessMessageReject",
    "J": "AllocationInstruction",
    "k": "BidRequest",
    "K": "ListCancelRequest",
    "l": "BidResponse",
    "L": "ListExecute",
    "m": "ListStrikePrice",
    "M": "ListStatusRequest",
    "n": "XML_non_FIX",
    "N": "ListStatus",
    "o": "RegistrationInstructions",
    "p": "RegistrationInstructionsResponse",
    "P": "AllocationInstructionAck",
    "q": "OrderMassCancelRequest",
    "Q": "DontKnowTradeDK",
    "r": "OrderMassCancelReport",
    "R": "QuoteRequest",
    "s": "NewOrderCross",
    "S": "Quote",
    "t": "CrossOrderCancelReplaceRequest",
    "T": "SettlementInstructions",
    "u": "CrossOrderCancelRequest",
    "v": "SecurityTypeRequest",
    "V": "MarketDataRequest",
    "w": "SecurityTypes",
    "W": "MarketDataSnapshotFullRefresh",
    "x": "SecurityListRequest",
    "X": "MarketDataIncrementalRefresh",
    "y": "SecurityList",
    "Y": "MarketDataRequestReject",
    "z": "DerivativeSecurityListRequest",
    "Z": "QuoteCancel"
}


def start() :
    file_path = pick_and_copy_file() # Paso 0: Abrir el archivo a procesar
    if not file_path: return
    
    filter_dic = get_filter_inputs() # Paso 1: Solicitar criterios de filtro
    
    generate_outputs(file_path, filter_dic) # Paso 2: Procesar el archivo y generar 
    
    input("Processing done. Press Enter to close...") 


def pick_and_copy_file():
    initial_file_path = get_last_directory()  # Obtén el path del último archivo usado
    if os.path.isdir(initial_file_path):
        initial_dir, initial_file = initial_file_path, ""
    else:
        initial_dir, initial_file = os.path.split(initial_file_path)  # Separa el directorio y el nombre del archivo
    
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    root.attributes("-topmost", True)  # Asegura que esté en primer plano
    root.iconify()  # Minimiza la ventana principal para que no sea visible
    
    original_file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        initialfile=initial_file,
        title="Selecciona un archivo",
        filetypes=(("Archivos permitidos", "*.reg *.log *.txt"),)
    ) # Abre el cuadro de diálogo para seleccionar un archivo
    
    root.destroy()  # Cierra la ventana principal
    
    if not original_file_path:
        print("No file selected")
        return None
    
    save_last_directory(original_file_path)
    
    filename, extension = os.path.splitext(os.path.basename(original_file_path)) # Obtiene el nombre y extension del archivo
    folder_path = get_output_folder(original_file_path) # Crea/ obtiene el path al directorio de output
    new_file_path = os.path.join(folder_path, f"{filename}{extension}") # Crear el path inicial
    
    i = 1
    while os.path.exists(new_file_path): # Incrementar el sufijo si el archivo ya existe
        new_file_path = os.path.join(folder_path, f"{filename} ({i}){extension}")
        i += 1

    shutil.copy(original_file_path, new_file_path) # Copiar el archivo al nuevo path

    return new_file_path


def get_last_directory():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ) as key:
            last_dir = winreg.QueryValueEx(key, LAST_DIR_KEY)[0]
            if os.path.exists(last_dir):  # Verificar que el archivo aún existe
                return last_dir
            elif os.path.isdir(os.path.dirname(last_dir)):  # Si el archivo no existe, pero el directorio sí
                return os.path.dirname(last_dir)
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


def get_last_input() -> str:
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
    if not (len(filter_input) > 0 and str(filter_input[0]).lower() == "y"):
        save_last_input("None")
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
        print(f"LENGTH CONTENT original file: {len([s for s in lines if s])}")

        i = 0
        while i < len(lines):
            line = (i, lines[i].strip())
            
            if "35=y" in line[1]:
                securitylist.append(line)
                i += 1
                continue

            if len(header) == 0 and "--------------- USER CON" in line[1]:
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

    header_str = set_row_index(header, True) if len(header) != 0 else ["------------------ USER CONNECTION INFORMATION ------------------","------------------    NO INFORMATION FOUND     ------------------"]
    print(f"LENGTH CONTENT header: {len([s for s in header_str if s])}")
    generate_file(folder_path, f"{file_name} - errors_misc", header_str, set_row_index(error_misc, True))
    generate_file(folder_path, f"{file_name} - securitylist", header_str, set_row_index(securitylist, True))
    for key in filters_dict.keys():
        generate_file(folder_path, f"{file_name} - filtered by {key}", header_str, set_row_index(filters_dict[key]))
        generate_csv(folder_path, f"{file_name} - filtered by {key}", header_str, set_row_index(filters_dict[key]))
    if generate_unfiltered:
        generate_file(folder_path, f"{file_name} - unfiltered", header_str, set_row_index(unfiltered))
        generate_csv(folder_path, f"{file_name} - unfiltered", header_str, set_row_index(unfiltered))


def set_row_index(error_misc, jump_row = False):
    result = []
    prev_i = -1
    for i_line in error_misc:
        if jump_row and prev_i != -1 and i_line[0] != prev_i + 1:
            result.append("")
        result.append(f"{i_line[0] + 1}.- {i_line[1]}")
        prev_i = i_line[0]
    return result


def get_output_folder(file_path):
    project_root = os.getcwd() # Obtener el directorio raíz del proyecto (el directorio actual)
    folder = os.path.join(project_root, "output") # Crear la carpeta "input" en el root del proyecto si no existe
    os.makedirs(folder, exist_ok=True) # folder = os.path.join(folder, os.path.basename(file_path))
    return folder


def generate_file(dir_path, name, header, content):
    print(f"LENGTH CONTENT {name}: {len([s for s in content if s])}")
    output_file_path = os.path.join(dir_path, f'{name}.log')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines("\n".join(header))
        output_file.writelines("\n\n")
        output_file.writelines("\n".join(content))
        
def generate_csv(dir_path, name, header, content: list[str]):
    T = "\t"
    print(f"CSV GENERATION {name}")
    output_file_path = os.path.join(dir_path, f'{name}.csv')
    csv_content = [f"full row{T}instrument name{T}row n{T}local date (yyyy-mm-dd hh:mm:ss.000){T}minutes in seconds.microseconds{T}msg head{T}'8{T}BeginString{T}'9{T}BodyLength{T}'35{T}MsgType{T}MSG TYPE TITLE{T}'34{T}MsgSeqNum{T}'49{T}SenderCompId{T}'52{T}SendingTime{T}minutes in seconds.microseconds{T}'56{T}TargetCompId{T}"]
    pattern_msg_type = r"\t35\t([A-Za-z0-9]+)\t34\t"
    pattern_data_time = r"\t(\d{8}-\d{2}:\d{2}:\d{2}\.\d{3})\t"
    
    for row in content:
        full_row = str(row)
        row = row.strip()
        row = row.replace("(8=FIXT.1.19", f"({T}8{T}FIXT.1.1{T}9")
        row = row.replace(" - INFO  logs.CustomScreenLog - <FIXT.1.1", f"{T}<FIXT.1.1") # separator for fx
        row = row.replace(" - <FIXT.1.1", f"{T}<FIXT.1.1") # separator for clasic and plus
        row = row.replace(".- ", f"{T}")
        row = row.replace(",", ".")
        row = row.replace(chr(0x01), f"{T}")
        row = row.replace("=", f"{T}")
        row = re.sub(pattern_msg_type, replace_msg_type, row)
        row = re.sub(pattern_data_time, replace_with_datetime, row)
        instrument = extract_instrument(row)
        csv_content.append(full_row + instrument + row)
        
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"sep={T}\n")  
        output_file.writelines("\n".join(csv_content))


def replace_msg_type(match):
        msg_type = match.group(1)  # Captura el valor de "V" o el que corresponda
        msg_text = MSG_TYPE_DICT.get(msg_type, "Unknown")  # Busca en el diccionario
        return f"\t35\t{msg_type}\t{msg_text}\t34\t"  # Reemplaza con el nuevo formato


def replace_with_datetime(match):
    date_str = match.group(1)  # Captura la fecha del grupo de la regex
    date_obj = datetime.strptime(date_str, "%Y%m%d-%H:%M:%S.%f")  # Convierte a datetime

    seconds_only = date_obj.second + date_obj.microsecond / 1_000_000  # Calcular los segundos dentro del minuto
    total_seconds = date_obj.minute * 60 + seconds_only  # Minutos a segundos + segundos dentro del minuto

    return f"\t{date_obj}\t{total_seconds:.3f}\t"


def extract_instrument(input_string):
    # Patrón para coincidir con el formato "\tXXXXXXX-dddd-X-XX-XXX\t"
    pattern = r'\t\S+-\d{4}-[A-Z]-[A-Z]{2}-[A-Z]{3}\t'
    match = re.search(pattern, input_string)
    if match:
        return match.group(0)
    else:
        return "\tUnknown\t"


if __name__ == "__main__":
    start()
