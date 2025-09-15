import os
import string
import shutil
import subprocess

def get_available_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def find_file_in_drive(filename, start_path, excluded_dirs=None):
    if excluded_dirs is None:
        excluded_dirs = ['Windows', 'ProgramData', 'Users']
    results = []

    for root, dirs, files in os.walk(start_path, topdown=True):
        # Обрезаем исключённые директории
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        try:
            if filename in files:
                full_path = os.path.join(root, filename)
                results.append(full_path)
        except PermissionError:
            continue
    return results

if __name__ == "__main__":
    filename = "Dishonored.exe"
    drives = get_available_drives()
    print("Detected drives:", drives)

    all_matches = []
    for drive in drives:
        print(f"\nSearching drive {drive}...")
        matches = find_file_in_drive(filename, drive)
        if matches:
            all_matches.extend(matches)

    parent_dir = None  # Инициализация переменной
    if all_matches:
        print("\nAll detected matches:")
        for path in all_matches:
            print(path)
        # Фильтрация по конкретному пути для Steam версии
        filtered = [p for p in all_matches if 'steamapps\\common\\Dishonored RHCP\\Binaries\\Win32' in p]
        if filtered:
            print("\nSteam версия Dishonored RHCP найдена")
            for path in filtered:
                print(path)
            # Получение корневого каталога
            parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(filtered[0])))
        else:
            print("\nDishonored.exe был найден.")
    else:
        print("Файл не найден.")

# Проверьте, была ли найдена папка с игрой
if parent_dir:
    # Лучше использовать os.path.join
    source_loc = "Dishonored RHCP"
    dest_loc = parent_dir

    try:
        shutil.copytree(source_loc, dest_loc, dirs_exist_ok=True)
        print("Версия игры 1.2 Downpatch успешно установлена")
    except Exception as e:
        print('Ошибка:', e)

    # Установка dishonored.ini
    source_loc_in = "D1_CFG"
    Engine_ini_path = os.path.join(source_loc_in, "DishonoredEngine.ini")
    Game_ini_path = os.path.join(source_loc_in, "DishonoredGame.ini")
    Input_ini_path = os.path.join(source_loc_in, "DishonoredInput.ini")

    try:
        subprocess.run(['attrib', '+r', Engine_ini_path], check=True)
        subprocess.run(['attrib', '+r', Game_ini_path], check=True)
        subprocess.run(['attrib', '+r', Input_ini_path], check=True)
    except subprocess.CalledProcessError as e:
        print('Ошибка при установке атрибутов:', e)

    dest_path_ini = os.path.expanduser(r"~/Documents/My Games/Dishonored/DishonoredGame/Config")
    try:
        shutil.copytree(source_loc_in, dest_path_ini, dirs_exist_ok=True)
        print("dishonored.ini установлен успешно")
    except Exception as e:
        print('Ошибка:', e)

    # Установка XMouseButtonControl
    subprocess.run([r"related\XMouseButtonControlSetup.exe", "/S"])

    source_loc_cfg = "related\Configs"
    dest_loc_cfg = os.path.expanduser(r"~/AppData/Roaming/Highresolution Enterprises\XMouseButtonControl\Configs")
    try:
        shutil.copytree(source_loc_cfg, dest_loc_cfg, dirs_exist_ok=True)
    except Exception as e:
        print('Ошибка:', e)

    source_settings = "related\settings.ini"
    dest_settings = os.path.expanduser(r"~/AppData/Roaming/Highresolution Enterprises\XMouseButtonControl\settings.ini")
    try:
        shutil.copy(source_settings, dest_settings)
        print("XMouseButtonControl успешно установлен")
    except Exception as e:
        print('Ошибка:', e)

    # Установка macros
    source_macros = "related\other"
    dest_macros = r"C:\Program Files"
    try:
        shutil.copytree(source_macros, dest_macros, dirs_exist_ok=True)
        print("livesplit/NogBoard/D1 Jump Macro успешно установлен")
    except Exception as e:
        print('Ошибка:', e)
else:
    print("Не удалось найти папку с игрой для продолжения установки.")