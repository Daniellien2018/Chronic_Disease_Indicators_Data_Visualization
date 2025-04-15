Chronic Disease Indicators Data Visualization
============================================

DESCRIPTION - Project Overview:
-----------------
This project aims to forecast mortality rates across U.S. states from 2021 to 2050, using historical public health data and socioeconomic indicators.
A Random Forest regression model is trained to predict mortality outcomes based on variables such as Medicaid spending, median household income, and chronic disease stratifications (e.g., gender, race/ethnicity).

Objectives:
-----------
- Collect and process reliable state-level data from public sources.
- Forecast socioeconomic drivers (e.g., income, Medicaid spending) through 2050.
- Integrate chronic disease indicators by stratification group.
- Train and evaluate different machine learning models to predict mortality from historical patterns.
- Use the best model to estimate future mortality trends by state and demographic subgroup.

Data Sources:
-------------
1. U.S. Chronic Disease Indicators (CDI) Dataset
   Source: CDC – U.S. Chronic Disease Indicators
   URL: https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators/hksd-2xuw/about_data
   NOTE: This dataset is currently unavailable due to current administration laws (Jan. 2025). A copy has been saved and zipped for this project purposes. Find in data/raw/.
   Description: Provides state-level data on chronic diseases and risk factors, compiled from various surveys and administrative sources. 
   Used Range: 2011-2020
   Collection Method:
     - Navigate to the webpage
     - Click the "Export" button
     - NOTE: Please find the CDC CDI dataset in the uploaded .zip in data/raw/.
   Purpose: Used to analyze mortality and risk factors and to train prediction models.

2. Medicaid Spending by State of Residence (1980–2020)
   Source: Centers for Medicare & Medicaid Services
   URL: https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/state-residence
   Table: Health Expenditures by State of Residence – Medicaid (Table 21)
   Description: Historical healthcare spending by state, including Medicaid expenditures.
   Collection Method:
     - Download the ZIP file labeled "Health expenditures by state of residence"
     - Locate and extract "MEDICAID_AGGREGATE20.csv"
   Purpose: Used for forecasting state-level Medicaid spending.

3. Median Income by State (1967–2022)
   Source: U.S. Census Bureau
   URL: https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html
   Table: Table H-8 – Median Household Income by State
   Description: Contains annual, inflation-adjusted median household income by state.
   Collection Method:
     - Scroll to Table H-8
     - Download the Excel (.xls) file
   Purpose: Used for income trend forecasting from 2021–2050.

INSTALLATION - Setup Instructions:
-------------------
1. Clone the repository and set up a virtual environment:

   git clone <repo-url>
   cd Chronic_Disease_Indicators_Data_Visualization

   python3 -m venv .venv
   source .venv/bin/activate   (for Linux/macOS)

2. Install project dependencies:

   pip install -r requirements.txt

EXECUTION – COPD Mortality Forecasting Demo:
----------------------------------------------------

Step 00 – Data Collection:
  Ensure raw data has been downloaded and placed into the directory:
  data/raw/. Do not rename any of the dataset filenames.

Step 0 – Data Cleaning:
  Run:
    python3 src/0_data_cleaning.py
  Function:
    - Cleans and merges Chronic Disease, Medicaid, and Income datasets
    - Handles missing values and formatting issues
    - Output: data/processed/merged_copd_income_medicaid

Step 1 – Data Preprocessing:
  Run:
    python3 src/1_data_preprocessing.py
  Function:
    - Splits data into train/test sets based on year
    - One-hot encodes categorical values
    - Output: data/split/train.csv, data/split/test.csv

Step 2 – Model Training:
  Run:
    python3 src/2_train_models.py
  Function:
    - Trains various regression models (linear, polynomial, ridge, lasso, elastic net, random forest)
    - Saves trained model artifacts to: model_artifacts/{model}

Step 3 – Model Comparison:
  Run:
    python3 src/3_model_comparison.py
  Function:
    - Evaluates models using MAE, MSE, RMSE, R²
    - Selects best-performing model
    - Output: output/model_comparison_results.csv

Step 4 – Forecasting Predictors:
  Run:
    python3 src/4_forecast.py
  Function:
    - Forecasts Medicaid spending and income through 2050
    - Output: data/predictors/forecasted_income_medicaid.csv

Step 5 – Making Predictions:
  Run:
    python3 src/5_make_predictions.py
  Function:
    - Loads best model and forecasted inputs
    - Predicts future COPD mortality rates by state and subgroup
    - Output: outputs/COPD_predicted_mortality_2021_2050.csv

END. 