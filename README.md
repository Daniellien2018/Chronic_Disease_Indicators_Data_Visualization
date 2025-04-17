# Chronic Disease Indicators Data Visualization

## 🩺 Project Overview:
This project aims to forecast mortality rates across U.S. states from 2021 to 2050, leveraging a combination of historical public health data and socioeconomic indicators. Using a Random Forest regression model, we predict mortality outcomes based on key variables such as Medicaid spending, median household income, and chronic disease stratifications (e.g., gender, race/ethnicity).

## 🎯  Objectives:
- Collect and process reliable state-level data from public sources.
- Forecast socioeconomic drivers (e.g., income, Medicaid spending) through 2050.
- Integrate chronic disease indicators by stratification group.
- Train and evaluate different machine learning models to predict mortality from historical patterns.
- Use the best model to estimate future mortality trends by state and demographic subgroup.

## 🧠 Data Sources
This project uses several public datasets collected from trusted government and research organization. Each dataset is described with instructions on how to access.

1. U.S. Chronic Disease Indicators (CDI) Dataset
    - Source: <a href="https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators/hksd-2xuw/about_data" target="_blank">Centers for Disease Control and Prevention (CDC) – U.S. Chronic Disease Indicators</a>
    - EDITOR NOTE: This dataset is currently unavailable due to current administration laws (Jan. 2025). A copy has been saved and zipped for this project purposes. Find in **data/raw/*.zip**
    - Description: The CDI dataset provides state-level data on key chronic diseases and their risk factors, compiled from various sources such as surveys, vital records, and administrative data. It includes standardized definitions to estimate and track a wide range of chronic disease indicators.
    - Data Range (Used): 2011-2020
    - Collection Method:
        - ~~Navigate to webpage above~~
        - ~~Click on "Export" button~~
        - EDITOR NOTE: Extract from the .zip file in **data/raw/**
    - Used for: Analyzing state-level chronic disease mortality and associated risk factors. This dataset also serves as the primary source for training and generating chronic illness mortality predictions. 
2. Medicaid Spending by State of Residence (1980-2020)
    - Source: <a href="https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/state-residence" target="_blank">Centers for Medicare & Medicaid Services – National Health Expenditure Data: State of Residence</a> 
    - Table Used: Health Expenditures by State of Residence – Medicaid (Table 21)
    - Description: This dataset provides historical health care spending by state of residence, including detailed breakdowns by service and payer category. Speficially, Table 21 reports total Medicaid expenditures per state. 
    - Data Range: 1980-2020
    - Collection Method:
        - Navigate to webpage above
        - Download the ZIP file labeled **"Health expenditures by state of residence"**
        - Locate **"MEDICAID_AGGREGATE20.csv"**
    - Used for: Forecasting future state-level Medicaid spending to model its relationship with mortality
3. Median Income by State (1967-2022)
    - Source: <a href="https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html" target="_blank">U.S. Census Bureau – Historical Income Tables: Households</a>
    - Table Used: Table H-8. Median Household Income by State
    - Description: This dataset contains inflation-adjusted and nominal median household income data, broken down by state and year
    - Data Range: 1984-2022
    - Collection Method:
        - Navigate to webpage above
        - Scroll to **Table H-8** and clikc the Excel link (.xls format).
        - Download the Excel
    - Used for: Forecasting state-level income trends between 2021-2050 


    
## 🛠️ Setup Instructions
Demo Set Up Video - https://youtu.be/_fmsY-HX-P0

### Clone the repository and set up Virtual Environment
```bash
## Clone the repository
git clone <repo-url>
cd Chronic_Disease_Indicators_Data_Visualization

## Create a virtual environment
python3 -m venv .venv

## Activate the virtual environment:
# For Linux/macOS
source .venv/bin/activate
```
### Install Project Dependencies 
```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Project Execution - COPD Demo
### 00. Data Collection
Before running this project, ensure that the proper data has been collected from the data sources listed above. Collect the required data into `data/raw/`. Do not rename any of the dataset filenames.


### 0. Data Cleaning
```bash
python3 src/0_data_cleaning.py
```
- Cleans and prepares the raw Chronic Disease Indicators, Medicaid Spending, and Median Income datasets, merging into one
- Handles missing values and formatting issues
- Produces `data/processed/merged_copd_income_medicaid`

### 1. Data Preprocessing
```bash
python3 src/1_data_preprocessing.py
```
- Splits the processed dataset into train/test splits based on temporality 
- Applied One-hot Encoding to categorical values 
- Produces `data/split/train.csv` and `data/split/test.csv`

### 2. Model Training
```bash
python3 src/2_train_models.py
``` 
- Train a variety of regression models including linear regression, polynomial regression, gradient descent, ridge regression, lasso regression, elastic net, and random forest. 
- Saves each trained model artifact to `model_artifacts/{model}`

### 3. Model Comparison
```bash
python3 src/3_model_comparison.py
```
- Compares trained models using performance metrics including MAE, MSE, RMSE, and R2
- Identifies best-performing model for prediction
- Produces model results to `output/model_comparison_results.csv`

### 4. Forecasting Future Predictors
```bash
python3 src/4_forecast.py
```
- Forecasts key predictor variables (Medicaid Spending, Median Income) from 2021-2050
- Outputs forecasted values used in the final prediction step
- Saves forecasts to `data/predictors/forecasted_income_medicaid.csv`

### 5. Make Predictions
```bash
python3 src/5_make_predictions.py
```
- Loads the best model and forecasted data
- Predicts future mortality rates by state and stratification group
- Saves final output to `outputs/COPD_predicted_mortality_2021_2050.csv`
