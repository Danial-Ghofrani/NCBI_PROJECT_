import os
import shutil
import patoolib
import pandas as pd
import mysql.connector
from ..entity.gene import *
from ..entity.genome import WholeGenome


class DB:
    def __init__(self, gene, db_info):
        self.gene = gene
        self.db_info = db_info
        self.mydb = None

    def connect(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.db_info['host'],
                user=self.db_info['user'],
                passwd=self.db_info['password'],
                database=self.db_info['database']
            )
            self.cursor = self.mydb.cursor()
            print("Successfully connected to the database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self, commit=False):
        if commit:
            self.mydb.commit()
        self.cursor.close()
        self.mydb.close()

    def table_exists(self, table_name):
        self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = self.cursor.fetchone()
        return result is not None

    import os
    import pandas as pd

    def create_and_insert_blast_results(self, table_name, csv_file):
        self.connect()

        # Check if the table already exists
        if self.table_exists(table_name):
            print(f"Table '{table_name}' already exists. Skipping creation and insertion.")
            self.disconnect()
            return

        # Define table columns and types
        columns = '''
            id INT AUTO_INCREMENT PRIMARY KEY,
            query_id NVARCHAR(100),
            genome_name NVARCHAR(100),
            subject_id VARCHAR(100),
            identity FLOAT,
            alignment_length INT,
            mismatches INT,
            gap_opens INT,
            q_start INT,
            q_end INT,
            s_start INT,
            s_end INT,
            evalue FLOAT,
            bit_score FLOAT,
            query_length INT,
            subject_length INT,
            subject_strand NVARCHAR(20),
            query_frame INT,
            sbjct_frame INT,
            qseq_path NVARCHAR(300),
            sseq_path NVARCHAR(300)
        '''

        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        insert_query = f"""
            INSERT INTO {table_name} (query_id, genome_name, subject_id, identity, alignment_length,
                                      mismatches, gap_opens, q_start, q_end, s_start, s_end, evalue, bit_score,
                                      query_length, subject_length, subject_strand, query_frame, sbjct_frame, qseq_path, sseq_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.connect()
        self.cursor.execute(create_table_query)

        # Read the CSV file
        df = pd.read_csv(f'{csv_file}.csv', header=None)

        folder_path = f"{self.gene}_seq_folder"
        os.makedirs(folder_path, exist_ok=True)

        # Iterate through each row in the DataFrame
        for idx, row in df.iterrows():
            query_id = row[1]

            # Split the query_id by '|'
            parts = query_id.split('|')

            if len(parts) == 2:
                genome_name, original_query_id = parts
            elif len(parts) > 2:
                genome_name = parts[0]
                original_query_id = parts[2]
                # If needed, you can handle additional parts here
            else:
                print(f"Unexpected format in query_id: {query_id}")
                continue

            # Include genome_name in the file names
            qseq_path = os.path.join(folder_path, f"{self.gene}_{genome_name}_qseq_{idx}.fasta")
            sseq_path = os.path.join(folder_path, f"{self.gene}_{genome_name}_sseq_{idx}.fasta")

            with open(qseq_path, 'w') as qf:
                qf.write(row[17])
            with open(sseq_path, 'w') as sf:
                sf.write(row[18])

            row_data = (original_query_id, genome_name) + tuple(row[1:17]) + (qseq_path, sseq_path)
            self.cursor.execute(insert_query, row_data)

        self.disconnect(commit=True)

    def add_cutoff_column(self, table_name):
        self.connect()
        self.cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'cutoff'")
        exists = self.cursor.fetchone()
        if not exists:
            alter_table_query = f"ALTER TABLE {table_name} ADD COLUMN cutoff TINYINT"
            self.cursor.execute(alter_table_query)
        update_query = f"""UPDATE {table_name} SET cutoff = CASE
                                    WHEN identity < 85 OR (alignment_length / query_length) * 100 < 90 or evalue > 0.05 THEN 0
                                    ELSE 1
                                END
                            """
        self.cursor.execute(update_query)
        print(f"Column 'cutoff' updated in {table_name} table.")
        self.disconnect(commit=True)

    def show_database_contents(self, table_name):
        # Query to select all rows from the specified table
        self.connect()
        select_query = f"SELECT * FROM {table_name}"

        # Execute the query
        df = pd.read_sql_query(select_query, self.mydb, index_col='id')

        # To show all columns
        # pd.set_option('display.max_columns', None)

        self.disconnect()
        return df

    def execute_command(self, sql_command):
        self.connect()
        self.cursor.execute(sql_command)
        self.disconnect()

    def save(self):
        table_name = self.gene
        csv_file = f"{self.gene}.csv"
        self.create_and_insert_blast_results(table_name, csv_file)

    def search_result_table_by_name(self, table_name):
        self.connect()
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        self.disconnect()
        return rows

    def add_row(self, table_name, row_data):
        self.connect()
        insert_query = f"""
                INSERT INTO {table_name} (genome_name, query_id, subject_id, identity, alignment_length, 
                mismatches, gap_opens, q_start,q_end, s_start, s_end, evalue, bit_score, query_length, 
                subject_length, subject_strand, query_frame, sbjct_frame, qseq_path, sseq_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
            """
        self.cursor.execute(insert_query, row_data)
        self.disconnect(commit=True)

    def delete_row_from_result_table_by_condition(self, table_name, condition):
        self.connect()
        self.cursor.execute(f" DELETE FROM {table_name} WHERE {condition}")
        self.disconnect(commit=True)

    def update_result_table_row_by_condition(self, table_name, updates, condition):
        self.connect()
        self.cursor.execute(f"UPDATE {table_name} SET {updates} WHERE {condition}")
        self.disconnect(commit=True)

    def search_result_table_by_name(self, table_name):
        self.connect()
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s 
                AND table_name LIKE %s
        """

        self.cursor.execute(query, (self.db_info['database'], table_name))
        rows = self.cursor.fetchall()
        self.disconnect()
        return rows

    def search_all_genes(self):
        self.connect()
        self.cursor.execute("SELECT * FROM gene_files")
        genes = self.cursor.fetchall()
        genes_list = []
        for gene in genes:
            gene = Gene(*gene)
            genes_list.append(gene)

        self.disconnect()
        return genes_list

    def search_gene_by_name(self, gene_name):
        self.connect()
        self.cursor.execute("SELECT * FROM gene_files WHERE file_name LIKE %s", [f'%{gene_name}%'])
        genes = self.cursor.fetchall()
        genes_list = []
        for gene in genes:
            gene = Gene(*gene)
            genes_list.append(gene)

        self.disconnect()
        return genes_list

    def search_gene_by_id(self, id):
        self.connect()
        self.cursor.execute("SELECT * FROM gene_files WHERE id=%s", [id])
        gene = self.cursor.fetchone()
        gene = Gene(*gene)
        self.disconnect()
        return gene

    def search_all_genomes(self):
        self.connect()
        self.cursor.execute("SELECT * FROM genome_files")
        genomes = self.cursor.fetchall()
        genomes_list = []
        for genome in genomes:
            genome = WholeGenome(*genome)
            genomes_list.append(genome)

        self.disconnect()
        return genomes_list

    def search_genome_by_name(self, genome_name):
        self.connect()
        self.cursor.execute("SELECT * FROM genome_files WHERE file_name LIKE %s", [f'%{genome_name}%'])
        genomes = self.cursor.fetchall()
        genomes_list = []
        for genome in genomes:
            genome = WholeGenome(*genome)
            genomes_list.append(genome)

        self.disconnect()
        return genomes_list

    def search_genome_by_id(self, id):
        self.connect()
        self.cursor.execute("SELECT * FROM genome_files WHERE id=%s", [id])
        genome = self.cursor.fetchone()
        genome = WholeGenome(*genome)
        self.disconnect()
        return genome

    def export_table(self, table_name, output_file, file_format):
        self.connect()
        select_query = f"SELECT * FROM {table_name}"

        # Execute the query
        df = pd.read_sql_query(select_query, self.mydb, index_col='id')
        self.disconnect()

        if file_format == 'csv':
            df.to_csv(f"{output_file}.csv", index=False)
        elif file_format == 'excel':
            df.to_excel(f"{output_file}.xlsx", index=False)
        elif file_format == 'json':
            df.to_json(f"{output_file}.json", orient='records')

    def create_combined_wgs(self):
        genomes = self.search_all_genomes()

        genome_dict = {}
        for genome in genomes:
            genome_dict[genome.name] = genome.file_path

        output_file = "combined_wgs.fasta"
        with open(output_file, 'w') as outfile:
            for genome_name, genome_path in genome_dict.items():
                with open(genome_path, 'r') as infile:
                    for line in infile:
                        if line.startswith('>'):
                            header = line.strip()
                            # Embed genome name in the query_id
                            new_header = f">{genome_name}|{header[1:]}"
                            outfile.write(new_header + '\n')
                        else:
                            outfile.write(line)



    def organize_sequences_by_cutoff(self, table_name):

        self.connect()

        # Define folders
        base_folder = f"{self.gene}_seq_folder"
        cutoff_folder = os.path.join(base_folder, "cutoff_1")

        os.makedirs(cutoff_folder, exist_ok=True)

        # Fetch all records from the database
        query = f"""
            SELECT id, query_id, genome_name, qseq_path, sseq_path, cutoff
            FROM {table_name};
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        # Step 1: Copy all sequence files to cutoff_folder
        for record in records:
            _, _, _, qseq_path, sseq_path, _ = record

            # Paths for copying
            base_qseq_path = os.path.join(base_folder, os.path.basename(qseq_path))
            base_sseq_path = os.path.join(base_folder, os.path.basename(sseq_path))

            # Destination paths in the cutoff_folder
            cutoff_qseq_path = os.path.join(cutoff_folder, os.path.basename(qseq_path))
            cutoff_sseq_path = os.path.join(cutoff_folder, os.path.basename(sseq_path))

            # Copy files if they exist in the base folder
            if os.path.exists(base_qseq_path):
                shutil.copy(base_qseq_path, cutoff_qseq_path)
            if os.path.exists(base_sseq_path):
                shutil.copy(base_sseq_path, cutoff_sseq_path)

        # Step 2: Remove files from cutoff_folder if cutoff != 1
        for record in records:
            _, _, _, qseq_path, sseq_path, cutoff = record

            if cutoff != 1:
                # Remove files from cutoff_folder if cutoff != 1
                cutoff_qseq_path = os.path.join(cutoff_folder, os.path.basename(qseq_path))
                cutoff_sseq_path = os.path.join(cutoff_folder, os.path.basename(sseq_path))
                if os.path.exists(cutoff_qseq_path):
                    os.remove(cutoff_qseq_path)
                if os.path.exists(cutoff_sseq_path):
                    os.remove(cutoff_sseq_path)

        self.disconnect()
        print("Sequences organized by cutoff value.")


    def organize_sequences_by_duplicate(self, table_name):
        self.connect()

        # Define folders
        base_folder = f"{self.gene}_seq_folder"
        duplicate_folder = os.path.join(base_folder, "duplicate_1")

        os.makedirs(duplicate_folder, exist_ok=True)

        # Fetch all records from the database
        query = f"""
            SELECT id, query_id, genome_name, qseq_path, sseq_path, duplicate
            FROM {table_name};
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        # Step 1: Copy all sequence files to duplicate_folder
        for record in records:
            _, _, _, qseq_path, sseq_path, duplicate = record

            # Debugging: print duplicate value
            print(f"Processing record with duplicate={duplicate}")

            # Paths for copying
            base_qseq_path = os.path.join(base_folder, os.path.basename(qseq_path))
            base_sseq_path = os.path.join(base_folder, os.path.basename(sseq_path))

            # Destination paths in the duplicate_folder
            duplicate_qseq_path = os.path.join(duplicate_folder, os.path.basename(qseq_path))
            duplicate_sseq_path = os.path.join(duplicate_folder, os.path.basename(sseq_path))

            # Copy files if they exist in the base folder
            if os.path.exists(base_qseq_path):
                shutil.copy(base_qseq_path, duplicate_qseq_path)
            if os.path.exists(base_sseq_path):
                shutil.copy(base_sseq_path, duplicate_sseq_path)

        # Step 2: Remove files from duplicate_folder if duplicate is not 1
        for record in records:
            _, _, _, qseq_path, sseq_path, duplicate = record

            # Only remove if duplicate is not 1 and is not NULL
            if duplicate is not None and duplicate != 1:
                duplicate_qseq_path = os.path.join(duplicate_folder, os.path.basename(qseq_path))
                duplicate_sseq_path = os.path.join(duplicate_folder, os.path.basename(sseq_path))

                if os.path.exists(duplicate_qseq_path):
                    os.remove(duplicate_qseq_path)
                if os.path.exists(duplicate_sseq_path):
                    os.remove(duplicate_sseq_path)

        self.disconnect()
        print("Sequences organized by duplicate value.")

    def move_files_to_results(self, source_folder, destination_folder, exclude_items):
        # Ensure destination folder exists
        os.makedirs(destination_folder, exist_ok=True)

        for item in os.listdir(source_folder):
            item_path = os.path.join(source_folder, item)
            dest_path = os.path.join(destination_folder, item)

            # Skip excluded items or items starting with 'WGS'
            if item in exclude_items or item.startswith('WGS') or item.endswith('.csv'):
                continue

            # Delete the existing file at destination if it exists
            if os.path.exists(dest_path):
                os.remove(dest_path)

            # Move the file
            shutil.move(item_path, destination_folder)
            print(f"Replaced existing file and moved {item} to {destination_folder}")


    def create_rar_from_folder(self, folder_path, rar_file_name):
        patoolib.create_archive(rar_file_name, [folder_path])




