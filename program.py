import tkinter as tk
import os
import shutil
import ctypes

try:
    import customtkinter as ctk
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "customtkinter"])
    import customtkinter as ctk

root = ctk.CTk()
root.title("Usuwanie plików tymczasowych")
root.geometry("400x200")
root.resizable(False, False)

# Ustawienie tła okna na stały kolor
window_bg = "#f0e2cd"
root.configure(bg=window_bg)

background = tk.Canvas(root, width=400, height=300, bg=window_bg, highlightthickness=0)
background.pack(fill="both", expand=True)

label1 = tk.Label(root, text="Czy chcesz usunąć pliki tymczasowe ze swojego komputera?",
                   bg=window_bg, font=("Arial", 9))
label1.place(x=20, y=20)

def schedule_deletion(path):
    MOVEFILE_DELAY_UNTIL_REBOOT = 0x4
    result = ctypes.windll.kernel32.MoveFileExW(path, None, MOVEFILE_DELAY_UNTIL_REBOOT)
    if result:
        print(f"Plik '{path}' zaplanowany do usunięcia przy następnym uruchomieniu.")
    else:
        print(f"Nie udało się zaplanować usunięcia pliku '{path}'.")

def delete_temp_files(folder):
    for root_dir, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            file_path = os.path.join(root_dir, file)
            try:
                os.chmod(file_path, 0o777)
                os.remove(file_path)
                print(f"Usunięto plik: {file_path}")
            except Exception as e:
                print(f"Nie można usunąć pliku '{file_path}': {e}")
                schedule_deletion(file_path)
        for dir in dirs:
            dir_path = os.path.join(root_dir, dir)
            try:
                os.rmdir(dir_path)
                print(f"Usunięto pusty folder: {dir_path}")
            except Exception as e:
                print(f"Nie można usunąć folderu '{dir_path}': {e}")

def optymalizuj():
    temp1 = os.getenv("TEMP")
    temp2 = r"C:\Windows\Temp"
    for folder in (temp1, temp2):
        if folder and os.path.exists(folder):
            print(f"Przetwarzanie folderu: {folder}")
            delete_temp_files(folder)
        else:
            print(f"Folder '{folder}' nie istnieje lub jest nieprawidłowy.")

def wyczysc_kosz():
    SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
    flags = 0x00000001
    result = SHEmptyRecycleBin(0, None, flags)
    if result == 0:
        print("Kosz został wyczyszczony.")
    else:
        print("Błąd przy czyszczeniu kosza:", result)

# Ustawiamy bg_color przycisków na kolor tła okna, aby tło przycisków było spójne z tłem
btn_optymalizuj = ctk.CTkButton(root, text="Optymalizuj", fg_color="blue", text_color="white",
                                font=("Arial", 10, "bold"), command=optymalizuj, corner_radius=20,
                                width=120, height=40, bg_color=window_bg)
btn_optymalizuj.place(x=50, y=100)

btn_kosz = ctk.CTkButton(root, text="Wyczyść Kosz", fg_color="red", text_color="white",
                         font=("Arial", 10, "bold"), command=wyczysc_kosz, corner_radius=20,
                         width=120, height=40, bg_color=window_bg)
btn_kosz.place(x=220, y=100)

info_label = tk.Label(root, text="Usuwane: %TEMP% oraz C:\\Windows\\Temp", bg=window_bg, font=("Arial", 8))
info_label.place(x=50, y=150)

root.mainloop()
