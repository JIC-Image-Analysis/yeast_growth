library(ggplot2)
library(reshape2)
data <- read.csv('output/aggregated.csv')
dmelt <- melt(data, id='dist')
ggplot(dmelt, aes(x=dist, y=value, colour=variable)) + geom_line()
ggsave('all_genotypes.png')
