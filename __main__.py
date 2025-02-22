import os
import hashlib
import shutil
import binascii
import xml.etree.ElementTree as ET
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Configuración de la ventana principal
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.title("ROM Manager 1.0")
window.geometry("500x500")
window.resizable(False, False)

# Función para mostrar salida en el cuadro de texto
def log_message(message):
    output_text.configure(state="normal")
    output_text.insert("end", message + "\n")
    output_text.configure(state="disabled")
    output_text.see("end")

# Funciones para manejo de archivos
def load_datfile(datfile):
    hash_dict = {}
    tree = ET.parse(datfile)
    root = tree.getroot()
    
    for game in root.findall("game"):
        region = game.get("region", "Unknown")
        for rom in game.findall("rom"):
            md5 = rom.get("md5")
            crc = rom.get("crc")
            sha1 = rom.get("sha1")
            size = rom.get("size")
            rom_name = rom.get("name")
            
            if md5 and rom_name:
                hash_dict[md5] = (rom_name, size, crc, sha1, region)
    
    return hash_dict

def calculate_hash(file, method="md5", buffer_size=65536):
    hasher = hashlib.md5() if method == "md5" else hashlib.sha1()
    
    with open(file, "rb") as f:
        while chunk := f.read(buffer_size):
            hasher.update(chunk)
    
    return hasher.hexdigest()

def calculate_crc32(file):
    buf_size = 65536
    crc = 0
    with open(file, "rb") as f:
        while chunk := f.read(buf_size):
            crc = binascii.crc32(chunk, crc)
    return format(crc & 0xFFFFFFFF, '08x')

def rename_and_organize_roms(folder, hash_dict, organize_for_twilight):
    region_folders = {}
    game_count = 0
    batch_num = 1
    
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            if full_path.lower().endswith((".nes", ".sfc", ".smc", ".bin", ".md", ".zip")):
                rom_hash = calculate_hash(full_path, "md5")
                rom_crc = calculate_crc32(full_path)
                file_size = str(os.path.getsize(full_path))
                
                if rom_hash in hash_dict:
                    new_name, expected_size, expected_crc, _, region = hash_dict[rom_hash]
                    
                    if expected_size and file_size != expected_size:
                        log_message(f"⚠ Size mismatch: {file}")
                        continue
                    
                    if expected_crc and rom_crc != expected_crc:
                        log_message(f"⚠ CRC mismatch: {file}")
                        continue
                    
                    region_folder = os.path.join(folder, region)
                    if region not in region_folders:
                        os.makedirs(region_folder, exist_ok=True)
                        region_folders[region] = region_folder
                        game_count = 0
                        batch_num = 1
                    
                    if organize_for_twilight and game_count >= 200:
                        batch_num += 1
                        game_count = 0
                    
                    final_folder = os.path.join(region_folder, f"Batch_{batch_num}") if organize_for_twilight else region_folder
                    os.makedirs(final_folder, exist_ok=True)
                    
                    new_path = os.path.join(final_folder, new_name)
                    if full_path != new_path:
                        try:
                            shutil.move(full_path, new_path)
                            log_message(f"✅ Moved: {file} -> {new_path}")
                            game_count += 1
                        except Exception as e:
                            log_message(f"⚠ Could not move {file}: {e}")

def process_roms():
    rom_folder = entry_roms.get()
    dat_file = entry_dat.get()
    organize_for_twilight = checkbox_organize.get()
    
    if not os.path.isdir(rom_folder) or not os.path.isfile(dat_file):
        messagebox.showerror("Error", "Please select a valid ROM folder and DAT file.")
        return
    
    try:
        hash_dict = load_datfile(dat_file)
        rename_and_organize_roms(rom_folder, hash_dict, organize_for_twilight)
        messagebox.showinfo("Success", "Process completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Marco principal
frame = ctk.CTkFrame(master=window, corner_radius=10)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Etiquetas y Entradas
label_roms = ctk.CTkLabel(master=frame, text="ROMs Folder:", font=("Arial", 14))
label_roms.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_roms = ctk.CTkEntry(master=frame, placeholder_text="./")
entry_roms.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

def select_rom_folder():
    folder = filedialog.askdirectory()
    if folder:
        entry_roms.delete(0, "end")
        entry_roms.insert(0, folder)
button_browse_roms = ctk.CTkButton(master=frame, text="Browse", command=select_rom_folder)
button_browse_roms.grid(row=0, column=2, padx=10, pady=10)

label_dat = ctk.CTkLabel(master=frame, text="DAT File:", font=("Arial", 14))
label_dat.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_dat = ctk.CTkEntry(master=frame, placeholder_text="./")
entry_dat.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

def select_dat_file():
    file = filedialog.askopenfilename(filetypes=[("DAT File", "*.dat")])
    if file:
        entry_dat.delete(0, "end")
        entry_dat.insert(0, file)
button_browse_dat = ctk.CTkButton(master=frame, text="Browse", command=select_dat_file)
button_browse_dat.grid(row=1, column=2, padx=10, pady=10)

# Checkbox
checkbox_organize = ctk.CTkCheckBox(master=frame, text="Organize for Twilight Menu++")
checkbox_organize.grid(row=2, column=0, columnspan=3, pady=10, padx=10 ,sticky="w")

# Botón Ejecutar
button_execute = ctk.CTkButton(master=frame, text="Execute", fg_color="#1E90FF", command=process_roms)
button_execute.grid(row=3, column=0, columnspan=3, pady=20, padx=10, sticky="ew")

# Área de salida con scrollbar
output_frame = ctk.CTkFrame(master=frame)
output_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

output_text = ctk.CTkTextbox(master=output_frame, height=100, wrap="word", state="disabled")
output_text.pack(side="left", fill="both", expand=True)

scrollbar = ctk.CTkScrollbar(master=output_frame, command=output_text.yview)
scrollbar.pack(side="right", fill="y")
output_text.configure(yscrollcommand=scrollbar.set)

# Ajuste de columnas
frame.columnconfigure(1, weight=1)

# Ejecutar ventana
window.mainloop()
