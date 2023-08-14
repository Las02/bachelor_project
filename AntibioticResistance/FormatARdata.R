library(tidyverse)
library(magrittr)
library(stringr)
library(RSQLite)

# Set the working directory
setwd("/mnt/raid2/s203512/bachelor/DataPreparation/FindARinDNA/scripts")

# Read in the data from the found antibiotic resistance genes based on the output from the abricate summary function
ar_d_read <- read_table("./megares_sum_after_del.tab")

# Filter out the strains which did not have any antibiotic resistance genes "abricate --summary"
ar_d <- ar_d_read %>% filter(!grepl(".arfound", `#FILE`))

# Format the coulmn containing the gcf code correctly
ar_d <- ar_d %>%
    rename(gcf = `#FILE`) %>%
    mutate(gcf = paste(str_split_i(gcf,"_",1),str_split_i(gcf,"_",2), sep="_"))


# Apply 1 hot enoding for the strain for the antibiotic resistance genes they contain.
# Only write a strain as containg the gene if the alignment has above 90% coverage
t <- 90
# Function to check if, given the input consist of several values, any values are above the threshold
any_above_threshold <- function(seq, t){
    split <- str_split(seq, ";")
    # If there is ; in the data check if any value is above the threshold
    if(length(split[[1]]) > 1){
    any_above_t <- FALSE
    for (i in seq_along(split[[1]])){
        num = as.double(split[[1]][i])
        if (num > t){
            any_above_t <- TRUE
            }
        }
    if(any_above_t){
        return("100.0")
        } else{return("0.00")
        }
    }
    # If it is not several values return the sequence
    return(seq)
}

# actually applying the 1 hot encoding
one_hot <- ar_d %>%
    mutate(across(3:last_col(), ~ifelse(.x == ".", "0", .x))) %>%
    mutate(across(3:last_col(), ~map(.x, ~any_above_threshold(.x, t)))) %>%
    mutate(across(3:last_col(), as.double)) %>%
    mutate(across(3:last_col(), ~ifelse(.x > t, 1, 0)))

## Join the megares annotations to the data
# Read in the data and format it
drug_ann_tmp <- read.csv("megares_annotations_v3.00.csv", sep="|", skip=1, header=FALSE)
drug_ann_tmp$V6 <- str_split_i(drug_ann_tmp$V6, ",",1)
drug_ann <- drug_ann_tmp %>% 
    select(V1, V3) %>%
    rename(res_type = V1, res_ann = V3)


# Join the two tables
ar_long_joined <- one_hot %>%
    pivot_longer(cols=3:last_col(), values_to = "is_res", names_to = "res_type") %>%
    mutate(res_type = gsub(">","",res_type)) %>%
    left_join(drug_ann, by="res_type", multiple = "all")

# Now collect them in mechanisms
final <- ar_long_joined %>%
    group_by(gcf, res_ann) %>%
    summarise(is_res = ifelse(1 %in% is_res, 1, 0))  %>%
    pivot_wider(names_from = res_ann, values_from = is_res)

# Find the sum of unique ar types
sum <- final %>%
    rowwise() %>%
    mutate(ar_count = sum(pick(2:last_col()), na.rm = TRUE)) %>%
    select(gcf, ar_count)

write.csv(final,"../sum_final2.csv")
write.csv(sum,"../wide_final2.csv")

