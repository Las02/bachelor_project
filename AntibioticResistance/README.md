
## Purpose
The purpose of this folder is to find antibiotic genes in the the genomes downloaded with Ribdif. This is done through using the tool Abricate with the MEGAres database of antibiotic resistance genes.

## Method and files
Fasta files of antibiotic genes were downloaded from https://www.meglab.org/megares/. For making the fasta files into a database for Abricate they were formatted with the following:

```
awk -F "|" '{if ($0 ~ />/) {gsub(">", ""); printf ">megares~~~%s~~~%s~~~%s\n", $1, $5,$4} else {print $0}}' < megares_Not_Formatted.fasta > /mnt/raid2/s203512/miniconda/db/megaresdb/sequences
```
After the files were moved to the correct location they were made into to a database with the following command:

```
makeblastdb -in sequences -title megares -dbtype nucl -hash_index
```
Based on this database abricate were run on all genomes found, with the script "runARonGenusMEGARES.py". After abricate were run, we filtered our antibiotic resistances which were defined by a specific SNP unless they had 100% coverage and identity. This was done based on the file "isSNP.csv" which contains the annotaed SNP antibiotic resistances from the MEGAres database. Lastly the found data were formatted correctly and joined at a antibiotic resistance level in the script "FormatARdata.R". 
