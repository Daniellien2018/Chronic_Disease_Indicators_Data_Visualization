install.packages("cli")

# Load libraries
library(readxl)
library(dplyr)
library(tidyr)
library(ggplot2)
library(caret)
library(randomForest)
library(gbm)
library(openxlsx)
library(purrr)

# Load CDC chronic diseases dataset into df
df = chronic_disease[chronic_disease$Topic == "Cancer", ]

# View first 5 rows
head(df, 5)

# Look at column headers
colnames(df)

# Check if any cancer data exists
cancer_check <- df %>%
  filter(Topic == 'Cancer') %>%
  count()
print(paste("Number of cancer records:", cancer_check$n))

# Check what DataValueType values exist for cancer records
cancer_value_types <- df %>%
  filter(Topic == 'Cancer') %>%
  count(DataValueType)
print("DataValueType values for cancer records:")
print(cancer_value_types)

# Check what StratificationCategory1 values exist for cancer records
cancer_strat_cats <- df %>%
  filter(Topic == 'Cancer') %>%
  count(StratificationCategory1)
print("StratificationCategory1 values for cancer records:")
print(cancer_strat_cats)

# Filter data to show only rows where 'DataValueType = number'
# Filter by Topic = Cancer
# Include Question column which contains the type of cancer
# Filter by 'StratificationCategory1 = gender' and 'StratificationCategory1 = Race/Ethnicity'
filtered_df <- df %>%
  filter(StratificationCategory1 == "Gender" | StratificationCategory1 == "Race/Ethnicity") %>%
  select(YearStart, LocationDesc, Topic, Question, DataValue, StratificationCategory1, Stratification1) %>%
  rename(
    Year = YearStart,
    State = LocationDesc,
    Disease = Topic,
    Type = Question,
    Number_Diagnosed = DataValue
  ) %>%
  mutate(Year = as.numeric(Year)) %>%
  arrange(Year, State) %>%
  mutate(Number_Diagnosed = as.numeric(Number_Diagnosed))

# View first 5 rows
head(filtered_df, 5)

# Remove rows with na in 'number_diagnosed'
# Convert year to int
cdc_df <- filtered_df %>%
  filter(!is.na(Number_Diagnosed)) %>%
  mutate(Year = as.integer(Year)) %>%
  mutate(Number_Diagnosed = as.integer(Number_Diagnosed))

# View the first 5 rows of the cleaned data and last 5 rows
head(cdc_df, 5)
tail(cdc_df, 5)

# Load Medicaid expenditures into df2
df2 <- MEDICAID_AGGREGATE20

# View first 5 rows
head(df2, 5)

# Select relevant columns only and rename them
# Select years in common with cdc_df
filtered_df2 <- df2 %>%
  select(State_Name, Y2008, Y2009, Y2010, Y2011, Y2012, Y2013, Y2014, Y2015, Y2016, Y2017, Y2018, Y2019, Y2020) %>%
  rename(
    State = State_Name,
    '2008'= Y2008,
    '2009' =Y2009,
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

# Remove rows with na
medicaid_df <- filtered_df2 %>%
  drop_na()

# View first 5 rows
head(medicaid_df, 5)

# Reshape medicaid_df to long format and group by state then sum all medicaid expenses
medicaid_df <- medicaid_df %>%
  pivot_longer(cols = starts_with("20"), names_to = "Year", values_to = "Expenses") %>%
  group_by(State, Year) %>%
  summarise(Medicaid_Expenses = sum(Expenses), .groups = 'drop') %>%
  mutate(Year = as.integer(Year))

# View first 5 rows
head(medicaid_df, 5)

# Combine cdc and medicaid dfs by state and year
combined_df <- medicaid_df %>%
  left_join(cdc_df, by = c("State", "Year"))

# View first 5 rows
head(combined_df, 5)

# STOP HERE

# Load median income df
df3 <- read.csv("state_median_income.csv", header = TRUE)

# View first 5 rows
head(df3, 5)

# Delete second row
df3 <- df3[-2, ]

# Set the column names to the first row
colnames(df3) <- as.character(unlist(df3[1, ]))

# Remove the first row (which is now the header)
df3 <- df3[-1, ]

# Select columns with data from 2010 through 2020
# Drop u.s. and d.c.
filtered_df3 <- df3 %>%
  select(State, '2008', '2009 (36)', '2010 (37)', '2011', '2012', '2013 (39)', '2014', '2015', '2016', '2017 (40)', '2018', '2019', '2020 (41)') %>%
  rename(
    '2009' = '2009 (36)',
    '2010' = '2010 (37)',
    '2013' = '2013 (39)',
    '2017' = '2017 (40)',
    '2020' = '2020 (41)'
  ) %>%
  filter((State != 'United States') & (State != 'District of Columbia'))

# View first 5 rows
head(filtered_df3, 5)

# Reshape filtered_df3 from wide to long format using pivot_longer
long_filtered_df3 <- filtered_df3 %>%
  pivot_longer(cols = `2008`:`2020`, names_to = "Year", values_to = "Median_Income") %>%
  mutate(Year = as.integer(Year))

# Left join on state and year
final_df <- combined_df %>%
  left_join(long_filtered_df3, by = c("State", "Year"))

# Remove rows with na
final_df <- final_df %>%
  drop_na()

# View first 5 rows
head(final_df, 5)

# exploratory data analysis
# summary stats for numeric columns
summary(Filter(is.numeric, final_df))

# average of number_diagnosed by cancer type
final_df %>%
  group_by(Type) %>%
  summarise(average = mean(Number_Diagnosed, na.rm = TRUE))

# average of number_diagnosed by race and gender
final_df %>%
  group_by(Stratification1) %>%
  summarise(average = mean(Number_Diagnosed, na.rm = TRUE))

# HERE final

# Clean median_Income and convert to numeric
final_df <- final_df %>%
  mutate(Median_Income = as.numeric(gsub(",", "", Median_Income)))

final_df %>%
  group_by(State) %>%
  summarise(across(c(Medicaid_Expenses, Number_Diagnosed, Median_Income), 
                   list(mean = mean, median = median)))

# summary stats by state
final_df %>%
  group_by(State) %>%
  summarise(across(c(Medicaid_Expenses, Number_Diagnosed, Median_Income), list(mean = mean, median = median)))

# medicaid expenses frequency distribution
ggplot(final_df, aes(x = Medicaid_Expenses)) +
  geom_histogram(binwidth = 10000, fill = "cadetblue", color = "black") +
  labs(title = "Histogram of Medicaid Expenses", x = "Medicaid Expenses (in millions)", y = "Frequency")

# median income frequency distribution-- doesn't work
ggplot(final_df, aes(x = Median_Income)) +
  geom_histogram(binwidth = 1000, fill = "cadetblue3", color = "black") +
  labs(title = "Histogram of Median Income", x = "Median Income (in thousands)", y = "Frequency")

# Plot distribution by cancer type
ggplot(final_df, aes(x = Type, y = Number_Diagnosed)) +
  geom_boxplot(fill = "skyblue") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Number Diagnosed by Cancer Type", x = "Cancer Type", y = "Number Diagnosed")

# filter to gender
gender <- final_df %>%
  filter(StratificationCategory1 == 'Gender')

# filter to race/ethnicity
race <- final_df %>%
  filter(StratificationCategory1 == 'Race/Ethnicity')

# number diagnosed by gender
ggplot(gender, aes(x = Stratification1, y = Number_Diagnosed)) +
  geom_boxplot(fill = "orange") +
  facet_wrap(~Type, scales = "free_y") +
  labs(title = "Number Diagnosed by Gender and Cancer Type", x = "Gender", y = "Number Diagnosed")

# number diagnosed by race/ethnicity
ggplot(race, aes(x = Stratification1, y = Number_Diagnosed)) +
  geom_boxplot(fill = "orange") +
  facet_wrap(~Type, scales = "free_y") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Number Diagnosed by Race/Ethnicity and Cancer Type", x = "Race/Ethnicity", y = "Number Diagnosed")

# correlation analysis
cor_matrix <- final_df %>%
  select(where(is.numeric)) %>%
  cor(use = "pairwise.complete.obs")

corrplot::corrplot(cor_matrix, method = "circle")

# only factor categorical columns used in modeling
modified_df <- final_df %>%
  mutate(across(c(State, Stratification1, Type), as.factor))

# view first 5 rows
head(modified_df, 5)

# split data into training and testing sets
# training data uses data from 2010 - 2017 and testing data uses data from 2018 - 2020
set.seed(123)
train_df <- modified_df %>% filter(Year >= 2008 & Year <= 2017)
test_df <- modified_df %>% filter(Year >= 2018 & Year <= 2020)

# Want to make the model predict type of cancer 

# Preprocessing
train_df <- train_df %>%
  mutate(
    State = as.factor(State),
    Year = as.factor(Year),
    Stratification1 = as.factor(Stratification1),
    Type = as.factor(Type),
    Medicaid_Expenses = as.numeric(Medicaid_Expenses),
    Median_Income = as.numeric(Median_Income)
  )

train_df_clean <- train_df %>%
  filter(
    !is.na(Number_Diagnosed),
    !is.na(State),
    !is.na(Year),
    !is.na(Stratification1),
    !is.na(Medicaid_Expenses),
    !is.na(Median_Income)
  )

# 1. REGRESSION: Predict Number_Diagnosed
rf_reg_model <- randomForest(Number_Diagnosed ~ State + Stratification1 + Medicaid_Expenses + Median_Income,
                             data = train_df_clean, ntree = 100)

print(rf_reg_model)

# 2. CLASSIFICATION: Predict Type
unique(train_df_clean$Type)
rf_class_model <- randomForest(Type ~ State + Stratification1 + Medicaid_Expenses + Median_Income,
                               data = train_df_clean, ntree = 100)

print(rf_class_model)

# STOP

summary(train_df_clean$Number_Diagnosed)  # Should not be all NA
print(rf_reg_model)  # Check if % Var explained is reasonable

table(train_df_clean$Type)  # Ensure no empty categories
print(rf_class_model)  # Check OOB error rate

# STOP HERE

# 3. PREDICTIONS ON TEST SET
# Make sure test data has the same format as training data
test_df <- test_df %>%
  mutate(
    State = as.factor(State),
    Year = as.factor(Year),
    Stratification1 = as.factor(Stratification1),
    Type = as.factor(Type),
    Medicaid_Expenses = as.numeric(Medicaid_Expenses),
    Median_Income = as.numeric(Median_Income)
  )

for(col in names(test_df)) {
  if(is.factor(test_df[[col]])) {
    test_df[[col]] <- factor(test_df[[col]], 
                             levels = levels(train_df[[col]]))
  }
}

# Regression prediction
test_df$rf_pred_Number_Diagnosed <- predict(rf_reg_model, test_df)

# Classification prediction
test_df$rf_pred_Type <- predict(rf_class_model, test_df, type = "response")

# Evaluation Metrics - only if test data has actual values
if("Number_Diagnosed" %in% names(test_df) && "Type" %in% names(test_df)) {
  reg_mae <- mean(abs(test_df$Number_Diagnosed - test_df$rf_pred_Number_Diagnosed), na.rm = TRUE)
  reg_rmse <- sqrt(mean((test_df$Number_Diagnosed - test_df$rf_pred_Number_Diagnosed)^2, na.rm = TRUE))
  class_acc <- mean(test_df$rf_pred_Type == test_df$Type, na.rm = TRUE)
  
  cat("Random Forest Regression:\nMAE:", reg_mae, "\nRMSE:", reg_rmse, "\n\n")
  cat("Random Forest Classification Accuracy:", class_acc, "\n")
}

# -------------------------------
# 4. FUTURE PREDICTIONS (2021–2030)
# -------------------------------
# Future years
years <- 2021:2030
states <- unique(as.character(train_df$State))
stratification_values <- unique(as.character(train_df$Stratification1))

# Modern approach to trend models using nested dataframes
medicaid_trends <- train_df %>%
  mutate(Year_numeric = as.numeric(as.character(Year))) %>%
  group_by(State) %>%
  nest() %>%
  mutate(model = map(data, ~lm(Medicaid_Expenses ~ Year_numeric, data = .x))) %>%
  ungroup()

income_trends <- train_df %>%
  mutate(Year_numeric = as.numeric(as.character(Year))) %>%
  group_by(State) %>%
  nest() %>%
  mutate(model = map(data, ~lm(Median_Income ~ Year_numeric, data = .x))) %>%
  ungroup()

# Create future data frame
future_data <- expand.grid(
  State = factor(states, levels = levels(train_df$State)),
  Year = factor(years, levels = c(levels(train_df$Year), as.character(years))),
  Stratification1 = factor(stratification_values, levels = levels(train_df$Stratification1)),
  stringsAsFactors = FALSE
)

# Function to predict future values 
predict_future_value <- function(state_val, year_val, model_data) {
  model_row <- model_data %>% filter(State == state_val)
  if(nrow(model_row) == 0) return(NA)
  
  prediction <- predict(model_row$model[[1]], 
                        newdata = data.frame(Year_numeric = as.numeric(year_val)))
  return(prediction)
}

# Apply predictions
future_data <- future_data %>%
  rowwise() %>%
  mutate(
    Medicaid_Expenses = predict_future_value(State, Year, medicaid_trends),
    Median_Income = predict_future_value(State, Year, income_trends)
  ) %>%
  ungroup()

# Make predictions with random forest models
future_data$Predicted_Number_Diagnosed <- predict(rf_reg_model, future_data)
future_data$Predicted_Cancer_Type <- predict(rf_class_model, future_data)

# -------------------------------
# 5. Summarize and Plot
# -------------------------------
# Grouped Summary
summary_df <- future_data %>%
  group_by(Year, Predicted_Cancer_Type) %>%
  summarise(
    Total_Cases = sum(Predicted_Number_Diagnosed, na.rm = TRUE),
    .groups = 'drop'
  )

# Plot by type over time
ggplot(summary_df, aes(x = Year, y = Total_Cases, color = Predicted_Cancer_Type, group = Predicted_Cancer_Type)) +
  geom_line(size = 1) +
  geom_point() +
  labs(title = "Predicted Diagnosed Cases by Cancer Type (2021–2030)",
       x = "Year", y = "Total Predicted Cases", color = "Cancer Type") +
  theme_minimal()

# -------------------------------
# 6. Export to Excel
# -------------------------------
write.xlsx(
  future_data,
  file = "cancer_predictions_dual_output_2021_2030.xlsx",
  sheetName = "Predictions",
  rowNames = FALSE
)
