
library(tidyverse)
library(car)
library(broom)
library(patchwork)

## Read in the data and format it correctly
D_ar <- read_csv("./data/sum_final2.csv")
# Read in the annotations from the mega res database.
drug_ann_tmp <- read.csv("./data/megares_annotations_v3.00.csv", sep="|", skip=1, header=FALSE)
drug_ann <- drug_ann_tmp %>% 
  select(V3, V2) %>%
  rename(res_type = V3, res_ann = V2)

# Get a list for later of the unique types of antibiotic resistances
drug_v <- drug_ann %>% filter(res_ann == "Drugs") %>% pull(res_type) %>% unique()
# Format large list of drugs to only containing information from the list of unqiue drugs
Ddrug <- D_ar %>% select(gcf,any_of(drug_v))

# Get the number of unique drugs for each and view the distribution
Dsum <- Ddrug %>% 
  rowwise() %>% 
  mutate(ar_count = sum(pick(2:last_col()))) %>% 
  select(gcf, ar_count)
hist(Dsum$ar_count)

# Plot the number which are resistant in the large data
Dsum %>% mutate(ar_count = ifelse(ar_count == 0, "0", "1")) %>% 
  ggplot(aes(ar_count)) + geom_bar()
# Write the list of unique drugs to file, for manual annotation of wheter they target protein synthesis
as.data.frame(drug_v) %>% write_csv("drugann.csv")

D_ar <- Ddrug

# Connect to the DB
conn <- dbConnect(SQLite(),"../../s16.sqlite")
# List of all the tables
dbListTables(conn)
# read in ribdif
ribdif <- dbGetQuery(conn, "SELECT * FROM species_gcf2species_ribdif_info")
# Join the the ribdif table with the antibiotic resistance information table
D <- left_join(ribdif, D_ar, by="gcf") %>% 
  select(number_16s, total_div, genome_components,genus, Aminoglycosides:last_col())

# Further format the antibiotic resistance table
D <- D %>% mutate(across(Aminoglycosides:last_col(), ~replace_na(.x,0)))
D <- D %>% mutate(across(c(Aminoglycosides:last_col()), factor))

# Now join the table with tax information table
tax <- dbGetQuery(conn, "SELECT * FROM taxInfoFull") %>% 
  rename(genus=GENUS)
D_t <- left_join(tax,D, by="genus") %>% 
  select(phylum=PHYLUM, number_16s, genome_components,total_div:last_col())

# remove the phylum column
D_t <- select(D_t, -phylum)

# One column of the 30 000, did not have 16S info, which is wierd but too be expected
D_t <- D_t %>% filter(!is.na(number_16s)) 

# Now fit the model and step transform it 
fit <- lm(log2(total_div+0.1) ~ (.-number_16s-genome_components)*log2(genome_components)+log2(number_16s)-log2(genome_components):log2(number_16s), data=D_t)
#fit_plus <- lm(log2(total_div+0.1) ~ (.-number_16s-genome_components)+log2(number_16s)  , data=D_t)
fit_plus <- stats::step(fit,  scope=~(.-number_16s-genome_components)*log2(genome_components)+log2(number_16s)-log2(genome_components):log2(number_16s) , direction = "both", test="F", k=log(nrow(D_t)))

## Now predict the EMM for the found resistances and save it in a dataframe callded df
types <- c("Fosfomycin","betalactams", "Rifampin",
  "Bacitracin","Phenicol","MLS","Fluoroquinolones",
  "Elfamycins","Sulfonamides","Fusidic_acid",
  "Aminocoumarins","Mupirocin","Oxazolidinone","Tetracyclines",
  "Pleuromutilin","Nucleosides","Spiropyrimidinetriones",
  "Multi-drug_resistance")
df <- data.frame("types"=types)
df[2,1]
for(i in seq_along(types)){
  # Predict
  v <- c(1,3)
  pred <- ggpredict(fit_plus,terms = c(types[[i]], "genome_components [v]"))
  print(pred$predicted)
  # Extract values
  # GenomeC = 1 + Res
  g1r_pred <- pred$predicted[[3]]
  g1r_high <- pred$conf.high[[3]]
  g1r_low <- pred$conf.low[[3]]
  # GenomeC = 3 + Res
  g3r_pred <- pred$predicted[[4]]
  g3r_high <- pred$conf.high[[4]]
  g3r_low <- pred$conf.low[[4]]
  
  # Assign to df
  df[i,2] <- g1r_pred
  df[i,3] <- g1r_high
  df[i,4] <- g1r_low
  df[i,5] <- g3r_pred
  df[i,6] <- g3r_high
  df[i,7] <- g3r_low
}
pred

# Rename df
df <- df %>% rename(g1r_pred=V2,
              g1r_high=V3,
              g1r_low=V4,
              g3r_pred=V5,
              g3r_high=V6,
              g3r_low=V7)

# Read in the annotated drug info about whether they target protein synthesis
cur <- read.csv("./data/drug_curated_ann.csv", header=F, sep=";")
df_ann <- cur %>% 
  rename(types=V1) %>% 
  right_join(df, by="types") %>% 
  rename(target_protein = V3) %>% 
  mutate(target_protein = ifelse(target_protein == 1, "yes", "no"))

# Lastly plot the found estimated marginal means
p1 <- df_ann %>% 
  rename(`targets ribosome` = target_protein) %>% 
  mutate(types = fct_reorder(types, g1r_pred)) %>% 
  ggplot(aes(y=types,x=g1r_pred, fill=`targets ribosome`)) +
  geom_col() +
  geom_errorbar(aes(xmin=g1r_low,xmax=g1r_high)) +
  geom_vline(xintercept = 0.67) +
  labs(x="Entropy +0.1",title="Genome components = 1",y="")
p2 <- df_ann %>% 
  rename(`targets ribosome` = target_protein) %>% 
  mutate(types = fct_reorder(types, g1r_pred)) %>% 
  ggplot(aes(y=types,x=g3r_pred, fill=`targets ribosome`)) +
  geom_col() +
  geom_errorbar(aes(xmin=g3r_low,xmax=g3r_high)) +
  geom_vline(xintercept = 0.86) +
  labs(x="Entropy +0.1",title="Genome components = 3",y="")
p1 + p2 


