import os
import shutil
import patoolib

def move_files_to_results(source_folder, destination_folder, exclude_items):

    os.makedirs(destination_folder, exist_ok=True)

    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        if item in exclude_items or item.startswith('WGS'):
            continue

        shutil.move(item_path, destination_folder)



def create_rar_from_folder(folder_path, rar_file_name):
    patoolib.create_archive(rar_file_name, [folder_path])


# usage :

source_folder = r"D:\programming\NCBI_PROJECT_"
destination_folder = r"D:\programming\NCBI_PROJECT_\results"
exclude_items = ["wgs", "model", "concatenate", ".git", ".idea", "main.py"]

rar_file_name = 'D:/programming/NCBI_PROJECT_/results.rar'

move_files_to_results(source_folder, destination_folder, exclude_items)
create_rar_from_folder(destination_folder, rar_file_name)