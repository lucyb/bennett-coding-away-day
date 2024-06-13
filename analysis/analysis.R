library(tidyverse)
library(ggplot2)

dat <- read_csv("output/dataset.csv.gz")

pc_ferret_bites <- sum(dat$ferret_bites) / sum(dat$bites)*100
pc_non_ferret_bites <- 100 - pc_ferret_bites

plot_dat <- tibble(nom = c(pc_ferret_bites, pc_non_ferret_bites), id  = c("catsnake_nom", "other_nom"))

ggplot(dat = plot_dat,
       aes(x = "", y = c(pc_ferret_bites, pc_non_ferret_bites), fill = id)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  theme_void()
