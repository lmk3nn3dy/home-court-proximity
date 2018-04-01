library(ggplot2)
library(glmnet)

df <- read.csv('home_advantage.csv')

# find mean_advantage
mean_advantage <- mean(df$kilometer_advantage)

# reshape data and convert to miles
exp2 <- data.frame(mi_adv=c(df$kilometer_advantage/1.60934, -df$kilometer_advantage/1.60934))
exp2$result <- c(rep(1, 330), rep(0, 330))  # first half are wins, second are losses

# plot with logistic curve
ggplot(exp2,aes(mi_adv,result)) + geom_jitter(height=.03, alpha=.3, color='deeppink4') + 
  geom_smooth(method = "glm", color= 'darkcyan',   
              method.args = list(family = "binomial"), se = FALSE) +
  labs(title='Win-Likelihood as a Function of Proximity', 
       x='Advantage Against Opposing Team (mi)',
       y='Result')

