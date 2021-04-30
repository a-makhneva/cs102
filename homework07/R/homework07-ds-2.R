# Set working directory
setwd("C:/Users/79111/Documents/R")

df <- read.csv("howpop_train.csv", encoding="UTF-8")

head(df)

df <- df[,!grepl("_lognorm$", names(df))]

sapply(df, function(x) sum(is.na(x)))

df$published = as.POSIXct(df$published, format = "%Y-%m-%d %H:%M:%S", tz = "GMT")

summary(df)

df$year <- as.numeric(format(df$published, '%Y'))
df$month <- as.numeric(format(df$published, '%m'))
df$weekday <- as.numeric(format(df$published, '%u'))
df$day <- as.numeric(format(df$published, '%d'))
df$hour <- as.numeric(format(df$published, '%H'))

# 1. В каком месяце (и какого года) было больше всего публикаций?
# март 2016
# март 2015
# апрель 2015
# апрель 2016

march_15 <- subset(df, df$month == 3 & df$year == 2015)
march_16 <- subset(df, df$month == 3 & df$year == 2016)
april_15 <- subset(df, df$month == 4 & df$year == 2015)
april_16 <- subset(df, df$month == 4 & df$year == 2016)

m <- rbind(c(nrow(march_15), nrow(april_15)), c(nrow(march_16), nrow(april_16)))
colnames(m) <- c("March", "April")
rownames(m) <- c(2015, 2016)

barplot(m, main = 'Publications in March, April of 2015, 2016', ylab = "Publications",
        ylim = c(1500, 2200), xpd = F,
        col = c("lightblue", "mistyrose"),
        legend = T, beside = T)

# 2. Проанализируйте публикации в месяце из предыдущего вопроса

# Выберите один или несколько вариантов:

#  * Один или несколько дней сильно выделяются из общей картины (да)

barplot(table(march_15$day), main = 'Daily publications (March 2015)',
        ylab = 'Publications', xlab = 'Day',
        col = "lavender",
        legend = F, beside = T)

#  * На хабре всегда больше статей, чем на гиктаймсе (нет)

barplot(table(march_15$domain, march_15$day), main = 'Daily publications by domain (March 2015)',
        ylab = 'Publications', xlab = 'Day',
        col = c("wheat", "lightcyan"),
        legend = T, beside = T)

#  * По субботам на гиктаймс и на хабрахабр публикуют примерно одинаковое число статей (да)

table(subset(march_15, march_15$weekday == 6)$domain)

# 3. Когда лучше всего публиковать статью?

#  * Больше всего просмотров набирают статьи, опубликованные в 12 часов дня (нет)
#  * Больше всего просмотров набирают статьи, опубликованные в 6 часов утра (да)

library(dplyr)

by_hour <- df %>% group_by(hour)

views_comms <- by_hour %>% summarise(
  aver_views = mean(views),
  aver_comms = mean(comments)
)

barplot(views_comms$aver_views ~ views_comms$hour, main = 'Average views by publication time',
        ylab = 'Views', xlab = 'Hour',
        ylim = c(14000, 21000), xpd = F, col = "sienna3",
        legend = F, beside = T)

#  * У опубликованных в 10 утра постов больше всего комментариев (нет)

barplot(views_comms$aver_comms ~ views_comms$hour, main = 'Average comments by publication time',
        ylab = 'Comments', xlab = 'Hour',
        ylim = c(30, 55), xpd = F, col = "salmon",
        legend = F, beside = T)

#  * Максимальное число комментариев на гиктаймсе набрала статья, опубликованная в 9 часов вечера (нет)

geek <- by_hour %>% filter(domain == 'geektimes.ru')
geek$published[which(geek$comments == max(geek$comments))]

#  * На хабре дневные статьи комментируют чаще, чем вечерние (нет)

habr <- by_hour %>% filter(domain == 'habrahabr.ru')

habr_comms <- by_hour %>% summarise(
  aver_comms = mean(comments)
)

plot(habr_comms$aver_comms ~ habr_comms$hour, type = 'l', main = 'Average comments on habrahabr.ru by publication time',
     ylab = 'Comments', xlab = 'Hour', col = 2)


# 4. Кого из топ авторов чаще всего минусуют?

# @Mordatyj
# @Mithgol
# @alizar
# @ilya42

by_author <- df %>% group_by(author)

top_4 <- by_author %>% filter(author %in% c('@Mordatyj', '@Mithgol', '@alizar', '@ilya42'))

na.exclude(top_4) %>% summarise(
  average_minus = mean(votes_minus)
)


# 5. Сравните субботы и понедельники

# Правда ли, что по субботам авторы пишут в основном днём, а по
# понедельникам — в основном вечером? (нет)

mon_sat <- by_hour %>% filter(weekday %in% c(1, 6))

barplot(table(mon_sat$weekday, mon_sat$hour), main = 'Monday vs Saturday publications by hour',
        ylab = 'Publications', xlab = 'Hour',
        col = c(10, 29),
        legend = c('Mon', 'Sat'), beside = T)
