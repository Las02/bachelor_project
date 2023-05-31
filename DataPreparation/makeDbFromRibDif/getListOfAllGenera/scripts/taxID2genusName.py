
# Convert the found genus Taxids to their "normal" names
import requests
count = 0

# Define the url of the API
base_url = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/taxonomy/taxon/"

# Set the out file
outfile = open("../out/all_genus_names.dat","w")

# For each of the found tax id for the genera, "ask" the API for their name
errors = []
with open("../out/all_genus_taxid.dat") as file:
    for tax_id in file:
        endpoint = tax_id.strip()
        data = requests.get(base_url + endpoint).json()
        tax_info = data["taxonomy_nodes"]
        if len(tax_info) != 1:
            count += 1
        orgn = tax_info[0]["taxonomy"]["organism_name"]
        
        # If the found genus is not annotated as a genus, do not add it
        if tax_info[0]["taxonomy"]["rank"] != "GENUS":
            errors.append(orgn)
        else:
            print(orgn, file = outfile)
            
outfile.close()
            