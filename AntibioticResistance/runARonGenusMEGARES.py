# Ran script with: python3 runARonGenus.py > stdout_run1 2> stderr_run2 &
import subprocess
import os

# Set path for output from ribdif
path = "/mnt/raid2/s203512/bachelor/main/MakingAndProccesingData2Database/make_the_db/all_genus_ribdif-ed/"


# Read in the found genera
infile = open("/mnt/raid2/s203512/bachelor/DataPreparation/makeDbFromRibDif/getListOfAllGenera/out/all_genus_names.dat")

# Make sure gcf annotated under several genera does not get added twice
gcf_seen = list()

# Go trough each file
for i, genus in enumerate(infile):
    # Format genus from file
    genus = genus.strip()
    genus = "-".join(genus.split())
    
    # Set the correct dir for each genus 
    dir = path+genus+f"/refseq/bacteria/"
    # Get all the different gcf found for the specific assembly
    # Ignore if genus through ribdif did not have any entries
    try:
        all_gcf = os.listdir(dir)
    except FileNotFoundError:
        continue
    
    # Run abricate on all the different gcf found and save output as a file.
    print(f"Running on {genus}...")
    #print(gcf_seen)
    for gcf in all_gcf:
        # Run abricate on the gcf if it is not seen allready
        if gcf not in gcf_seen:
            gcf_seen = gcf_seen + [gcf]
            genomic_fasta = dir + gcf + f"/*genomic.fna"
            print(gcf)
            subprocess.run("abricate " + genomic_fasta +f" --db megaresdb -nopath > ../dataMEGARES2/{gcf}.arfound", shell = True) 
            
    print(f"Done with {genus}, number {i+1}")
 
