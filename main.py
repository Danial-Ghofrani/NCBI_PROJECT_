from datetime import datetime
from model.DB.db_model import DB
from model.entity.blast_model import BLAST
from model.entity.duplicate import *
from model.entity.analysis import *
import time


start_time = datetime.now()

# Database information:
db_info = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'wgs'
}

WGS = r"combined_wgs.fasta"
Gene = "mepa"

db = DB(Gene, db_info)
db.create_combined_wgs()

# Create a list of genes from database for blast
genes_list = db.search_all_genes()
output_file = 'gene_analysis_results.xlsx'
print(genes_list)
# Loop through genes and blast and create table of each one and export excel from the results
for gene in genes_list:
    print('-' * 20)
    print('name: ', gene.name)
    blast = BLAST(WGS, gene)
    blast.blast()
    time.sleep(1)
    db = DB(gene.name, db_info)
    db.create_and_insert_blast_results(gene.name, gene.name)
    db.add_cutoff_column(gene.name)
    duplicate_checker = DuplicateCheck(gene.name, db_info)
    duplicate_checker.process_duplicates()
    analysis = Analysis(db_info)
    analysis.process_analysis(['gene_analysis.xlsx', 'genome_gene.xlsx'])
    db.export_table(gene.name, gene.name, 'excel')



source_folder = r"D:\programming\NCBI_PROJECT_"
destination_folder = r"D:\programming\NCBI_PROJECT_\results"
exclude_items = ["wgs", "model", "concatenate", ".git", ".idea", "main.py"]
rar_file_name = 'D:/programming/NCBI_PROJECT_/results.rar'


db.move_files_to_results(source_folder, destination_folder, exclude_items)
db.create_rar_from_folder(destination_folder, rar_file_name)
end_time = datetime.now()
print("final results folder and rar file created!")

print()
print('Duration: {}'.format(end_time - start_time))