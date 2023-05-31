import pandas as pd
import glob
files = glob.glob("../dataMEGARES3/*")

snp = pd.read_csv("isSNP.csv")
snp = snp["V1"].values
snp = [">"+x for x in snp]

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
        if line_split[4] in snp and line_split[8] != "100.00" and line_split[9] != "100.00":
            continue
        else:
            i+=1
            print(line, file=out)
    print("lines after", i)