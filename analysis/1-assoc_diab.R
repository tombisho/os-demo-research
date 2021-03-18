## import libraries

library('tidyverse')

## import data
df_input <- read_csv(
  here::here("output", "cohorts", "input_2_diab.csv"),
  col_types = cols(
    patient_id = col_integer(),
    has_diab = col_integer(),
    bmi = col_number(),
    bmi_date_measured = col_date("%Y-%m"),
    sex = col_factor(),
    age = col_integer()
  )
)

my_mod = summary(lm(formula = has_diab ~ bmi, data = df_input))
  

#write_csv(x = as.data.frame(my_mod$coefficients), file = here::here("output", "models", "diab-model.csv"))
write.csv(x = as.data.frame(my_mod$coefficients), file = here::here("output", "models", "diab-model.csv"))
