import os
from Bio import SeqIO

def convert_rtf_to_text(rtf_file, txt_file):
    with open(rtf_file, "r") as rtf:
        content = rtf.read()

    content = content.replace('{\\rtf1\\ansi\\deff0', '').replace('}', '').replace('\\', '')
    with open(txt_file, "w") as txt:
        txt.write(content)

def convert_txt_to_fasta(txt_file, fasta_file):
    with open(txt_file, "r") as txt:
        lines = txt.readlines()
    with open(fasta_file, "w") as fasta:
        fasta.write(">gene_description\n")
        for line in lines:
            fasta.write(line.strip() + "\n")

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".rtf"):
            rtf_path = os.path.join(folder_path, filename)
            txt_path = os.path.join(folder_path, filename.replace(".rtf", ".txt"))
            fasta_path = os.path.join(folder_path, filename.replace(".rtf", ".fasta"))
            convert_rtf_to_text(rtf_path, txt_path)
            convert_txt_to_fasta(txt_path, fasta_path)
            print(f"Converted {filename} to FASTA format.")


process_folder(r"C:\Users\Danial\Desktop\bad_genes")
