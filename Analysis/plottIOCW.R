rm(list=ls())
library(tidyverse)
library(rmarkdown)
library(ggplot2)
library(knitr)
library(entropy)
library(kableExtra)

setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step0")
frb0 = read_csv("freebies0")
setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step2")
frb2 = read_csv("freebies2")

t0 = frb0 %>% group_by(encoder, Acorrect, NblockAhyp) %>% 
  summarize(blockmean= mean(AScore)) %>%
  summarize(MeanAcc = mean(blockmean), sd = sd(blockmean)) %>% 
  mutate(scores = paste(round(MeanAcc*100, digits = 2), " (",round(sd*100, digits = 2), ")", sep = ""))

t2 = frb2 %>% group_by(encoder, Acorrect, NblockAhyp) %>% 
  summarize(blockmean= mean(AScore)) %>%
  summarize(MeanAcc = mean(blockmean), sd = sd(blockmean)) %>% 
  mutate(scores = paste(round(MeanAcc*100, digits = 2), " (",round(sd*100, digits = 2), ")", sep = ""))

relations = t2 %>% ungroup() %>% filter(encoder == "BGRU") %>% select(2)
BGRUscores2 = t2 %>% ungroup() %>% filter(encoder == "BGRU") %>% select(5)
CONVscores2 = t2 %>% ungroup() %>% filter(encoder == "CONV") %>% select(5)
INFSscores2 = t2 %>% ungroup() %>% filter(encoder == "INFS") %>% select(5)
INNRscores2 = t2 %>% ungroup() %>% filter(encoder == "INNR") %>% select(5)
all2 = cbind(relations, BGRUscores2, CONVscores2, INFSscores2, INNRscores2)
names(all2) <- c("Relation", "BGRU", "CONV", "INNR", "INFS")

relations = t0 %>% ungroup() %>% filter(encoder == "BGRU") %>% select(2)
BGRUscores0 = t0 %>% ungroup() %>% filter(encoder == "BGRU") %>% select(5)
CONVscores0 = t0 %>% ungroup() %>% filter(encoder == "CONV") %>% select(5)
INFSscores0 = t0 %>% ungroup() %>% filter(encoder == "INFS") %>% select(5)
INNRscores0 = t0 %>% ungroup() %>% filter(encoder == "INNR") %>% select(5)
all0 = cbind(relations, BGRUscores0, CONVscores0, INFSscores0, INNRscores0)
names(all0) <- c("Relation", "BGRU", "CONV", "INNR", "INFS")


latex=kable(all0, "latex", booktabs = T) %>% 
  kable_styling(latex_options = c("striped","scale_down"))
latex
latex=kable(all2, "latex", booktabs = T) %>% 
  kable_styling(latex_options = c("striped","scale_down"))
latex
