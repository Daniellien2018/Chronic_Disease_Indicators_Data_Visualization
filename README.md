# Chronic Disease Indicators Data Visualization

## Project Overview:
This project aims to forecast mortality rates across U.S. states from 2021 to 2050, leveraging a combination of historical public health data and socioeconomic indicators. Using a Random Forest regression model, we predict mortality outcomes based on key variables such as Medicaid spending, median household income, and chronic disease stratifications (e.g., gender, race/ethnicity).
## Objectives:
- Collect and process reliable state-level data from public sources.
- Forecast socioeconomic drivers (e.g., income, Medicaid spending) through 2050.
- Integrate chronic disease indicators by stratification group.
- Train and evaluate different machine learning models to predict mortality from historical patterns.
- Use the best model to estimate future mortality trends by state and demographic subgroup.
## Data Sources
This project uses several public datasets collected from trusted government and research organization. Each dataset is described with instructions on how to access.

1. U.S. Chronic Disease Indicators (CDI) Dataset
    - Source: [Centers for Disease Control and Prevention (CDC) – U.S. Chronic Disease Indicators](https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators/hksd-2xuw/about_data)
    - Description: The CDI dataset provides state-level data on key chronic diseases and their risk factors, compiled from various sources such as surveys, vital records, and administrative data. It includes standardized definitions to estimate and track a wide range of chronic disease indicators.
    - Data Range (Used): 2011-2020
    - Collection Method:
        - Navigate to webpage above
        - Click on "Export" button
    - Used for: Analyzing state-level chronic disease mortality and associated risk factors. This dataset also serves as the primary source for training and generating chronic illness mortality predictions. 
2. Medicaid Spending by State of Residence (1980-2020)
    - Source: [Centers for Medicare & Medicaid Services – National Health Expenditure Data: State of Residence](https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/state-residence)
    - Table Used: Health Expenditures by State of Residence – Medicaid (Table 21)
    - Description: This dataset provides historical health care spending by state of residence, including detailed breakdowns by service and payer category. Speficially, Table 21 reports total Medicaid expenditures per state. 
    - Data Range: 1980-2020
    - Collection Method:
        - Navigate to webpage above
        - Download the ZIP file labeled **"Health expenditures by state of residence"**
        - Locate **"MEDICAID_AGGREGATE20.csv"**
    - Used for: Forecasting future state-level Medicaid spending to model its relationship with mortality
3. Median Income by State (1967-2022)
    - Source: [U.S. Census Bureau – Historical Income Tables: Households](https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html)
    - Table Used: Table H-8. Median Household Income by State
    - Description: This dataset contains inflation-adjusted and nominal median household income data, broken down by state and year
    - Data Range: 1984-2022
    - Collection Method:
        - Navigate to webpage above
        - Scroll to **Table H-8** and clikc the Excel link (.xls format).
        - Download the Excel
    - Used for: Forecasting state-level income trends between 2021-2050 


    
## Setup Instructions

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

# For Windows (Command Prompt)
.venv\Scripts\activate

# For Windows (PowerShell)
.venv\Scripts\Activate.ps1
```
### Install Project Dependencies 
```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage
0_data_cleaning.py
1_data_preprocessing.py
2_train_models.py
3_model_comparison.py


### 1: Download data 
Download all required data from their respective sources and save them into the `data/` directory.

### 2: Proprocess Data (Train/Test Split)

### 3: Train Models

### 4:Evaluate Performance 

### 5: Forecast

### 6: Make Predictions

## Directory Structure

## License 

## Contributors 
