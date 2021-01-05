rm(list=ls())
library(tidyverse)
library(rmarkdown)
library(ggplot2)
library(knitr)
library(entropy)
library(kableExtra)
library(gridExtra)
library(grid)
library(lattice)

setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step0")
BGRU0 = read_csv("BGRU0")
CONV0 = read_csv("CONV0")
INFS0 = read_csv("INFS0")
INNR0 = read_csv("INNR0") %>% mutate(encoder = "SATT")
WUGS0 = rbind(BGRU0, CONV0, INFS0, INNR0)
rm(BGRU0, CONV0, INFS0, INNR0)
setwd("~/U3/compositionality-code/Code/Variability/results/paired_outputs/step2")
BGRU2 = read_csv("BGRU2") 
CONV2 = read_csv("CONV2")
INFS2 = read_csv("INFS2") 
INNR2 = read_csv("INNR2") %>% mutate(encoder = "SATT")
WUGS2 = rbind(BGRU2, CONV2, INFS2, INNR2)
rm(BGRU2, CONV2, INFS2, INNR2)

relations0 = WUGS0 %>%
  mutate(condition=replace(condition, condition == "0", "small")) %>%
  group_by(condition, encoder, `in`, out, diff, Acorrect, Bcorrect, VblockAhyp) %>% 
  summarize(blockmean = mean(BScore)) %>% 
  summarize(mean = mean(blockmean)*100, sd = sd(blockmean)*100)
relations2 = WUGS2 %>%
  mutate(condition=replace(condition, condition == "2", "large")) %>%
  group_by(condition, encoder, `in`, out, diff, Acorrect, Bcorrect, VblockAhyp) %>% 
  summarize(blockmean = mean(BScore)) %>% 
  summarize(mean = mean(blockmean)*100, sd = sd(blockmean)*100) 
relations = rbind(relations0, relations2)

relations$condition <- factor(relations$condition, levels = c("small", "large"))

meanplots = ggplot(data = relations) + 
  geom_violin(aes(x = condition, y = mean))+ 
  geom_point(aes(x = condition, y = mean), size =.35) + facet_grid(cols = vars(encoder)) + xlab("")
sdplots = ggplot(data = relations) +
  geom_violin(aes(x = condition, y = sd)) + 
  geom_point(aes(x = condition, y = sd), size =.35) + facet_grid(cols = vars(encoder))+ xlab("")
grid.arrange(meanplots, sdplots, bottom = "all transformations")

neg_meanplots = ggplot(data = (relations%>%filter(`in` == 'not' | out == 'not'))) + 
  geom_violin(aes(x = condition, y = mean))+ 
  geom_point(aes(x = condition, y = mean), size =.35) + facet_grid(cols = vars(encoder)) + xlab("")
neg_sdplots = ggplot(data = (relations%>%filter(`in` == 'not' | out == 'not'))) + 
  geom_violin(aes(x = condition, y = sd)) + 
  geom_point(aes(x = condition, y = sd), size =.35) + facet_grid(cols = vars(encoder))+ xlab("")
grid.arrange(neg_meanplots, neg_sdplots, bottom = "inserting or deleting negation")

qants_meanplots = ggplot(data = (relations%>%filter(`in` == 'all' | out == 'all'))) + 
  geom_violin(aes(x = condition, y = mean))+ 
  geom_point(aes(x = condition, y = mean), size =.35) + facet_grid(cols = vars(encoder)) + xlab("")
qants_sdplots = ggplot(data = (relations%>%filter(`in` == 'all' | out == 'all'))) + 
  geom_violin(aes(x = condition, y = sd)) + 
  geom_point(aes(x = condition, y = sd), size =.35) + facet_grid(cols = vars(encoder))+ xlab("")
grid.arrange(qants_meanplots, qants_sdplots, bottom = "inserting or deleting all")


red_meanplots = ggplot(data = (relations%>%filter(`in` == 'red' | out == 'red'))) + 
  geom_violin(aes(x = condition, y = mean))+ 
  geom_point(aes(x = condition, y = mean), size =.35) + facet_grid(cols = vars(encoder)) + xlab("")
red_sdplots = ggplot(data = (relations%>%filter(`in` == 'red' | out == 'red'))) + 
  geom_violin(aes(x = condition, y = sd)) + 
  geom_point(aes(x = condition, y = sd), size =.35) + facet_grid(cols = vars(encoder))+ xlab("")
grid.arrange(red_meanplots, red_sdplots, bottom = "inserting or deleting 'red'")

