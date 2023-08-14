import pandas as pd
import glob

# Read in the data about which antibiotic resistance genes come form a SNP
snp = pd.read_csv("isSNP.csv")
snp = snp["V1"].values
snp = [">"+x for x in snp]

# Go through each Abricate output and filter out each SNP if they do not have 100% coverage and 100% identity
files = glob.glob("../dataMEGARES3/*")
for path in files:
    file =  open(path, "r")
    file = file.readlines()
    out =  open(path, "w")

    print("file:",path)
    print("lines before", len(file))
    i=0
    for line in file:
        line = line.strip()
        line_split=line.split("\t")
        # Check if they have 100% coverage and 100% identity
        if line_split[4] in snp and line_split[8] != "100.00" and line_split[9] != "100.00":
            continue
        else:
            i+=1
            print(line, file=out)
    print("lines after", i)
