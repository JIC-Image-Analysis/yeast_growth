library(ggplot2)
data <- read.table('output/pline.txt', header=T, sep=',')
ggplot(data=data, aes(x=position, y=intensity)) + geom_line()
ggsave('line-plot.png')
