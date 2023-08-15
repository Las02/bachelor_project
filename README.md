# Analysis of rRNA multiplicity and diversity
### Aim
The aim of this project was to establish correlations between the sequence diversity and copy 
number multiplicity of the 16S rRNA genes and bacterial traits and environmental factors. 
This was be done through data-mining both databases and bacterial genomes for 16S rRNA 
gene information and information about bacterias’ traits and the environment they live in. 
This information was then be used to build several statistical models that can explain the 16S 
rRNA gene’s variation in both copy number and degree of intragenomic sequence diversity.

### Folders
The files for the project is structured into 3 different main folders. Firstly, the folder "DataPreparation", which contains the files for gathering the data used for the project. Secondly, the folder "DataAnalysis" which contains the files for the dataanalysis in addition to files for preparing the data for modelling. Thirdly, the folder AntibioticResistance which contains the files for gathering information about antibiotic resistance mechanisms. A more in depht overview of the files can be found in the "README"s in the above mentioned folders.

### Abstract
Bacteria exhibit variability in the number of 16S rRNA gene copy numbers, and in the degree
of intragenomic sequence diversity between these copies. This variation affects microbial
community analysis based on 16S rRNA sequencing. Heterogeneity in the numbers of 16S
rRNA genes and in the intragenomic sequence diversity of these genes can lead to a
quantitative bias in the estimation of species abundance and diversity.  
However, how bacterial traits and environmental factors, such as spore formation, motility 
and bacterial habitat are correlated with the variation in the 16S rRNA gene’s multiplicity and 
diversity remains inadequately explored. The aim of this project was to address this gap. 
To investigate this, in addition to information about bacterial traits and environment, 16S 
rRNA genes was gathered from (already existing) databases and bacterial genomes. This 
information was then used to construct several statistical models to explore the impact of 
environmental factors and bacterial traits on both the 16S rRNA gene copy number and the 
degree of intragenomic diversity of the 16S rRNA genes.   
Firstly, we found 5 traits associated with the intragenomic 16S rRNA gene diversity, with the 
largest predictor being the number of 16S rRNA genes. Secondly, we found additional 
evidence supporting the hypothesis that copiotroph bacteria have a high number of 16S rRNA 
genes in comparison to oligotrophic bacteria. Thirdly, we found psychrophilic bacteria to 
have a higher number of 16S gene copies than would be expected based on their traits and 
habitat. Lastly, we found spore-forming bacteria to have a higher number of 16S rRNA gene 
copies in comparison to non-spore forming bacteria. We showed that spore formation in 
Actinomycetota and Bacilliota could be predicted with an accuracy of 0.90 and an AUC of 
0.95 based only on the genome size and the number of 16S rRNA genes. Overall, this project 
demonstrates that the number of 16S rRNA genes is correlated with bacterial ecology, while 
the intragenomic 16S rRNA gene diversity is mostly dependent on the number of 16S rRNA 
gene copies. This project therefore provides additional information for which to better 
understand the factors which can lead to bias in microbial community analysis when using 
16S rRNA sequencing.
