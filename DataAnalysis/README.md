## Purpose
This folder contains the files for the dataanalysis of the 16S gene copy number and the intragenomic gene diverstiy of the 16S genes. Additionally, it contains the files for training and evaluating the random forrest models build to predict spore formation.
Lastly, it also contains the files for preparing the data for modelling.

## Files
The files can be found in ./ 
The following is a describtion of the files 
01_ReadInData.Rmd                       -   Read in the data from the database, and other sources. Format it for modelling.  
02_PredictMissingSpore.Rmd              -   Train a Random Forrest model and use it to predict spore formation for NAN's.  
03_BuildModelOfN16S.Rmd                 -   Model the number of 16S gene copies as a function of other attributes in the data.  
04_RandomForrestOnlyN16sSeqlen.Rmd      -   Train a Random Forrest model to predict spore formation based on the number of 16S rRNA genes and the sequence length.  
05_RandomForrestAllAttributes.Rmd       -   Train a Random Forrest model to predict spore formation based on the other attributes in the data  
06_PlotsOfN16AndPCA.Rmd                 -   Analyse the model of the number of 16S gene copies. Additionally make a PCA plot of the attributes used for the Random Forrest models.  
07_BuildModelOfEntropyAndPlot.Rmd        -   Model the amount of entropy as a function of the other attributes in the data. And plot the results of the model  
08_BuildModelArMechanismsAndPlot.R      -   Model the entropy as a function of the different types of antibiotic resistance mechanims. Additionally plot the results  

## Data
The data can be found in ./data/
While the raw data used (and the data for modelling the effect of antibiotic resistance mechanisms on entropy), is not avalible in this Git, due to size constraints, the final data set used for analysis of both the 16S gene copy number, prediction of spore formation, and the intragenomic gene diversity (but not the antibiotic resistance mechanism) can be found in the following two files:

"pred_bacdive_growth_ribdif.rds" contains the data used for modelling the 16S gene copy number and the intragenomic gene diversity. Therby some of the values for spore formation are predicted

"bacdive_growth_ribdif.rds" contains the data before predicting spore formation. This is the dataset used for predicting spore formation

