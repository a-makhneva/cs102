# Set working directory
setwd("C:/Users/79111/Documents/R")

# Read the date into a dataframe called adult
adult <- read.csv("adult_data.csv", header=T)

# What type of object is adult?
class(adult)

# List the names of the variables in the dataframe
names(adult)

# What is the shape of adult
dim(adult)

# Print the data frame
head(adult)

# Print the number of NA among adult
sapply(adult, function(x) sum(is.na(x)))

# Objects structure
str(adult)

# Print descriptive statistics
summary(adult)

# Print the number of men and women
table(adult$sex)

# What is the mean age of women?
mean(subset(adult, sex == "Female")$age)

# What is the share of Germans?
sum(adult$native.country == "Germany") / nrow(adult)

# What is the mean and standard deviation of age for rich and poor people?

rich <- subset(adult, salary == ">50K")
poor <- subset(adult, salary == "<=50K")
mean(rich$age)
sd(rich$age)
mean(poor$age)
sd(poor$age)

# Is it true that rich people have high education only: Assoc-acdm, Assoc-voc,
# Bachelors, Doctorate, Masters or Prof-school?

table(rich$education)

# Get age stats for all races by sex. What's the max age among Amer-Indian-Eskimo men?

for(i in unique(adult$race)) {
  print(i)
  for(j in unique(adult$sex)) {
    print(j)
    print(summary(subset(adult, race == i & sex == j)$age))
  }
}

max(subset(adult, race == "Amer-Indian-Eskimo" & sex == "Male")$age)

# Which share of rich people (>50K) is greater: among married or bachelor men
# (marital.status)? Married are men whose marital.status begins with "Married"
# (Married-civ-spouse, Married-spouse-absent or Married-AF-spouse). All the
# others are considered bachelors.

married_men <- subset(adult, sex == "Male" & (substr(marital.status, 1, 7) == "Married"))
sum(married_men$salary == ">50K") / nrow(married_men)
bachelor_men <- subset(adult, sex == "Male" & (substr(marital.status, 1, 7) != "Married"))
sum(bachelor_men$salary == ">50K") / nrow(bachelor_men)

# What is the maximum of hours per week? How many people work that much? What is
# the percentage of rich (>50K) among them?

max(adult$hours.per.week)
workaholic <- subset(adult, hours.per.week == max(adult$hours.per.week))
nrow(workaholic)
sum(workaholic$salary == ">50K") / nrow(workaholic) * 100

# What is the mean hours.per.week for poor (<=50K) and rich (>50K) people of
# each native.country?

for(i in unique(adult$native.country)) {
  print(i)
  print(mean(subset(poor, native.country == i)$hours.per.week))
  print(mean(subset(rich, native.country == i)$hours.per.week))
}
