import os
from Bio import SeqIO
import re
#
# def convert_rtf_to_text(rtf_file, txt_file):
#     with open(rtf_file, "r") as rtf:
#         content = rtf.read()
#
#     content = content.replace('{\\rtf1\\ansi\\deff0', '').replace('}', '').replace('\\', '')
#     with open(txt_file, "w") as txt:
#         txt.write(content)
#
# def convert_txt_to_fasta(txt_file, fasta_file):
#     with open(txt_file, "r") as txt:
#         lines = txt.readlines()
#     with open(fasta_file, "w") as fasta:
#         fasta.write(">gene_description\n")
#         for line in lines:
#             fasta.write(line.strip() + "\n")
#
# def process_folder(folder_path):
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".rtf"):
#             rtf_path = os.path.join(folder_path, filename)
#             txt_path = os.path.join(folder_path, filename.replace(".rtf", ".txt"))
#             fasta_path = os.path.join(folder_path, filename.replace(".rtf", ".fasta"))
#             convert_rtf_to_text(rtf_path, txt_path)
#             convert_txt_to_fasta(txt_path, fasta_path)
#             print(f"Converted {filename} to FASTA format.")

import os
import re


import os
import re

def process_files_to_fasta(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Read the file content
        with open(file_path, "r") as file:
            file_content = file.read()

        # Preprocess the filename to remove unwanted characters and ensure it ends with .fasta
        base_name, ext = os.path.splitext(filename)
        new_base_name = re.sub(r'[^A-Za-z0-9_]', '_', base_name)
        new_filename = new_base_name + ".fasta"
        new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file if the name has changed
        if new_filename != filename:
            os.rename(file_path, new_file_path)
            print(f"Renamed file: {filename} to {new_filename}")





def clean_fasta_sequence(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".fasta"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")  # Debugging line
            with open(file_path, "r") as file:
                fasta_string = file.read()

            lines = fasta_string.strip().split("\n")

            headers = []
            sequence = []

            for line in lines:
                if ">" in line:
                    # Remove anything before '>' and strip the line
                    clean_header = line[line.find(">"):].strip()
                    headers.append(clean_header)
                else:
                    sequence.append(line)

            sequence = "".join(sequence).upper()

            if not re.match("^[ATCGN]*$", sequence):
                print(f"Invalid FASTA format in {file_path}: Sequence contains invalid characters")

            corrected_sequence = re.sub("[^ATCGN]", "", sequence)

            corrected_fasta = "\n".join(headers) + "\n" + corrected_sequence

            # Save the cleaned sequence back to the file
            with open(file_path, "w") as file:
                file.write(corrected_fasta)

            print(f"Cleaned sequence saved to {file_path}")




# Example usage
folder_path = r'C:\Users\Danial\Desktop\raw_genes'
process_files_to_fasta(folder_path)
clean_fasta_sequence(folder_path)

