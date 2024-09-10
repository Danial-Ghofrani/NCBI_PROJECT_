import os
import subprocess
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

# Paths to your directories
concatenated_dir = "D:\\programming\\NCBI_PROJECT_\\concatenate"
output_dir = "D:\\programming\\NCBI_PROJECT_\\phylogeny"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Path to the MAFFT executable
mafft_path = r"D:\apps\MAFFT\mafft-win\mafft.bat"  # Replace with the actual path to your MAFFT executable

# Step 1: Collect all concatenated FASTA files
fasta_files = [f for f in os.listdir(concatenated_dir) if f.endswith('.fasta')]

# Initialize a list to store the aligned sequences
aligned_files = []

# Step 2: Perform Multiple Sequence Alignment (MSA) on each file
for fasta_file in fasta_files:
    input_path = os.path.join(concatenated_dir, fasta_file)
    output_path = os.path.join(output_dir, f"aligned_{fasta_file}")

    # Perform alignment using MAFFT
    result = subprocess.run([mafft_path, "--auto", input_path], capture_output=True, text=True)
    stdout = result.stdout

    with open(output_path, "w") as aligned_file:
        aligned_file.write(stdout)

    aligned_files.append(output_path)

# Step 3: Combine all aligned sequences into a single alignment
combined_alignment_path = os.path.join(output_dir, "combined_alignment.fasta")

with open(combined_alignment_path, "w") as outfile:
    for aligned_file in aligned_files:
        with open(aligned_file, "r") as infile:
            outfile.write(infile.read())

# Step 4: Load the combined alignment
alignment = AlignIO.read(combined_alignment_path, "fasta")

# Step 5: Calculate the distance matrix
calculator = DistanceCalculator('identity')
distance_matrix = calculator.get_distance(alignment)

# Step 6: Construct the phylogenetic tree using the distance matrix
constructor = DistanceTreeConstructor()
tree = constructor.nj(distance_matrix)

# Step 7: Save and visualize the tree
tree_output_path = os.path.join(output_dir, "phylogenetic_tree.xml")
Phylo.write(tree, tree_output_path, "phyloxml")

# Optional: Visualize the tree using matplotlib
Phylo.draw(tree)