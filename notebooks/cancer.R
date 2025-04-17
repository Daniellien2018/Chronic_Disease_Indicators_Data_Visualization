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
  # Filter to keep only specific cancer types (excluding screening tests)
  filter(Question %in% c(
    "Invasive cancer of the prostate, incidence",
    "Cancer of the female breast, mortality",
    "Invasive cancer of the oral cavity or pharynx, incidence",
    "Cancer of the oral cavity and pharynx, mortality",
    "Cancer of the prostate, mortality",
    "Invasive cancer (all sites combined), mortality",
    "Invasive cancer (all sites combined), incidence",
    "Invasive cancer of the female breast, incidence",
    "Cancer of the female cervix, mortality",
    "Invasive cancer of the cervix, incidence",
    "Cancer of the colon and rectum (colorectal), incidence",
    "Cancer of the colon and rectum (colorectal), mortality",
    "Cancer of the lung and bronchus, incidence",
    "Cancer of the lung and bronchus, mortality",
    "Melanoma, mortality",
    "Invasive melanoma, incidence"
  )) %>%
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

print(unique(filtered_df$Type))

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

# Clean median_Income and convert to numeric
final_df <- final_df %>%
  mutate(Median_Income = as.numeric(gsub(",", "", Median_Income)))

# Exploratory data analysis
# Summary stats for numeric columns
summary(Filter(is.numeric, final_df))

# Only factor categorical columns used in modeling
modified_df <- final_df %>%
  mutate(across(c(State, Stratification1, Type), as.factor))

# View first 5 rows
head(modified_df, 5)

# Split data into training and testing sets
# Training data uses data from 2010 - 2017 and testing data uses data from 2018 - 2020
set.seed(123)
train_df <- modified_df %>% filter(Year >= 2008 & Year <= 2013)
test_df <- modified_df %>% filter(Year >= 2013 & Year <= 2015)

# Preprocessing
train_df <- train_df %>%
  mutate(
    State = as.factor(State),
    Year = as.numeric(Year),  # Keep Year as numeric, not factor!
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

# REGRESSION: Predict Number_Diagnosed
rf_reg_model <- randomForest(Number_Diagnosed ~ State + Stratification1 + Medicaid_Expenses + Median_Income,
                             data = train_df_clean, ntree = 100)

print(rf_reg_model)

# CLASSIFICATION: Predict Type
unique(train_df_clean$Type)
rf_class_model <- randomForest(Type ~ State + Stratification1 + Medicaid_Expenses + Median_Income,
                               data = train_df_clean, ntree = 100)

print(rf_class_model)

# PREDICTIONS ON TEST SET
# Make sure test data has the same format as training data
test_df <- test_df %>%
  mutate(
    State = as.factor(State),
    Year = as.numeric(Year),  # Keep Year as numeric, not factor!
    Stratification1 = as.factor(Stratification1),
    Type = as.factor(Type),
    Medicaid_Expenses = as.numeric(Medicaid_Expenses),
    Median_Income = as.numeric(Median_Income)
  )

# FUTURE PREDICTIONS (2021-2050)
# Future years
years <- 2021:2050
states <- unique(as.character(train_df$State))
stratification_values <- unique(as.character(train_df$Stratification1))

# ---------- FIXED PART STARTS HERE ----------

# Calculate state-specific annual growth rates for Medicaid and Income
# These will provide more realistic predictions by using compound growth
medicaid_growth_rates <- train_df %>%
  group_by(State) %>%
  summarize(
    start_year = min(Year),
    end_year = max(Year),
    start_medicaid = median(Medicaid_Expenses[Year == min(Year)]),
    end_medicaid = median(Medicaid_Expenses[Year == max(Year)]),
    # Calculate annual compound growth rate
    medicaid_annual_growth = (end_medicaid / start_medicaid)^(1/(end_year - start_year)) - 1,
    # Apply sanity checks to growth rates
    medicaid_annual_growth = ifelse(
      medicaid_annual_growth > 0.15, 0.15, 
      ifelse(medicaid_annual_growth < -0.05, -0.05, medicaid_annual_growth)
    )
  ) %>%
  # Handle cases where growth rate couldn't be calculated properly
  mutate(
    medicaid_annual_growth = ifelse(
      is.na(medicaid_annual_growth) | !is.finite(medicaid_annual_growth), 
      median(medicaid_annual_growth, na.rm = TRUE), 
      medicaid_annual_growth
    )
  )

income_growth_rates <- train_df %>%
  group_by(State) %>%
  summarize(
    start_year = min(Year),
    end_year = max(Year),
    start_income = median(Median_Income[Year == min(Year)]),
    end_income = median(Median_Income[Year == max(Year)]),
    # Calculate annual compound growth rate  
    income_annual_growth = (end_income / start_income)^(1/(end_year - start_year)) - 1,
    # Apply sanity checks to growth rates
    income_annual_growth = ifelse(
      income_annual_growth > 0.08, 0.08, 
      ifelse(income_annual_growth < -0.02, -0.02, income_annual_growth)
    )
  ) %>%
  # Handle cases where growth rate couldn't be calculated properly
  mutate(
    income_annual_growth = ifelse(
      is.na(income_annual_growth) | !is.finite(income_annual_growth), 
      median(income_annual_growth, na.rm = TRUE), 
      income_annual_growth
    )
  )

print("Medicaid Growth Rates by State:")
print(medicaid_growth_rates)

print("Income Growth Rates by State:")
print(income_growth_rates)

# Get the most recent values as starting points for projections
latest_values <- train_df %>%
  group_by(State) %>%
  filter(Year == max(Year)) %>%
  summarize(
    latest_year = max(Year),
    latest_medicaid = median(Medicaid_Expenses),
    latest_income = median(Median_Income)
  )

# Create future data frame
future_data <- expand.grid(
  State = factor(states, levels = levels(train_df$State)),
  Year = years,  # Use numeric years, not factors
  Stratification1 = factor(stratification_values, levels = levels(train_df$Stratification1)),
  stringsAsFactors = FALSE
)

# Apply compound growth to project future values
future_data <- future_data %>%
  left_join(latest_values, by = "State") %>%
  left_join(medicaid_growth_rates %>% select(State, medicaid_annual_growth), by = "State") %>%
  left_join(income_growth_rates %>% select(State, income_annual_growth), by = "State") %>%
  rowwise() %>%
  mutate(
    # Use compound growth formula for projection
    years_to_project = Year - latest_year,
    Medicaid_Expenses = latest_medicaid * (1 + medicaid_annual_growth)^years_to_project,
    Median_Income = latest_income * (1 + income_annual_growth)^years_to_project
  ) %>%
  ungroup() %>%
  select(-latest_year, -latest_medicaid, -latest_income, -medicaid_annual_growth, 
         -income_annual_growth, -years_to_project)

# Ensure State is a factor with the same levels as in training data
future_data$State <- factor(future_data$State, levels = levels(train_df$State))

# Make predictions with random forest models
future_data$Predicted_Number_Diagnosed <- predict(rf_reg_model, future_data)
future_data$Predicted_Cancer_Type <- predict(rf_class_model, future_data)

# Add a new column to identify the stratification category
future_data <- future_data %>%
  mutate(StratificationCategory = case_when(
    Stratification1 %in% c("Male", "Female") ~ "Gender",
    TRUE ~ "Race/Ethnicity"
  ))

# Rename Stratification1 to make it clearer
future_data <- future_data %>%
  rename(StratificationValue = Stratification1)

# Make sure all predictions and columns are properly formatted
future_data <- future_data %>%
  mutate(
    Year = as.numeric(Year),
    Predicted_Number_Diagnosed = round(Predicted_Number_Diagnosed, 1),
    Medicaid_Expenses = round(Medicaid_Expenses, 2),
    Median_Income = round(Median_Income, 2)
  )

# Sort in a logical order
future_data <- future_data %>%
  arrange(Year, State, StratificationCategory, StratificationValue, Predicted_Cancer_Type)

# Export to Excel - include all columns including both StratificationCategory and StratificationValue
write.xlsx(
  future_data,
  file = "cancer_predictions_revised_2021_2050.xlsx",
  sheetName = "Predictions",
  rowNames = FALSE
)

# Make predictions
test_df$predicted_number_diagnosed <- predict(rf_reg_model, test_df)

# Calculate RMSE
rmse <- sqrt(mean((test_df$Number_Diagnosed - test_df$predicted_number_diagnosed)^2))
print(paste("RMSE for cancer prediction model:", round(rmse, 2)))

mean_actual <- mean(test_df$Number_Diagnosed)
mean_predicted <- mean(test_df$predicted_number_diagnosed)
percent_error <- (3308.7 / mean_actual) * 100
