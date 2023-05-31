
import sys
import bacdive
import numpy as np
import pandas as pd
import random
from Bacdivefunctions import *
# Set random seed to date
random.seed(1502)


def retrive_tax_info(genus, df):
    """Function to correctly request and parse the information from the BacDive database"""

    # Get various information
    number_found = client.search(taxonomy=genus)
    
    # If no information for the entry was found, skip this entry
    if number_found == 0:
        return df
    
    # Go through each strain found and extract the relecant information
    for strain in client.retrieve():
        bacDat = dict()
        bacDat["genus"] = genus
        
        # Taxonomy
        try:
            tmp_dict = get_bacDat(["species","genus","family","order","class","phylum","domain"],strain["Name and taxonomic classification"]["LPSN"], "nominal")
            bacDat.update(tmp_dict)
        except KeyError:
            pass
        
        
        # Morphology
        try:
            data=strain["Morphology"]["cell morphology"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["motility","gram stain"],data, "nominal")
            bacDat.update(tmp_dict)
        
        
        # Temperature
        try:
            data=strain["Culture and growth conditions"]["culture temp"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = GetPH_or_Temp("temperature", data)
            bacDat.update(tmp_dict)
    
        # pH type
        try:
            data=strain["Culture and growth conditions"]["culture pH"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["PH range"],data, "nominal")
            bacDat.update(tmp_dict)


        # Get environmental information
        try:
            data=strain["Isolation, sampling and environmental information"]["taxonmaps"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["Total samples", "soil counts", "aquatic counts","plant counts"],data, "nominal")
            bacDat.update(tmp_dict)
            
        # Get GC content
        try:
            data=strain["Sequence information"]["GC content"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["GC-content"],data, "continuous")
            bacDat.update(tmp_dict)
            
        # Get NCBI tax ID
        try:
            data=strain["Sequence information"]["Genome sequences"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["NCBI tax ID"],data, "nominal")
            bacDat.update(tmp_dict)

        # Is it aerobe?
        try:
            data=strain["Physiology and metabolism"]["oxygen tolerance"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["oxygen tolerance"],data, "nominal")
            bacDat.update(tmp_dict)
            
        # Strain 
        try:
            data=strain["Name and taxonomic classification"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["strain designation"],data, "nominal")
            bacDat.update(tmp_dict)
        
        # Antibiotics
        try:
            data=strain["Physiology and metabolism"]["antibiotic resistance"]
        except KeyError:
            data=None
        # Format the antibiotic resistance correctly
        if data is not None:
            ar_dict = dict()
            has_AR = False
            
            # If there is several antibiotic resistance information:
            if type(data) is not list:
                # Define various information
                metabolite = data
                name = metabolite.get("metabolite")
                ar_or_not = metabolite.get("is antibiotic")
                resistent = metabolite.get("is resistant") 
                sens = metabolite.get("is sensitive")
                
                # Check if the strain is resistant
                # If it is resistant save the data as being resistant
                is_resistent = ar_or_not != "no" and resistent == "yes" and sens != "yes"
                if is_resistent:
                    ar_dict[name] = "R"
                    has_AR = True
                # If it is marked as sensitive to the antibiotic save this information
                is_sensitive = ar_or_not != "no" and resistent != "yes" and sens == "yes"
                if is_sensitive:
                    ar_dict[name] = "S"
            
            # If there is only one antibiotic resistance type:
            else:
                for metabolite in data:
                    name = metabolite.get("metabolite")
                    ar_or_not = metabolite.get("is antibiotic")
                    resistent = metabolite.get("is resistant") 
                    sens = metabolite.get("is sensitive")
                    # If it is resistant save the data as being resistant
                    is_resistent = ar_or_not != "no" and resistent == "yes" and sens != "yes"
                    if is_resistent:
                        ar_dict[name] = "R"
                        has_AR = True
                    # If it is marked as sensitive to the antibiotic save this information
                    is_sensitive = ar_or_not != "no" and resistent != "yes" and sens == "yes"
                    if is_sensitive:
                        ar_dict[name] = "S"
            
            # Save all antibiotics as seperate columns
            tmp_dict = dict()
            if has_AR:
                tmp_dict["antibiotics"] = "R"

            # Update the data with the found information
            tmp_dict.update(ar_dict)
            bacDat.update(tmp_dict)
    
        df = pd.concat([df, pd.DataFrame.from_records([bacDat])])
    return df
        

# Read in the genus list
with open("../../../makeDbFromRibDif/getListOfAllGenera/out/all_genus_names.dat") as genus_file:
    all_genus = genus_file.readlines()
    # Remove \n
    all_genus=[genus.strip() for genus in all_genus]

df = pd.DataFrame()

# Check if password for bacdive is given as argument
# To prevent password from being on git
if len(sys.argv) != 2:
    sys.exit("Please input bacdive code as input")
    
# Connect to the client
password = sys.argv[1]
client = bacdive.BacdiveClient("lasse101010@gmail.com", password)

all_genus = all_genus
# Run the function defined above for requesting and parseing the information from the BacDive database
# Do this in chunks for all genera.
out_file = "../out/BacdiveOut.csv"
chunk_size = 100
i = 0
for all_genus_subset in divide_chunks(all_genus, chunk_size):
    i += 1
    for pos, genus in enumerate(all_genus_subset):
        print("Finished:",pos,"of", len(all_genus_subset),"chunk:",i,"totalsize:", len(all_genus),"at genus:",genus)
        df = retrive_tax_info(genus, df)
    # write to .csv file. Only add header to first line
    if i == 1:
        df.to_csv(f"../data/{out_file}", index = False)
    else:
        df.to_csv(f"../data/{out_file}", mode="a", index = False, header=False)
    print("*"*15)
    print("Finished chunk:", i, "of:", len(all_genus)/chunk_size, "chunksize:", chunk_size)
    print("*"*15)

