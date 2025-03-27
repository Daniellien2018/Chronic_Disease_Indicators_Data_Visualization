# load libraries
library(readxl)
library(dplyr)
library(tidyr)
library(ggplot2)
library(caret)
library(randomForest)
library(gbm)
library(openxlsx)
library(purrr)

# load cdc chronic diseases dataset into df
df <- read_excel("/Users/Betsy/Desktop/Data Science/Georgia Tech Online Masters in Analytics/CSE 6242 Data and Visual Analytics/Project/Data/U.S._Chronic_Disease_Indicators__CDI___2023_Release copy.xlsx", sheet = 1)

# view first 5 rows
head(df, 5)

# look at column headers -- 34 total
colnames(df)

# filter data to show only rows where 'datavaluetype = number'
# did not include rates/prevalence as these are calculated values and total population/distribution not provided
# then filter by 'stratificationcategory1 = gender' and 'stratificationcategory1 = race/ethnicity'
# did not include 'stratificationcategory1 = overall' since this would double count the number of deaths from ckd and not a specific enough predictor
# filtering by gender and race/ethnicity sets stratification1 to male, female, hispanic, asian, etc.
# by using both gender and race/ethnicity, may be double counting number of deaths as well (something to keep in mind)
# select relevant columns only and rename them (decided to leave out question col)
filtered_df <- df %>%
  filter(DataValueType == 'Number' & 
           (StratificationCategory1 == "Gender" | StratificationCategory1 == "Race/Ethnicity")) %>%
  select(YearStart, LocationDesc, Topic, DataValue, StratificationCategory1, Stratification1) %>%
  rename(
    Year = YearStart,
    State = LocationDesc,
    Disease = Topic,
    Mortality_Count = DataValue
  ) %>%
  mutate(Year = as.numeric(Year)) %>%
  arrange(Year, State) %>%
  mutate(Mortality_Count = as.numeric(Mortality_Count))

# view first 5 rows
head(filtered_df, 5)

# remove rows with na in 'Mortality_Count'
# convert year to int
cdc_df <- filtered_df %>%
  filter(!is.na(Mortality_Count)) %>%
  mutate(Year = as.integer(Year)) %>%
  mutate(Mortality_Count = as.integer(Mortality_Count))

# view the first 5 rows of the cleaned data and last 5 rows
# data from 2010 through 2020
head(cdc_df, 5)
tail(cdc_df, 5)

# load medicaid expenditures into df2
df2 <- read_excel("/Users/Betsy/Desktop/Data Science/Georgia Tech Online Masters in Analytics/CSE 6242 Data and Visual Analytics/Project/Data/MEDICAID_AGGREGATE20.xlsx", sheet = 1)

# view top 5 rows
head(df2, 5)

# select relevant columns only and rename them
# select years in common with cdc df
filtered_df2 <- df2 %>%
  select(State_Name, Y2010, Y2011, Y2012, Y2013, Y2014, Y2015, Y2016, Y2017, Y2018, Y2019, Y2020) %>%
  rename(
    State = State_Name,
    '2010' = Y2010,
    '2011' = Y2011,
    '2012' = Y2012,
    '2013' = Y2013,
    '2014' = Y2014,
    '2015' = Y2015,
    '2016' = Y2016,
    '2017' = Y2017,
    '2018' = Y2018,
    '2019' = Y2019,
    '2020' = Y2020
  )

# remove rows with na
medicaid_df <- filtered_df2 %>%
  drop_na()

# view first 5 rows
head(medicaid_df, 5)

# reshape medicaid df to long format and group by state then sum all medicaid expenses (expenses broken down by personal, hospital, dental, etc.)
medicaid_df <- medicaid_df %>%
  pivot_longer(cols = starts_with("20"), names_to = "Year", values_to = "Expenses") %>%
  group_by(State, Year) %>%
  summarise(Medicaid_Expenses = sum(Expenses), .groups = 'drop') %>%
  mutate(Year = as.integer(Year))

# view first 5 rows
head(medicaid_df, 5)

# combine cdc and medicaid dfs by state and year
combined_df <- medicaid_df %>%
  left_join(cdc_df, by = c("State", "Year"))

# view first 5 rows
head(combined_df, 5)

# load median income df
df3 <- read_excel("/Users/Betsy/Desktop/Data Science/Georgia Tech Online Masters in Analytics/CSE 6242 Data and Visual Analytics/Project/Data/Table H-8. Median Household Income by State- 1984 to 2023.xlsx", sheet = 1)

# view first 5 rows
head(df3, 5)

# select columns with data from 2010 through 2020
# drop u.s. and d.c.
filtered_df3 <- df3 %>%
  select(State, '2010 (37)', '2011', '2012', '2013 (39)', '2014', '2015', '2016', '2017 (40)', '2018', '2019', '2020 (41)') %>%
  rename(
    '2010' = '2010 (37)',
    '2013' = '2013 (39)',
    '2017' = '2017 (40)',
    '2020' = '2020 (41)'
  ) %>%
  filter((State != 'United States') & (State != 'District of Columbia'))

# view first 5 rows
head(filtered_df3, 5)

# reshape filtered_df3 from wide to long format using pivot_longer
long_filtered_df3 <- filtered_df3 %>%
  pivot_longer(cols = `2010`:`2020`, names_to = "Year", values_to = "Median_Income") %>%
  mutate(Year = as.integer(Year))

# left join on state and year
final_df <- combined_df %>%
  left_join(long_filtered_df3, by = c("State", "Year"))

# remove rows with na
final_df <- final_df %>%
  drop_na()

# view first 5 rows
head(final_df, 5)

# exploratory data analysis
# summary stats for numeric columns
summary(Filter(is.numeric, final_df))

# average of Mortality_Count by race and gender
final_df %>%
  group_by(Stratification1) %>%
  summarise(average = mean(Mortality_Count, na.rm = TRUE))

# summary stats by state
final_df %>%
  group_by(State) %>%
  summarise(across(c(Medicaid_Expenses, Mortality_Count, Median_Income), list(mean = mean, median = median)))

# medicaid expenses frequency distribution
ggplot(final_df, aes(x = Medicaid_Expenses)) +
  geom_histogram(binwidth = 10000, fill = "cadetblue", color = "black") +
  labs(title = "Histogram of Medicaid Expenses", x = "Medicaid Expenses (in millions)", y = "Frequency")

# median income frequency distribution
ggplot(final_df, aes(x = Median_Income)) +
  geom_histogram(binwidth = 1000, fill = "cadetblue3", color = "black") +
  labs(title = "Histogram of Median Income", x = "Median Income (in thousands)", y = "Frequency")

# filter to gender
gender <- final_df %>%
  filter(StratificationCategory1 == 'Gender')

# filter to race/ethnicity
race <- final_df %>%
  filter(StratificationCategory1 == 'Race/Ethnicity')

# mortality count by gender
ggplot(gender, aes(x = Stratification1, y = Mortality_Count)) +
  geom_boxplot(fill = "orange") +
  labs(title = "Boxplot by Gender", x = "Gender", y = "Mortality Count")

# mortality count by race/ethnicity
ggplot(race, aes(x = Stratification1, y = Mortality_Count)) +
  geom_boxplot(fill = "orange") +
  labs(title = "Boxplot by Race/Ethnicity", x = "Race/Ethnicity", y = "Mortality Count")

# scatterplot showing mortality count against median income
ggplot(final_df, aes(x = Median_Income, y = Mortality_Count)) +
  geom_point(color = "red") +
  labs(title = "Scatter Plot for Mortality Count vs. Median Income", x = "Median Income (in thousands)", y = "Mortality Count")

# scatterplot showing mortality count against medicaid expenses
ggplot(final_df, aes(x = Medicaid_Expenses, y = Mortality_Count)) +
  geom_point(color = "red") +
  labs(title = "Scatter Plot for Mortality Count vs. Medicaid Expenses", x = "Medicaid Expenses (in millions)", y = "Mortality Count")

# correlation analysis
cor_matrix <- final_df %>%
  select(where(is.numeric)) %>%
  cor(use = "complete.obs")

corrplot::corrplot(cor_matrix, method = "circle")

# only factor categorical columns used in modeling
modified_df <- final_df %>%
  mutate(across(c(State, Stratification1), as.factor))

# view first 5 rows
head(modified_df, 5)

# split data into training and testing sets
# training data uses data from 2010 - 2017 and testing data uses data from 2018 - 2020
set.seed(123)
train_df <- modified_df %>% filter(Year >= 2010 & Year <= 2017)
test_df <- modified_df %>% filter(Year >= 2018 & Year <= 2020)

# train models
# multiple linear regression
lm_model <- lm(Mortality_Count ~ State + Year + Stratification1 + Medicaid_Expenses + Median_Income, data = train_df)

# random forest regression
rf_model <- randomForest(Mortality_Count ~ State + Year + Stratification1 + Medicaid_Expenses + Median_Income, data = train_df, ntree = 100)

# gradient boosting regression
gbm_model <- gbm(Mortality_Count ~ State + Year + Stratification1 + Medicaid_Expenses + Median_Income, data = train_df, distribution = "gaussian", n.trees = 100, interaction.depth = 3, shrinkage = 0.01, cv.folds = 5)

# predictions
test_df$lm_pred <- predict(lm_model, test_df)
test_df$rf_pred <- predict(rf_model, test_df)
test_df$gbm_pred <- predict(gbm_model, test_df, n.trees = 100)

# evaluate models
# calculate mae
mae <- function(actual, predicted) {
  mean(abs(actual - predicted))
}

# calculate mse
mse <- function(actual, predicted) {
  mean((actual - predicted)^2)
}

# calculate rmse
rmse <- function(actual, predicted) {
  sqrt(mean((actual - predicted)^2))
}

# calculate r-squared
r_squared <- function(actual, predicted) {
  ss_total <- sum((actual - mean(actual))^2)
  ss_residual <- sum((actual - predicted)^2)
  1 - (ss_residual / ss_total)
}

# metrics for multiple linear regression model
lm_mae <- mae(test_df$Mortality_Count, test_df$lm_pred)
lm_mse <- mse(test_df$Mortality_Count, test_df$lm_pred)
lm_rmse <- rmse(test_df$Mortality_Count, test_df$lm_pred)
lm_r2 <- r_squared(test_df$Mortality_Count, test_df$lm_pred)

# metrics for random forest model
rf_mae <- mae(test_df$Mortality_Count, test_df$rf_pred)
rf_mse <- mse(test_df$Mortality_Count, test_df$rf_pred)
rf_rmse <- rmse(test_df$Mortality_Count, test_df$rf_pred)
rf_r2 <- r_squared(test_df$Mortality_Count, test_df$rf_pred)

# metric for gradient boosting
gbm_mae <- mae(test_df$Mortality_Count, test_df$gbm_pred)
gbm_mse <- mse(test_df$Mortality_Count, test_df$gbm_pred)
gbm_rmse <- rmse(test_df$Mortality_Count, test_df$gbm_pred)
gbm_r2 <- r_squared(test_df$Mortality_Count, test_df$gbm_pred)

# results
cat("Multiple Linear Regression Metrics:")
cat("MAE:", lm_mae) # 899.1009
cat("MSE:", lm_mse) # 1884827
cat("RMSE:", lm_rmse) # 1372.89
cat("R-squared:", lm_r2) # 0.67858

cat("Random Forest Metrics:")
cat("MAE:", rf_mae) # 598.3433
cat("MSE:", rf_mse) # 1032967
cat("RMSE:", rf_rmse) # 1016.35
cat("R-squared:", rf_r2) # 0.8238479

cat("Gradient Boosting Metrics:")
cat("MAE:", gbm_mae) # 1064.362
cat("MSE:", gbm_mse) # 2165246
cat("RMSE:", gbm_rmse) # 1471.478
cat("R-squared:", gbm_r2) # 0.63076

# view first 5 rows for actuals vs. predictions
head(test_df[, c("Mortality_Count", "rf_pred")], 5)

# generate predictions on testing dataset using the random forest model
test_df$rf_pred <- predict(rf_model, test_df)

# generate predictions from 2021 - 2025
years <- 2021:2050

# define unique values for state and stratification1
states <- unique(train_df$State)
stratification_values <- unique(train_df$Stratification1)

# create new df to make predictions
new_data <- expand.grid(
  State = states,
  Year = years,
  Stratification1 = stratification_values
) %>%
  mutate(
    Medicaid_Expenses = mean(train_df$Medicaid_Expenses),
    Median_Income = mean(train_df$Median_Income)
  )

# view first 5 rows
head(new_data, 5)

# note that this is a poor dataset since medicaid expenses and median income are constant across state, year, and stratifiation1
# generate predictions for the new dataset
new_data$rf_pred <- predict(rf_model, new_data)

# view the predictions
head(new_data)

# save predictions onto excel (optional)
# write.xlsx(
#   new_data,
#   file = "predictions_2021_2050_with_state_1.xlsx",
#   sheetName = "Predictions",
#   rowNames = FALSE
# )

# since predictions are constant (generated dataset not capturing variability in medicaid expenses and median income) -- fine tune dataset
# fit linear models to make predictions for medicaid expenses by state
medicaid_trends <- train_df %>%
  group_by(State) %>%
  do(model = lm(Medicaid_Expenses ~ Year, data = .)) %>%
  ungroup()

# fit linear models to make predictions for median income by state
income_trends <- train_df %>%
  group_by(State) %>%
  do(model = lm(Median_Income ~ Year, data = .)) %>%
  ungroup()

# predict future medicaid expenses and median income and combine datasets
new_data <- new_data %>%
  left_join(medicaid_trends, by = "State") %>%
  rowwise() %>%
  mutate(Medicaid_Expenses = predict(model, newdata = data.frame(Year = Year))) %>%
  ungroup() %>%
  select(-model) %>%
  left_join(income_trends, by = "State") %>%
  rowwise() %>%
  mutate(Median_Income = predict(model, newdata = data.frame(Year = Year))) %>%
  ungroup() %>%
  select(-model)

# make predictions with new dataset
new_data$rf_pred <- predict(rf_model, new_data)

# view first 5 rows
head(new_data)

# write predictions to excel file to be used for interactive dashboard on tableau
write.xlsx(
  new_data,
  file = "predictions_2021_2050_with_state_2.xlsx",
  sheetName = "Predictions",
  rowNames = FALSE
)
