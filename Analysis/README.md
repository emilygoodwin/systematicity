## Probe Analyses 

### Preparing the data

Point `format_data.py` at the results file from one experiment; it should write out a file `metadata.json`.

(Use `format_all.sh` to save you from manually running `format_data.py` on all of the output files individually.)


Then run `output_cruncher.py`, which reads in `metadata.json` and writes out CSV files with pairs of test items. 

### Plotting

To get the plots for known word perturbation probe:\
run `comparing_encoders_KWP.R` and then `plotKWP.R` \\

To get the plots for logical consistency probe:\
run `comparing_encoders_consistency.R` and then `plotConsistency.R` \\

To get the plots for logical consistency probe:\
run `comparing_encoders_IOCW.R` and then `plotIOCW.R`

### Word Embedding Analyses

Notebook  `word_analysis.ipynb` will analyze the word embeddings, try to cluster them (Figure 1 in the paper) and get some similarity metrics. \
