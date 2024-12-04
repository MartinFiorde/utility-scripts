import os
import re
import shutil
import winreg
from datetime import datetime
from tkinter import Tk, filedialog


REGISTRY_PATH = r"SOFTWARE\\JavaSoft\\Prefs\\filterScript"
LAST_DIR_KEY = "LastUsedDir"
LAST_INPUT_KEY = "LastFilterInput"

FIX_TAGS_PRIORITY = ['9', '35', '34', '49', '52', '56']
FIX_TAGS_4D = ['1000', '1001', '1002', '1003', '1005', '1006', '1007', '1008', '1009', '1011', '1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', '1021', '1022', '1023', '1024', '1025', '1026', '1027', '1028', '1029', '1030', '1031', '1032', '1033', '1034', '1035', '1036', '1037', '1038', '1039', '1040', '1041', '1042', '1043', '1044', '1045', '1046', '1047', '1048', '1049', '1050', '1051', '1052', '1053', '1054', '1055', '1056', '1057', '1058', '1059', '1060', '1061', '1062', '1063', '1064', '1065', '1066', '1067', '1068', '1069', '1070', '1071', '1072', '1073', '1074', '1075', '1079', '1080', '1081', '1082', '1083', '1084', '1085', '1086', '1087', '1088', '1089', '1090', '1091', '1092', '1093', '1094', '1095', '1096', '1097', '1098', '1099', '1100', '1101', '1102', '1103', '1104', '1105', '1106', '1107', '1108', '1109', '1110', '1111', '1112', '1113', '1114', '1115', '1116', '1117', '1118', '1119', '1120', '1121', '1122', '1123', '1124', '1125', '1126', '1127', '1128', '1129', '1130', '1131', '1132', '1133', '1134', '1135', '1136', '1137', '1138', '1139']
FIX_TAGS_3D = ['100', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '262', '263', '264', '265', '266', '267', '268', '269', '270', '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', '281', '282', '283', '284', '285', '286', '287', '288', '289', '290', '291', '292', '293', '294', '295', '296', '297', '298', '299', '300', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '311', '312', '313', '314', '315', '316', '317', '318', '319', '320', '321', '322', '323', '324', '325', '326', '327', '328', '329', '330', '331', '332', '333', '334', '335', '336', '337', '338', '339', '340', '341', '342', '343', '344', '345', '346', '347', '348', '349', '350', '351', '352', '353', '354', '355', '356', '357', '358', '359', '360', '361', '362', '363', '364', '365', '366', '367', '368', '369', '370', '371', '372', '373', '374', '375', '376', '377', '378', '379', '380', '381', '382', '383', '384', '385', '386', '387', '388', '389', '390', '391', '392', '393', '394', '395', '396', '397', '398', '399', '400', '401', '402', '403', '404', '405', '406', '407', '408', '409', '410', '411', '412', '413', '414', '415', '416', '417', '418', '419', '420', '421', '422', '423', '424', '425', '426', '427', '428', '429', '430', '431', '432', '433', '434', '435', '436', '437', '438', '439', '440', '441', '442', '443', '444', '445', '446', '447', '448', '449', '450', '451', '452', '453', '454', '455', '456', '457', '458', '459', '460', '461', '462', '463', '464', '465', '466', '467', '468', '469', '470', '471', '472', '473', '474', '475', '476', '477', '478', '479', '480', '481', '482', '483', '484', '485', '486', '487', '488', '489', '490', '491', '492', '493', '494', '495', '496', '497', '498', '499', '500', '501', '502', '503', '504', '505', '506', '507', '508', '509', '510', '511', '512', '513', '514', '515', '516', '517', '518', '519', '520', '521', '522', '523', '524', '525', '526', '527', '528', '529', '530', '531', '532', '533', '534', '535', '536', '537', '538', '539', '540', '541', '542', '543', '544', '545', '546', '547', '548', '549', '550', '551', '552', '553', '554', '555', '556', '557', '558', '559', '560', '561', '562', '563', '564', '565', '566', '567', '568', '569', '570', '571', '572', '573', '574', '575', '576', '577', '578', '579', '580', '581', '582', '583', '584', '585', '586', '587', '588', '589', '590', '591', '592', '593', '594', '595', '596', '597', '598', '599', '600', '601', '602', '603', '604', '605', '606', '607', '608', '609', '610', '611', '612', '613', '614', '615', '616', '617', '618', '619', '620', '621', '622', '623', '624', '625', '626', '627', '628', '629', '630', '631', '632', '633', '634', '635', '636', '637', '638', '639', '640', '641', '642', '643', '644', '645', '646', '647', '648', '649', '650', '651', '652', '653', '654', '655', '656', '657', '658', '659', '660', '661', '662', '663', '664', '665', '666', '667', '668', '669', '670', '671', '672', '673', '674', '675', '676', '677', '678', '679', '680', '681', '682', '683', '684', '685', '686', '687', '688', '689', '690', '691', '692', '693', '694', '695', '696', '697', '698', '699', '700', '701', '702', '703', '704', '705', '706', '707', '708', '709', '710', '711', '712', '713', '714', '715', '716', '717', '718', '719', '720', '721', '722', '723', '724', '725', '726', '727', '728', '729', '730', '731', '732', '733', '734', '735', '736', '737', '738', '739', '740', '741', '742', '743', '744', '745', '746', '747', '748', '749', '750', '751', '752', '753', '754', '755', '756', '757', '758', '759', '760', '761', '762', '763', '764', '765', '766', '767', '768', '769', '770', '771', '772', '773', '774', '775', '776', '777', '778', '779', '780', '781', '782', '783', '784', '785', '786', '787', '788', '789', '790', '791', '792', '793', '794', '795', '796', '797', '798', '799', '800', '801', '802', '803', '804', '805', '806', '807', '808', '810', '811', '812', '813', '814', '815', '816', '817', '818', '819', '820', '821', '822', '823', '824', '825', '826', '827', '828', '829', '830', '831', '832', '833', '834', '835', '836', '837', '838', '839', '840', '841', '842', '843', '844', '845', '846', '847', '848', '849', '850', '851', '852', '853', '854', '855', '856', '857', '858', '859', '860', '861', '862', '863', '864', '865', '866', '867', '868', '869', '870', '871', '872', '873', '874', '875', '876', '877', '878', '879', '880', '881', '882', '883', '884', '885', '886', '887', '888', '889', '890', '891', '892', '893', '894', '895', '896', '897', '898', '899', '900', '901', '902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924', '925', '926', '927', '928', '929', '930', '931', '932', '933', '934', '935', '936', '937', '938', '939', '940', '941', '942', '943', '944', '945', '946', '947', '948', '949', '950', '951', '952', '953', '954', '955', '956', '957', '958', '959', '960', '961', '962', '963', '964', '965', '966', '967', '968', '969', '970', '971', '972', '973', '974', '975', '976', '977', '978', '979', '980', '981', '982', '983', '984', '985', '986', '987', '988', '989', '990', '991', '992', '993', '994', '996', '997', '998', '999']
FIX_TAGS_2D = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']
FIX_TAGS_1D = ['1', '2', '3', '4', '5', '6', '7', '9'] # removed '8' to avoid double tabulation on start of fix msg


MSG_TYPE_DICT = {
    "0": "35=0 Heartbeat",
    "1": "35=1 TestRequest",
    "2": "35=2 ResendRequest",
    "3": "35=3 Reject",
    "4": "35=4 SequenceReset",
    "5": "35=5 Logout",
    "6": "35=6 IOI",
    "7": "35=7 Advertisement",
    "8": "35=8 ExecutionReport",
    "9": "35=9 OrderCancelReject",
    "a": "35=a QuoteStatusRequest",
    "A": "35=A Logon",
    "AA": "35=AA DerivativeSecurityList",
    "AB": "35=AB NewOrderMultileg",
    "AC": "35=AC MultilegOrderCancelReplace",
    "AD": "35=AD TradeCaptureReportRequest",
    "AE": "35=AE TradeCaptureReport",
    "AF": "35=AF OrderMassStatusRequest",
    "AG": "35=AG QuoteRequestReject",
    "AH": "35=AH RFQRequest",
    "AI": "35=AI QuoteStatusReport",
    "AJ": "35=AJ QuoteResponse",
    "AK": "35=AK Confirmation",
    "AL": "35=AL PositionMaintenanceRequest",
    "AM": "35=AM PositionMaintenanceReport",
    "AN": "35=AN RequestForPositions",
    "AO": "35=AO RequestForPositionsAck",
    "AP": "35=AP PositionReport",
    "AQ": "35=AQ TradeCaptureReportRequestAck",
    "AR": "35=AR TradeCaptureReportAck",
    "AS": "35=AS AllocationReport",
    "AT": "35=AT AllocationReportAck",
    "AU": "35=AU Confirmation_Ack",
    "AV": "35=AV SettlementInstructionRequest",
    "AW": "35=AW AssignmentReport",
    "AX": "35=AX CollateralRequest",
    "AY": "35=AY CollateralAssignment",
    "AZ": "35=AZ CollateralResponse",
    "b": "35=b MassQuoteAcknowledgement",
    "B": "35=B News",
    "BA": "35=BA CollateralReport",
    "BB": "35=BB CollateralInquiry",
    "BC": "35=BC NetworkCounterpartySystemStatusRequest",
    "BD": "35=BD NetworkCounterpartySystemStatusResponse",
    "BE": "35=BE UserRequest",
    "BF": "35=BF UserResponse",
    "BG": "35=BG CollateralInquiryAck",
    "BH": "35=BH ConfirmationRequest",
    "BI": "35=BI TradingSessionListRequest",
    "BJ": "35=BJ TradingSessionList",
    "BK": "35=BK SecurityListUpdateReport",
    "BL": "35=BL AdjustedPositionReport",
    "BM": "35=BM AllocationInstructionAlert",
    "BN": "35=BN ExecutionAcknowledgement",
    "BO": "35=BO ContraryIntentionReport",
    "BP": "35=BP SecurityDefinitionUpdateReport",
    "c": "35=c SecurityDefinitionRequest",
    "C": "35=C Email",
    "d": "35=d SecurityDefinition",
    "D": "35=D NewOrderSingle",
    "e": "35=e SecurityStatusRequest",
    "E": "35=E NewOrderList",
    "f": "35=f SecurityStatus",
    "F": "35=F OrderCancelRequest",
    "g": "35=g TradingSessionStatusRequest",
    "G": "35=G OrderCancelReplaceRequest",
    "h": "35=h TradingSessionStatus",
    "H": "35=H OrderStatusRequest",
    "i": "35=i MassQuote",
    "j": "35=j BusinessMessageReject",
    "J": "35=J AllocationInstruction",
    "k": "35=k BidRequest",
    "K": "35=K ListCancelRequest",
    "l": "35=l BidResponse",
    "L": "35=L ListExecute",
    "m": "35=m ListStrikePrice",
    "M": "35=M ListStatusRequest",
    "n": "35=n XML_non_FIX",
    "N": "35=N ListStatus",
    "o": "35=o RegistrationInstructions",
    "p": "35=p RegistrationInstructionsResponse",
    "P": "35=P AllocationInstructionAck",
    "q": "35=q OrderMassCancelRequest",
    "Q": "35=Q DontKnowTradeDK",
    "r": "35=r OrderMassCancelReport",
    "R": "35=R QuoteRequest",
    "s": "35=s NewOrderCross",
    "S": "35=S Quote",
    "t": "35=t CrossOrderCancelReplaceRequest",
    "T": "35=T SettlementInstructions",
    "u": "35=u CrossOrderCancelRequest",
    "v": "35=v SecurityTypeRequest",
    "V": "35=V MarketDataRequest",
    "w": "35=w SecurityTypes",
    "W": "35=W MarketDataSnapshotFullRefresh",
    "x": "35=x SecurityListRequest",
    "X": "35=X MarketDataIncrementalRefresh",
    "y": "35=y SecurityList",
    "Y": "35=Y MarketDataRequestReject",
    "z": "35=z DerivativeSecurityListRequest",
    "Z": "35=Z QuoteCancel"
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
        if "8=FIXT.1.19=" not in lines:
                print(f"\n\n----------WARNING----------\nLOG FORMAT CORRUPTED.\nRECOVER SERVICE WILL TRY TO RECOVER TABULATION.\nSOME TAGS MAY GET INCORRECT VALUES\n\n")

        i = 0
        while i < len(lines):
            line = [i, lines[i].strip()]
            if "8=FIXT.1.19=" in line[1]:
                line[1] = recover_soh(line[1], "")
            if "8=FIXT.1.1|9=" in line[1]:
                line[1] = recover_soh(line[1], "|")
            if "8=FIXT.1.1 9=" in line[1]:
                line[1] = recover_soh(line[1], " ")
            
            if "\t\t" in line[1]:
                print("TRUE DOBLE TAB POST RECOVER")
            
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


def recover_soh(line: str, separator):
    for tag in FIX_TAGS_PRIORITY:
        line = line.replace(f"{separator}{tag}=", f"{tag}|&|=", 1)
    for tag in FIX_TAGS_3D:
        line = line.replace(f"{separator}{tag}=", f"{tag}|&|=")
    for tag in FIX_TAGS_4D:
        line = line.replace(f"{separator}{tag}=", f"{tag}|&|=")
    for tag in FIX_TAGS_2D:
        line = line.replace(f"{separator}{tag}=", f"{tag}|&|=")
    for tag in FIX_TAGS_1D:
        line = line.replace(f"{separator}{tag}=", f"{tag}|&|=")
    line = line.replace("|&|","")
    return line


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
    csv_column_headers = f"full row{T}instrument name{T}row n{T}local date (yyyy-mm-dd hh:mm:ss.000){T}minutes in seconds.microseconds{T}log header{T}'8{T}BeginString{T}'9{T}BodyLength{T}'35{T}MsgType{T}MSG TYPE TITLE{T}'34{T}MsgSeqNum{T}'49{T}SenderCompId{T}'52{T}SendingTime{T}minutes in seconds.microseconds{T}'56{T}TargetCompId{T}"
    csv_content = [csv_column_headers]
    pattern_log_header = r"\.\- (\d{8}-\d{2}:\d{2}:\d{2}.\d{3}) \- "
    pattern_msg_type = r"\t35\t([A-Za-z0-9]+)\t34\t"
    pattern_data_time = r"\t(\d{8}-\d{2}:\d{2}:\d{2}\.\d{3})\t"

    for row in content:
        if "\t\t" in row:
                print("TRUE DOBLE TAB CSV")
        
        full_row = str(row)
        row = row.strip()
        row = row.replace(",", ".", 1)
        row = re.sub(pattern_log_header, r"\t\1\t", row, 1)
        row = row.replace("8=FIXT.1.19", f"{T}8{T}FIXT.1.1{T}9")
        row = row.replace(chr(0x01), f"{T}")
        row = row.replace("=", f"{T}")
        row = re.sub(pattern_msg_type, replace_msg_type, row, 1)
        row = re.sub(pattern_data_time, replace_with_datetime, row, 2)
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
