rm(list=ls())
library(tidyverse)
library(rmarkdown)
library(ggplot2)
library(knitr)
library(entropy)
library(kableExtra)

#Read in data, setup-------
setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step0")
BGRU10_0 = read_csv("wug10tests_BGRU.csv")
BGRU20_0 = read_csv("wug20tests_BGRU.csv")
BGRU30_0 = read_csv("wug30tests_BGRU.csv")
CONV10_0 = read_csv("wug10tests_ConvNet.csv")
CONV20_0 = read_csv("wug20tests_ConvNet.csv")
CONV30_0 = read_csv("wug30tests_ConvNet.csv")
INFS10_0 = read_csv("wug10tests_InferSent.csv")
INFS20_0 = read_csv("wug20tests_InferSent.csv")
INFS30_0 = read_csv("wug30tests_InferSent.csv")
INNR10_0 = read_csv("wug10tests_InnerAttentionMILA.csv")
INNR20_0 = read_csv("wug20tests_InnerAttentionMILA.csv")
INNR30_0 = read_csv("wug30tests_InnerAttentionMILA.csv")

setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step2")
BGRU10_2 = read_csv("wug10tests_BGRU.csv")
BGRU20_2 = read_csv("wug20tests_BGRU.csv")
BGRU30_2 = read_csv("wug30tests_BGRU.csv")
CONV10_2 = read_csv("wug10tests_ConvNet.csv")
CONV20_2 = read_csv("wug20tests_ConvNet.csv")
CONV30_2 = read_csv("wug30tests_ConvNet.csv")
INFS10_2 = read_csv("wug10tests_InferSent.csv")
INFS20_2 = read_csv("wug20tests_InferSent.csv")
INFS30_2 = read_csv("wug30tests_InferSent.csv")
INNR10_2 = read_csv("wug10tests_InnerAttentionMILA.csv")
INNR20_2 = read_csv("wug20tests_InnerAttentionMILA.csv")
INNR30_2 = read_csv("wug30tests_InnerAttentionMILA.csv")

cleanpairs <- function(dfm ){
  temp = dfm %>%
    mutate(AScore = as.integer(Acorrect == Apredicted)) 
  temp = temp %>%
    mutate(BScore = as.integer(`Bcorrect` == `Bpredicted`)) 
  
  temp = temp %>%
    mutate(NblockAprem = str_extract(temp$pairAprem, "N(\\d)*\\.\\d") %>% str_extract("N(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VblockAprem = str_extract(temp$pairAprem, "V(\\d)*\\.\\d") %>% str_extract("V(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(NitemAprem = str_extract(temp$pairAprem, "N(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VitemAprem = str_extract(temp$pairAprem, "V(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(NblockBprem = str_extract(temp$pairBprem, "N(\\d)*\\.\\d") %>% str_extract("N(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VblockBprem = str_extract(temp$pairBprem, "V(\\d)*\\.\\d") %>% str_extract("V(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(NitemBprem = str_extract(temp$pairBprem, "N(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VitemBprem = str_extract(temp$pairBprem, "V(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  
  temp = temp %>%
    mutate(NblockAhyp = str_extract(temp$pairAhyp, "N(\\d)*\\.\\d") %>% str_extract("N(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VblockAhyp = str_extract(temp$pairAhyp, "V(\\d)*\\.\\d") %>% str_extract("V(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(NitemAhyp = str_extract(temp$pairAhyp, "N(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VitemAhyp = str_extract(temp$pairAhyp, "V(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(NblockBhyp = str_extract(temp$pairBhyp, "N(\\d)*\\.\\d") %>% str_extract("N(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VblockBhyp = str_extract(temp$pairBhyp, "V(\\d)*\\.\\d") %>% str_extract("V(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(NitemBhyp = str_extract(temp$pairBhyp, "N(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(VitemBhyp = str_extract(temp$pairBhyp, "V(\\d)*\\.\\d") %>% str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(Ntarget = (NitemBprem == 3 | NitemBhyp == 3 | NitemAprem == 3 | NitemAhyp == 3)) %>%
    mutate(Vtarget = (VitemBprem == 3 | VitemBhyp == 3 | VitemAprem == 3 | VitemAhyp == 3)) 
  temp = temp %>%   
    filter(AScore != 0)
  
  temp = temp %>% mutate(`in` = str_remove(`in`, "\\(\\[")) %>%
    mutate(`out` = str_remove(`out`, "\\]")) %>%
    mutate(`out` = str_remove(`out`, "u'")) %>%
    mutate(`in` = str_remove(`in`, "u'")) %>%
    mutate(`diff` =  str_remove(`diff`, "\\)")) %>%
    mutate(`diff` =  str_remove(`diff`, "'")) %>%
    mutate(`diff` =  str_remove(`diff`, "'")) 
  
  temp = temp %>% mutate(`out`= str_replace(`out`, " '", "NONE")) %>% 
    mutate(`in`=str_replace(`in`, " '", "NONE")) %>% 
    mutate(`in`= str_replace(`in`, "(\\d)*\\.", "")) %>%
    mutate(`out`= str_replace(`out`, "(\\d)*\\.", "")) %>%
    mutate(`in`= str_replace(`in`, "'", "")) %>%
    mutate(`out`= str_replace(`out`, "'", ""))
  return(temp)
}
cleanitems <- function(dfm ){
  temp = dfm %>% 
    distinct(pairAprem, pairAhyp, .keep_all = TRUE) %>% 
    mutate(AScore = as.integer(Acorrect == Apredicted)) 
  temp = temp %>%
    select(-c(pairBprem, pairBhyp, Bcorrect, Bpredicted, `in`, out, diff, X12))
  temp = temp %>%
    mutate(NblockAprem = str_extract(temp$pairAprem, "N(\\d)*\\.\\d") %>% 
             str_extract("N(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>% 
    mutate(VblockAprem = str_extract(temp$pairAprem, "V(\\d)*\\.\\d") %>% 
             str_extract("V(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>% 
    mutate(NitemAprem = str_extract(temp$pairAprem, "N(\\d)*\\.\\d") %>%
             str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>% 
    mutate(VitemAprem = str_extract(temp$pairAprem, "V(\\d)*\\.\\d") %>% 
             str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>%
    mutate(NblockAhyp = str_extract(temp$pairAhyp, "N(\\d)*\\.\\d") %>% 
             str_extract("N(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>% 
    mutate(VblockAhyp = str_extract(temp$pairAhyp, "V(\\d)*\\.\\d") %>% 
             str_extract("V(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>% 
    mutate(NitemAhyp = str_extract(temp$pairAhyp, "N(\\d)*\\.\\d") %>% 
             str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  temp = temp %>% 
    mutate(VitemAhyp = str_extract(temp$pairAhyp, "V(\\d)*\\.\\d") %>% 
             str_extract("\\.(\\d)*") %>% str_extract("\\d+"))
  
  temp = temp %>% 
    mutate(Ntarget = (NitemAprem == 3 | NitemAhyp == 3)) %>% 
    mutate(Vtarget = (VitemAprem == 3 | VitemAhyp == 3))
  return(temp)
}

BGRU10_0i = BGRU10_0 %>% cleanitems() %>% mutate(condition = "0", series = "10", encoder = "BGRU")
BGRU20_0i = BGRU20_0 %>% cleanitems() %>% mutate(condition = "0", series = "20", encoder = "BGRU")
BGRU30_0i = BGRU30_0 %>% cleanitems() %>% mutate(condition = "0", series = "30", encoder = "BGRU")
BGRU0 = rbind(BGRU10_0i, BGRU20_0i, BGRU30_0i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(BGRU10_0i, BGRU20_0i, BGRU30_0i)
rm(BGRU10_0, BGRU20_0, BGRU30_0)
CONV10_0i = CONV10_0 %>% cleanitems() %>% mutate(condition = "0", series = "10", encoder = "CONV")
CONV20_0i = CONV20_0 %>% cleanitems() %>% mutate(condition = "0", series = "20", encoder = "CONV")
CONV30_0i = CONV30_0 %>% cleanitems() %>% mutate(condition = "0", series = "30", encoder = "CONV")
CONV0 = rbind(CONV10_0i, CONV20_0i, CONV30_0i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(CONV10_0i, CONV20_0i, CONV30_0i)
rm(CONV10_0, CONV20_0, CONV30_0)
INFS10_0i = INFS10_0 %>% cleanitems() %>% mutate(condition = "0", series = "10", encoder = "INFS")
INFS20_0i = INFS20_0 %>% cleanitems() %>% mutate(condition = "0", series = "20", encoder = "INFS")
INFS30_0i = INFS30_0 %>% cleanitems() %>% mutate(condition = "0", series = "30", encoder = "INFS")
INFS0 = rbind(INFS10_0i, INFS20_0i, INFS30_0i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(INFS10_0i, INFS20_0i, INFS30_0i)
rm(INFS10_0, INFS20_0, INFS30_0)
INNR10_0i = INNR10_0 %>% cleanitems() %>% mutate(condition = "0", series = "10", encoder = "INNR")
INNR20_0i = INNR20_0 %>% cleanitems() %>% mutate(condition = "0", series = "20", encoder = "INNR")
INNR30_0i = INNR30_0 %>% cleanitems() %>% mutate(condition = "0", series = "30", encoder = "INNR")
INNR0 = rbind(INNR10_0i, INNR20_0i, INNR30_0i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(INNR10_0i, INNR20_0i, INNR30_0i)
rm(INNR10_0, INNR20_0, INNR30_0)


BGRU10_2i = BGRU10_2 %>% cleanitems() %>% mutate(condition = "2", series = "10", encoder = "BGRU")
BGRU20_2i = BGRU20_2 %>% cleanitems() %>% mutate(condition = "2", series = "20", encoder = "BGRU")
BGRU30_2i = BGRU30_2 %>% cleanitems() %>% mutate(condition = "2", series = "30", encoder = "BGRU")
BGRU2 = rbind(BGRU10_2i, BGRU20_2i, BGRU30_2i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(BGRU10_2i, BGRU20_2i, BGRU30_2i)
rm(BGRU10_2, BGRU20_2, BGRU30_2)

CONV10_2i = CONV10_2 %>% cleanitems() %>% mutate(condition = "2", series = "10", encoder = "CONV")
CONV20_2i = CONV20_2 %>% cleanitems() %>% mutate(condition = "2", series = "20", encoder = "CONV")
CONV30_2i = CONV30_2 %>% cleanitems() %>% mutate(condition = "2", series = "30", encoder = "CONV")
CONV2 = rbind(CONV10_2i, CONV20_2i, CONV30_2i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(CONV10_2i, CONV20_2i, CONV30_2i)
rm(CONV10_2, CONV20_2, CONV30_2)

INFS10_2i = INFS10_2 %>% cleanitems() %>% mutate(condition = "2", series = "10", encoder = "INFS")
INFS20_2i = INFS20_2 %>% cleanitems() %>% mutate(condition = "2", series = "20", encoder = "INFS")
INFS30_2i = INFS30_2 %>% cleanitems() %>% mutate(condition = "2", series = "30", encoder = "INFS")
INFS2 = rbind(INFS10_2i, INFS20_2i, INFS30_2i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(INFS10_2i, INFS20_2i, INFS30_2i)
rm(INFS10_2, INFS20_2, INFS30_2)

INNR10_2i = INNR10_2 %>% cleanitems() %>% mutate(condition = "2", series = "10", encoder = "INNR")
INNR20_2i = INNR20_2 %>% cleanitems() %>% mutate(condition = "2", series = "20", encoder = "INNR")
INNR30_2i = INNR30_2 %>% cleanitems() %>% mutate(condition = "2", series = "30", encoder = "INNR")
INNR2 = rbind(INNR10_2i, INNR20_2i, INNR30_2i) %>%
filter(NitemAprem == NitemAhyp) %>% filter(VitemAprem == VitemAhyp)
rm(INNR10_2i, INNR20_2i, INNR30_2i)
rm(INNR10_2, INNR20_2, INNR30_2)

freebies0 = rbind(BGRU0, CONV0, INFS0, INNR0)
write_csv(freebies0, "freebies0")
freebies2 = rbind(BGRU2, CONV2, INFS2, INNR2)
write_csv(freebies2, "freebies2")
