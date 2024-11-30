import pandas as pd
import matplotlib.pyplot as plt


def generate_chart():
    # Load the Excel file
    file_path = 'gene_analysis.xlsx'  # Update with the correct path if necessary
    df = pd.read_excel(file_path)

    # Extract the necessary columns
    genes = df.iloc[:, 0]  # Assuming the first column contains gene names
    gene_presence = df['gene_presence_count']
    diversity = df['diversity_count']

    # Set up the bar positions
    x = range(len(genes))  # Number of genes
    width = 0.4  # Width of the bars

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot gene presence
    presence_bars = plt.bar(x, gene_presence, width=width, label='Gene Presence', color='b', align='center')

    # Plot diversity
    diversity_bars = plt.bar([i + width for i in x], diversity, width=width, label='Diversity', color='r',
                             align='center')

    # Add the gene presence numbers on top of each bar
    for bar in presence_bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=10,
                 color='black')

    # Add the diversity numbers on top of each bar
    for bar in diversity_bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=10,
                 color='black')

    # Set the labels and title
    plt.xlabel('Gene Name')
    plt.ylabel('Counts')
    plt.title('Gene Presence and Diversity')
    plt.xticks([i + width / 2 for i in x], genes, rotation=90)

    # Add a legend
    plt.legend()

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.savefig("gene_diversity.png", dpi=300)
    plt.show()


def generate_grouped_chart():

    file_path = r'D:\programming\NCBI_PROJECT_\results\gene_analysis.xlsx'
    df = pd.read_excel(file_path)

    # Define the gene-to-group mapping
    # Define the gene-to-group mapping
    gene_to_group = {
        # Group 1: Motility and Flagellar Function
        'flag': 'Motility and Flagellar Function',
        'flgm': 'Motility and Flagellar Function',
        'flil': 'Motility and Flagellar Function',
        'flia': 'Motility and Flagellar Function',
        'flik': 'Motility and Flagellar Function',
        'jhp_1117': 'Motility and Flagellar Function',
        'motb': 'Motility and Flagellar Function',
        'flim': 'Motility and Flagellar Function',
        'flii': 'Motility and Flagellar Function',
        'flge1': 'Motility and Flagellar Function',
        'flgb': 'Motility and Flagellar Function',
        'flid': 'Motility and Flagellar Function',
        'flgl': 'Motility and Flagellar Function',
        'flgk': 'Motility and Flagellar Function',
        'flab': 'Motility and Flagellar Function',

        # Group 2: Outer Membrane and Adherence
        'homd': 'Outer Membrane and Adherence',
        'alpb': 'Outer Membrane and Adherence',
        'homb': 'Outer Membrane and Adherence',
        'hpylss1_01113': 'Outer Membrane and Adherence',
        'hpylss1_01021': 'Outer Membrane and Adherence',
        'hpylss1_01469': 'Outer Membrane and Adherence',
        'hcpe': 'Outer Membrane and Adherence',

        # Group 3: Secretion Systems and Pathogenicity
        'cagw': 'Secretion Systems and Pathogenicity',
        'caga': 'Secretion Systems and Pathogenicity',
        'cag26-caga': 'Secretion Systems and Pathogenicity',
        'cag24-cagd': 'Secretion Systems and Pathogenicity',
        'cage': 'Secretion Systems and Pathogenicity',
        'cagl': 'Secretion Systems and Pathogenicity',

        # Group 4: Efflux Pumps and Resistance
        'hp0497': 'Efflux Pumps and Resistance',
        'hp0939': 'Efflux Pumps and Resistance',
        'hpg27_715': 'Efflux Pumps and Resistance',
        'hpg27_526': 'Efflux Pumps and Resistance',
        'kefb': 'Efflux Pumps and Resistance',

        # Group 5: Quorum Sensing and Signal Transduction
        'luxs': 'Quorum Sensing and Signal Transduction',
        'tlpb': 'Quorum Sensing and Signal Transduction',
        'arsr': 'Quorum Sensing and Signal Transduction',

        # Group 6: Biofilm and Cell Wall Synthesis
        'mltd': 'Cell Wall Synthesis',
        'pgda': 'Cell Wall Synthesis',
        'fuct': 'Cell Wall Synthesis',
        'lpxb': 'Cell Wall Synthesis',
        'lptb': 'Cell Wall Synthesis',

        # Group 7: Ribosomal and Protein Synthesis
        'rplr': 'Ribosomal and Protein Synthesis',
        'rplw': 'Ribosomal and Protein Synthesis',
        'rpln': 'Ribosomal and Protein Synthesis',
        'rpld': 'Ribosomal and Protein Synthesis',
        'rplb': 'Ribosomal and Protein Synthesis',
        'rplf': 'Ribosomal and Protein Synthesis',
        'rpmf': 'Ribosomal and Protein Synthesis',
        'rpls': 'Ribosomal and Protein Synthesis',
        'rple': 'Ribosomal and Protein Synthesis',
        'rplv': 'Ribosomal and Protein Synthesis',
        'rpmg': 'Ribosomal and Protein Synthesis',
        'rpse': 'Ribosomal and Protein Synthesis',
        'rpsg': 'Ribosomal and Protein Synthesis',
        'rpsc': 'Ribosomal and Protein Synthesis',
        'rpsk': 'Ribosomal and Protein Synthesis',
        'rpsd': 'Ribosomal and Protein Synthesis',
        'fusa': 'Ribosomal and Protein Synthesis',
        'tufa': 'Ribosomal and Protein Synthesis',
        'yigz': 'Ribosomal and Protein Synthesis',

        # Group 8: Metabolism and Enzymatic Activity
        'napa': 'Metabolism and Enzymatic Activity',
        'upps': 'Metabolism and Enzymatic Activity',
        'thie': 'Metabolism and Enzymatic Activity',
        'folk': 'Metabolism and Enzymatic Activity',
        'ribh': 'Metabolism and Enzymatic Activity',

        # Group 9: Hypothetical and Uncharacterized Proteins
        'k747_09130': 'Hypothetical and Uncharacterized Proteins',
        'hpg27_166': 'Hypothetical and Uncharacterized Proteins',
        'hpylss1_00252': 'Hypothetical and Uncharacterized Proteins',
    }


    # Map genes to groups
    df['Group'] = df.iloc[:, 0].map(gene_to_group)

    # Aggregate by group
    grouped_data = df.groupby('Group').agg(
        gene_presence_count=('gene_presence_count', 'sum'),
        diversity_count=('diversity_count', 'sum')
    ).reset_index()

    # Extract grouped data
    groups = grouped_data['Group']
    group_presence = grouped_data['gene_presence_count']
    group_diversity = grouped_data['diversity_count']

    # Set up the bar positions
    x = range(len(groups))  # Number of groups
    width = 0.4  # Width of the bars

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot gene presence for groups
    presence_bars = plt.bar(x, group_presence, width=width, label='Gene Presence', color='b', align='center')

    # Plot diversity for groups
    diversity_bars = plt.bar([i + width for i in x], group_diversity, width=width, label='Diversity', color='r',
                             align='center')

    # Add the gene presence numbers on top of each bar
    for bar in presence_bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=10,
                 color='black')

    # Add the diversity numbers on top of each bar
    for bar in diversity_bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=10,
                 color='black')

    # Set the labels and title
    plt.xlabel('Gene Group')
    plt.ylabel('Counts')
    plt.title('Gene Presence and Diversity by Group')
    plt.xticks([i + width / 2 for i in x], groups, rotation=45)

    # Add a legend
    plt.legend()

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.savefig("grouped_gene_diversity.png", dpi=300)
    plt.show()


def generate_grouped_chart_horizontal():
    file_path = r'D:\programming\NCBI_PROJECT_\results\gene_analysis.xlsx'
    df = pd.read_excel(file_path)

    # Define the gene-to-group mapping
    gene_to_group = {
        'flag': 'Motility and Flagellar Function',
        'flgm': 'Motility and Flagellar Function',
        'flil': 'Motility and Flagellar Function',
        'flia': 'Motility and Flagellar Function',
        'flik': 'Motility and Flagellar Function',
        'jhp_1117': 'Motility and Flagellar Function',
        'motb': 'Motility and Flagellar Function',
        'flim': 'Motility and Flagellar Function',
        'flii': 'Motility and Flagellar Function',
        'flge1': 'Motility and Flagellar Function',
        'flgb': 'Motility and Flagellar Function',
        'flid': 'Motility and Flagellar Function',
        'flgl': 'Motility and Flagellar Function',
        'flgk': 'Motility and Flagellar Function',
        'flab': 'Motility and Flagellar Function',
        'homd': 'Outer Membrane and Adherence',
        'alpb': 'Outer Membrane and Adherence',
        'homb': 'Outer Membrane and Adherence',
        'hpylss1_01113': 'Outer Membrane and Adherence',
        'hpylss1_01021': 'Outer Membrane and Adherence',
        'hpylss1_01469': 'Outer Membrane and Adherence',
        'hcpe': 'Outer Membrane and Adherence',
        'cagw': 'Secretion Systems and Pathogenicity',
        'caga': 'Secretion Systems and Pathogenicity',
        'cag26-caga': 'Secretion Systems and Pathogenicity',
        'cag24-cagd': 'Secretion Systems and Pathogenicity',
        'cage': 'Secretion Systems and Pathogenicity',
        'cagl': 'Secretion Systems and Pathogenicity',
        'hp0497': 'Efflux Pumps and Resistance',
        'hp0939': 'Efflux Pumps and Resistance',
        'hpg27_715': 'Efflux Pumps and Resistance',
        'hpg27_526': 'Efflux Pumps and Resistance',
        'kefb': 'Efflux Pumps and Resistance',
        'luxs': 'Quorum Sensing and Signal Transduction',
        'tlpb': 'Quorum Sensing and Signal Transduction',
        'arsr': 'Quorum Sensing and Signal Transduction',
        'mltd': 'Cell Wall Synthesis',
        'pgda': 'Cell Wall Synthesis',
        'fuct': 'Cell Wall Synthesis',
        'lpxb': 'Cell Wall Synthesis',
        'lptb': 'Cell Wall Synthesis',
        'rplr': 'Ribosomal and Protein Synthesis',
        'rplw': 'Ribosomal and Protein Synthesis',
        'rpln': 'Ribosomal and Protein Synthesis',
        'rpld': 'Ribosomal and Protein Synthesis',
        'rplb': 'Ribosomal and Protein Synthesis',
        'rplf': 'Ribosomal and Protein Synthesis',
        'rpmf': 'Ribosomal and Protein Synthesis',
        'rpls': 'Ribosomal and Protein Synthesis',
        'rple': 'Ribosomal and Protein Synthesis',
        'rplv': 'Ribosomal and Protein Synthesis',
        'rpmg': 'Ribosomal and Protein Synthesis',
        'rpse': 'Ribosomal and Protein Synthesis',
        'rpsg': 'Ribosomal and Protein Synthesis',
        'rpsc': 'Ribosomal and Protein Synthesis',
        'rpsk': 'Ribosomal and Protein Synthesis',
        'rpsd': 'Ribosomal and Protein Synthesis',
        'fusa': 'Ribosomal and Protein Synthesis',
        'tufa': 'Ribosomal and Protein Synthesis',
        'yigz': 'Ribosomal and Protein Synthesis',
        'napa': 'Metabolism and Enzymatic Activity',
        'upps': 'Metabolism and Enzymatic Activity',
        'thie': 'Metabolism and Enzymatic Activity',
        'folk': 'Metabolism and Enzymatic Activity',
        'ribh': 'Metabolism and Enzymatic Activity',
        'k747_09130': 'Hypothetical and Uncharacterized Proteins',
        'hpg27_166': 'Hypothetical and Uncharacterized Proteins',
        'hpylss1_00252': 'Hypothetical and Uncharacterized Proteins',
    }

    # Map genes to groups
    df['Group'] = df.iloc[:, 0].map(gene_to_group)

    # Remove rows where genes are not mapped
    df = df.dropna(subset=['Group'])

    # Aggregate by group
    grouped_data = df.groupby('Group').agg(
        gene_presence_count=('gene_presence_count', 'sum'),
        diversity_count=('diversity_count', 'sum')
    ).reset_index()

    # Extract grouped data
    groups = grouped_data['Group']
    group_presence = grouped_data['gene_presence_count']
    group_diversity = grouped_data['diversity_count']

    # Set up the bar positions
    y = range(len(groups))  # Number of groups
    width = 0.4  # Width of the bars

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot gene presence for groups (horizontal bars)
    plt.barh(y, group_presence, height=width, label='Gene Presence', color='b')

    # Plot diversity for groups (horizontal bars)
    plt.barh([i + width for i in y], group_diversity, height=width, label='Diversity', color='r')

    # Add the gene presence numbers on the bars
    for i, v in enumerate(group_presence):
        plt.text(v, y[i], str(v), ha='left', va='center', fontsize=10, color='black')

    # Add the diversity numbers on the bars
    for i, v in enumerate(group_diversity):
        plt.text(v, y[i] + width, str(v), ha='left', va='center', fontsize=10, color='black')

    # Set the labels and title
    plt.ylabel('Gene Group')
    plt.xlabel('Counts')
    plt.title('Gene Presence and Diversity by Group')

    # Set the y-ticks
    plt.yticks([i + width / 2 for i in y], groups)

    # Add a legend
    plt.legend()

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.savefig("grouped_gene_diversity_horizontal.png", dpi=300)
    plt.show()

def generate_normalized_grouped_chart():
    # Load the Excel file
    file_path = r'D:\programming\NCBI_PROJECT_\results\gene_analysis.xlsx'
    df = pd.read_excel(file_path)

    # Define the gene-to-group mapping
    gene_to_group = {
        # Group 1: Motility and Flagellar Function
        'flag': 'Motility and Flagellar Function',
        'flgm': 'Motility and Flagellar Function',
        'flil': 'Motility and Flagellar Function',
        'flia': 'Motility and Flagellar Function',
        'flik': 'Motility and Flagellar Function',
        'jhp_1117': 'Motility and Flagellar Function',
        'motb': 'Motility and Flagellar Function',
        'flim': 'Motility and Flagellar Function',
        'flii': 'Motility and Flagellar Function',
        'flge1': 'Motility and Flagellar Function',
        'flgb': 'Motility and Flagellar Function',
        'flid': 'Motility and Flagellar Function',
        'flgl': 'Motility and Flagellar Function',
        'flgk': 'Motility and Flagellar Function',
        'flab': 'Motility and Flagellar Function',

        # Group 2: Outer Membrane and Adherence
        'homd': 'Outer Membrane and Adherence',
        'alpb': 'Outer Membrane and Adherence',
        'homb': 'Outer Membrane and Adherence',
        'hpylss1_01113': 'Outer Membrane and Adherence',
        'hpylss1_01021': 'Outer Membrane and Adherence',
        'hpylss1_01469': 'Outer Membrane and Adherence',
        'hcpe': 'Outer Membrane and Adherence',

        # Group 3: Secretion Systems and Pathogenicity
        'cagw': 'Secretion Systems and Pathogenicity',
        'caga': 'Secretion Systems and Pathogenicity',
        'cag26-caga': 'Secretion Systems and Pathogenicity',
        'cag24-cagd': 'Secretion Systems and Pathogenicity',
        'cage': 'Secretion Systems and Pathogenicity',
        'cagl': 'Secretion Systems and Pathogenicity',

        # Group 4: Efflux Pumps and Resistance
        'hp0497': 'Efflux Pumps and Resistance',
        'hp0939': 'Efflux Pumps and Resistance',
        'hpg27_715': 'Efflux Pumps and Resistance',
        'hpg27_526': 'Efflux Pumps and Resistance',
        'kefb': 'Efflux Pumps and Resistance',

        # Group 5: Quorum Sensing and Signal Transduction
        'luxs': 'Quorum Sensing and Signal Transduction',
        'tlpb': 'Quorum Sensing and Signal Transduction',
        'arsr': 'Quorum Sensing and Signal Transduction',

        # Group 6: Biofilm and Cell Wall Synthesis
        'mltd': 'Cell Wall Synthesis',
        'pgda': 'Cell Wall Synthesis',
        'fuct': 'Cell Wall Synthesis',
        'lpxb': 'Cell Wall Synthesis',
        'lptb': 'Cell Wall Synthesis',

        # Group 7: Ribosomal and Protein Synthesis
        'rplr': 'Ribosomal and Protein Synthesis',
        'rplw': 'Ribosomal and Protein Synthesis',
        'rpln': 'Ribosomal and Protein Synthesis',
        'rpld': 'Ribosomal and Protein Synthesis',
        'rplb': 'Ribosomal and Protein Synthesis',
        'rplf': 'Ribosomal and Protein Synthesis',
        'rpmf': 'Ribosomal and Protein Synthesis',
        'rpls': 'Ribosomal and Protein Synthesis',
        'rple': 'Ribosomal and Protein Synthesis',
        'rplv': 'Ribosomal and Protein Synthesis',
        'rpmg': 'Ribosomal and Protein Synthesis',
        'rpse': 'Ribosomal and Protein Synthesis',
        'rpsg': 'Ribosomal and Protein Synthesis',
        'rpsc': 'Ribosomal and Protein Synthesis',
        'rpsk': 'Ribosomal and Protein Synthesis',
        'rpsd': 'Ribosomal and Protein Synthesis',
        'fusa': 'Ribosomal and Protein Synthesis',
        'tufa': 'Ribosomal and Protein Synthesis',
        'yigz': 'Ribosomal and Protein Synthesis',

        # Group 8: Metabolism and Enzymatic Activity
        'napa': 'Metabolism and Enzymatic Activity',
        'upps': 'Metabolism and Enzymatic Activity',
        'thie': 'Metabolism and Enzymatic Activity',
        'folk': 'Metabolism and Enzymatic Activity',
        'ribh': 'Metabolism and Enzymatic Activity',

        # Group 9: Hypothetical and Uncharacterized Proteins
        'k747_09130': 'Hypothetical and Uncharacterized Proteins',
        'hpg27_166': 'Hypothetical and Uncharacterized Proteins',
        'hpylss1_00252': 'Hypothetical and Uncharacterized Proteins',
    }


    # Map genes to groups
    df['Group'] = df.iloc[:, 0].map(gene_to_group)

    # Calculate the number of genes in each group
    gene_counts = df.groupby('Group').size().rename('gene_count')

    # Aggregate data by group
    grouped_data = df.groupby('Group').agg(
        total_gene_presence=('gene_presence_count', 'sum'),
        total_diversity=('diversity_count', 'sum')
    ).reset_index()

    # Merge gene counts
    grouped_data = grouped_data.merge(gene_counts, on='Group')

    # Normalize counts
    grouped_data['normalized_gene_presence'] = grouped_data['total_gene_presence'] / grouped_data['gene_count']
    grouped_data['normalized_diversity'] = grouped_data['total_diversity'] / grouped_data['gene_count']

    # Extract grouped data
    groups = grouped_data['Group']
    normalized_presence = grouped_data['normalized_gene_presence']
    normalized_diversity = grouped_data['normalized_diversity']

    # Set up the bar positions
    x = range(len(groups))  # Number of groups
    width = 0.4  # Width of the bars

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot normalized gene presence for groups
    presence_bars = plt.bar(x, normalized_presence, width=width, label='Normalized Gene Presence', color='b', align='center')

    # Plot normalized diversity for groups
    diversity_bars = plt.bar([i + width for i in x], normalized_diversity, width=width, label='Normalized Diversity', color='r', align='center')

    # Add the normalized gene presence numbers on top of each bar
    for bar in presence_bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=10, color='black')

    # Add the normalized diversity numbers on top of each bar
    for bar in diversity_bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=10, color='black')

    # Set the labels and title
    plt.xlabel('Gene Group')
    plt.ylabel('Normalized Counts (Per Gene)')
    plt.title('Normalized Gene Presence and Diversity by Group')
    plt.xticks([i + width / 2 for i in x], groups, rotation=45)

    # Add a legend
    plt.legend()

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.savefig("normalized_grouped_gene_diversity.png", dpi=300)
    plt.show()



def generate_horizentally_normalized_grouped_chart():
    # Load the Excel file
    file_path = r'D:\programming\NCBI_PROJECT_\results\gene_analysis.xlsx'
    df = pd.read_excel(file_path)

    # Define the gene-to-group mapping
    gene_to_group = {
        # Group 1: Motility and Flagellar Function
        'flag': 'Motility and Flagellar Function',
        'flgm': 'Motility and Flagellar Function',
        'flil': 'Motility and Flagellar Function',
        'flia': 'Motility and Flagellar Function',
        'flik': 'Motility and Flagellar Function',
        'jhp_1117': 'Motility and Flagellar Function',
        'motb': 'Motility and Flagellar Function',
        'flim': 'Motility and Flagellar Function',
        'flii': 'Motility and Flagellar Function',
        'flge1': 'Motility and Flagellar Function',
        'flgb': 'Motility and Flagellar Function',
        'flid': 'Motility and Flagellar Function',
        'flgl': 'Motility and Flagellar Function',
        'flgk': 'Motility and Flagellar Function',
        'flab': 'Motility and Flagellar Function',

        # Group 2: Outer Membrane and Adherence
        'homd': 'Outer Membrane and Adherence',
        'alpb': 'Outer Membrane and Adherence',
        'homb': 'Outer Membrane and Adherence',
        'hpylss1_01113': 'Outer Membrane and Adherence',
        'hpylss1_01021': 'Outer Membrane and Adherence',
        'hpylss1_01469': 'Outer Membrane and Adherence',
        'hcpe': 'Outer Membrane and Adherence',

        # Group 3: Secretion Systems and Pathogenicity
        'cagw': 'Secretion Systems and Pathogenicity',
        'caga': 'Secretion Systems and Pathogenicity',
        'cag26-caga': 'Secretion Systems and Pathogenicity',
        'cag24-cagd': 'Secretion Systems and Pathogenicity',
        'cage': 'Secretion Systems and Pathogenicity',
        'cagl': 'Secretion Systems and Pathogenicity',

        # Group 4: Efflux Pumps and Resistance
        'hp0497': 'Efflux Pumps and Resistance',
        'hp0939': 'Efflux Pumps and Resistance',
        'hpg27_715': 'Efflux Pumps and Resistance',
        'hpg27_526': 'Efflux Pumps and Resistance',
        'kefb': 'Efflux Pumps and Resistance',

        # Group 5: Quorum Sensing and Signal Transduction
        'luxs': 'Quorum Sensing and Signal Transduction',
        'tlpb': 'Quorum Sensing and Signal Transduction',
        'arsr': 'Quorum Sensing and Signal Transduction',

        # Group 6:Cell Wall Synthesis
        'mltd': 'Cell Wall Synthesis',
        'pgda': 'Cell Wall Synthesis',
        'fuct': 'Cell Wall Synthesis',
        'lpxb': 'Cell Wall Synthesis',
        'lptb': 'Cell Wall Synthesis',

        # Group 7: Ribosomal and Protein Synthesis
        'rplr': 'Ribosomal and Protein Synthesis',
        'rplw': 'Ribosomal and Protein Synthesis',
        'rpln': 'Ribosomal and Protein Synthesis',
        'rpld': 'Ribosomal and Protein Synthesis',
        'rplb': 'Ribosomal and Protein Synthesis',
        'rplf': 'Ribosomal and Protein Synthesis',
        'rpmf': 'Ribosomal and Protein Synthesis',
        'rpls': 'Ribosomal and Protein Synthesis',
        'rple': 'Ribosomal and Protein Synthesis',
        'rplv': 'Ribosomal and Protein Synthesis',
        'rpmg': 'Ribosomal and Protein Synthesis',
        'rpse': 'Ribosomal and Protein Synthesis',
        'rpsg': 'Ribosomal and Protein Synthesis',
        'rpsc': 'Ribosomal and Protein Synthesis',
        'rpsk': 'Ribosomal and Protein Synthesis',
        'rpsd': 'Ribosomal and Protein Synthesis',
        'fusa': 'Ribosomal and Protein Synthesis',
        'tufa': 'Ribosomal and Protein Synthesis',
        'yigz': 'Ribosomal and Protein Synthesis',

        # Group 8: Metabolism and Enzymatic Activity
        'napa': 'Metabolism and Enzymatic Activity',
        'upps': 'Metabolism and Enzymatic Activity',
        'thie': 'Metabolism and Enzymatic Activity',
        'folk': 'Metabolism and Enzymatic Activity',
        'ribh': 'Metabolism and Enzymatic Activity',

        # Group 9: Hypothetical and Uncharacterized Proteins
        'k747_09130': 'Hypothetical and Uncharacterized Proteins',
        'hpg27_166': 'Hypothetical and Uncharacterized Proteins',
        'hpylss1_00252': 'Hypothetical and Uncharacterized Proteins',
    }


    # Map genes to groups
    df['Group'] = df.iloc[:, 0].map(gene_to_group)

    # Calculate the number of genes in each group
    gene_counts = df.groupby('Group').size().rename('gene_count')

    # Aggregate data by group
    grouped_data = df.groupby('Group').agg(
        total_gene_presence=('gene_presence_count', 'sum'),
        total_diversity=('diversity_count', 'sum')
    ).reset_index()

    # Merge gene counts
    grouped_data = grouped_data.merge(gene_counts, on='Group')

    # Normalize counts
    grouped_data['normalized_gene_presence'] = grouped_data['total_gene_presence'] / grouped_data['gene_count']
    grouped_data['normalized_diversity'] = grouped_data['total_diversity'] / grouped_data['gene_count']

    # Extract grouped data
    groups = grouped_data['Group']
    normalized_presence = grouped_data['normalized_gene_presence']
    normalized_diversity = grouped_data['normalized_diversity']

    # Set up the bar positions
    y = range(len(groups))  # Number of groups
    height = 0.4  # Height of the bars

    # Create the plot
    plt.figure(figsize=(12, 8))

    # Plot normalized gene presence for groups
    presence_bars = plt.barh(y, normalized_presence, height=height, label='Normalized Gene Presence', color='b', align='center')

    # Plot normalized diversity for groups
    diversity_bars = plt.barh([i + height for i in y], normalized_diversity, height=height, label='Normalized Diversity', color='r', align='center')

    # Add the normalized gene presence numbers next to each bar
    for bar in presence_bars:
        xval = bar.get_width()
        plt.text(xval, bar.get_y() + bar.get_height() / 2, f'{xval:.2f}', va='center', ha='left', fontsize=10, color='black')

    # Add the normalized diversity numbers next to each bar
    for bar in diversity_bars:
        xval = bar.get_width()
        plt.text(xval, bar.get_y() + bar.get_height() / 2, f'{xval:.2f}', va='center', ha='left', fontsize=10, color='black')

    # Set the labels and title
    plt.ylabel('Gene Group')
    plt.xlabel('Normalized Counts (Per Gene)')
    plt.title('Normalized Gene Presence and Diversity by Group')
    plt.yticks([i + height / 2 for i in y], groups)

    # Add a legend
    plt.legend()

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.savefig("normalized_grouped_gene_diversity_horizontal.png", dpi=300)
    plt.show()


generate_grouped_chart()
generate_grouped_chart_horizontal()
generate_normalized_grouped_chart()
generate_horizentally_normalized_grouped_chart()