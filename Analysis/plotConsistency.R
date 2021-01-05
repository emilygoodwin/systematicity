rm(list=ls())
library(tidyverse)
library(rmarkdown)
library(ggplot2)
library(knitr)
library(entropy)
library(kableExtra)

setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step0")
ttr0 = read_csv("ttrs0")
setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step2")
ttr2 = read_csv("ttrs2")


out0 = ttr0 %>% group_by(encoder, Acorrect, VblockAhyp, NblockAhyp, series) %>% 
  summarize(blockmean= mean(BScore)) %>%
  group_by(encoder, Acorrect) %>%
  summarize(meanacc = mean(blockmean), sd = sd(blockmean)) %>% 
  mutate(Encoder = encoder) %>%
  mutate(Relation = Acorrect) %>%
  mutate(scores = paste(round(meanacc*100, digits = 2),  " (", round(sd*100, digits =2), ")", sep = "")) %>%
  ungroup() %>%
  select(-c(meanacc, sd, Acorrect, encoder))
relations = out0 %>% filter(Encoder == "BGRU") %>% select(2) 
BGRUscores2 = out0 %>% filter(Encoder == "BGRU") %>% select(3) 
CONVscores2 = out0 %>% filter(Encoder == "CONV") %>% select(3) 
INNRscores2 = out0 %>% filter(Encoder == "INNR") %>% select(3) 
INFSscores2 = out0 %>% filter(Encoder == "INFS") %>% select(3) 
all0 = cbind(relations, BGRUscores2, CONVscores2, INNRscores2, INFSscores2)
names(all0) <- c("Relation", "BGRU", "CONV", "INNR", "INFS")

out2 = ttr2 %>% group_by(encoder, Acorrect, VblockAhyp, NblockAhyp, series) %>% 
  summarize(blockmean= mean(BScore)) %>%
  group_by(encoder, Acorrect) %>%
  summarize(meanacc = mean(blockmean), sd = sd(blockmean)) %>% 
  mutate(Encoder = encoder) %>%
  mutate(Relation = Acorrect) %>%
  mutate(scores = paste(round(meanacc*100, digits = 2),  " (", round(sd*100, digits =2), ")", sep = "")) %>%
  ungroup() %>%
  select(-c(meanacc, sd, Acorrect, encoder))
relations = out2 %>% filter(Encoder == "BGRU") %>% select(2) 
BGRUscores2 = out2 %>% filter(Encoder == "BGRU") %>% select(3) 
CONVscores2 = out2 %>% filter(Encoder == "CONV") %>% select(3) 
INNRscores2 = out2 %>% filter(Encoder == "INNR") %>% select(3) 
INFSscores2 = out2 %>% filter(Encoder == "INFS") %>% select(3) 
all2 = cbind(relations, BGRUscores2, CONVscores2, INNRscores2, INFSscores2)
names(all2) <- c("Relation", "BGRU", "CONV", "INNR", "INFS")






latex0=kable(all0, "latex", booktabs = T) %>% 
  kable_styling(latex_options = c("striped","scale_down"))
latex2=kable(all2, "latex", booktabs = T) %>% 
  kable_styling(latex_options = c("striped","scale_down"))
latex0
