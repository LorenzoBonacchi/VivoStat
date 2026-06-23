
# =========================
# LIBRERIE
# =========================

library(tidyverse)
library(lme4)
library(lmerTest)
library(emmeans)

data <- read.delim("test_data.csv",sep = ",",header = FALSE)
colnames(data) <- as.character(data[1, ])
data <- data[-1, ]
colnames(data) <- c("Time", as.character(data[1, -1]))
data <- data[-1, ]
long <- data %>%
  pivot_longer(
    cols = -Time,
    names_to = "mouse",
    values_to = "value"
  )

long <- long %>%
  mutate(
    trattamento = ifelse(grepl("^VEH", mouse),
                         "Vehicle",
                         "CRE"),
    sesso = ifelse(grepl("F", mouse),
                   "Female",
                   "Male"),    
    genotipo = ifelse(grepl("\\+", mouse),
                      "Plus",
                      "Minus"),
    topo_id = mouse,
    tempo = Time,
    value = as.numeric(value)
  )

# =========================
# Factors
# =========================
long$trattamento <- factor(long$trattamento)
long$sesso <- factor(long$sesso)
long$genotipo <- factor(long$genotipo)
long$tempo <- factor(long$tempo,
                     levels = c("BL","0.5","1","2","4","6"))
long$topo_id <- factor(long$topo_id)

# =========================
# MIXED MODEL
# =========================

model <- lmer(value ~ trattamento * tempo * genotipo +
                sesso +
                (1 | topo_id),
              data = long)
anova(model)
anova_df = as.data.frame(anova(model))
write.csv(anova_df, "anova_mixed_model.csv", row.names = TRUE)

emmeans(model, pairwise ~ trattamento | genotipo) #post-hoc test

ggplot(long,
       aes(x = tempo,
           y = value,
           color = trattamento,
           group = trattamento)) +  
  stat_summary(fun = mean,
               geom = "line",
               linewidth = 1) +
  stat_summary(fun = mean,
               geom = "point",
               size = 3) +
  facet_wrap(~ genotipo) +
  theme_classic() +
  labs(
    x = "Tempo",
    y = "Value",
    color = "Treatment"
  )

emmeans(model, pairwise ~ trattamento | tempo * genotipo)
emm <- emmeans(model,
               pairwise ~ trattamento | tempo * genotipo)

contr_clean <- as.data.frame(emm$contrasts)

contr_clean$tempo <- rep(c("BL","0.5","1","2","4","6"), times = 2)
contr_clean$genotipo <- rep(c("Minus","Plus"), each = 6)

#write.csv(contr_clean, file = "contrasti_emmeans.csv", row.names = FALSE)


model <- lmer(value ~ trattamento * tempo * genotipo * sesso +
                (1 | topo_id),
              data = long)

anova(model)
anova_df = as.data.frame(anova(model))
write.csv(anova_df, "anova_mixed_model.csv", row.names = TRUE)

emmeans(model, pairwise ~ trattamento | tempo * sesso)
emmeans(model, pairwise ~ trattamento | tempo * genotipo * sesso)
emmeans(model, pairwise ~ trattamento | tempo * genotipo * sesso)
emm <- emmeans(model,
               pairwise ~ trattamento | tempo * genotipo * sesso)

contr_clean <- as.data.frame(emm$contrasts)

#write.csv(contr_clean, file = "contrasti_emmeans_full.csv", row.names = FALSE)