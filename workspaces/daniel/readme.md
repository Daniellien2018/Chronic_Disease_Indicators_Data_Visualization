# Chronic Obstructive Pulmonary Disease 

## Project Goal
This project focuses exclusively on analyzing COPD Prevalence by state, year, and stratification factors (e.g., age, gender). The objective is to preprocess data, build predictive models, and evaluate trands to improve understanding of COPD trends in the U.S.


## Folder Structure:
```
/workspaces/daniel/
├── data/
│   ├── raw/                # Raw COPD prevalence data  
│   ├── processed/          # Processed datasets (train/test splits)  
├── models/                 
│   ├── serialized models/  # Saved models (.pkl)  
├── notebooks/              
│   ├── 0_eda.ipynb         # Exploratory Data Analysis  
│   ├── 1_model_training.ipynb # Model training  
│   ├── 2_evaluation.ipynb  # Model evaluation  
│   ├── 3_forecasting.ipynb # Forecasting future COPD trends  
├── src/                    
│   ├── utils/              # Helper functions  
│   ├── data_prep.py        # Data preprocessing (one-hot encoding, train-test split)  
│   ├── linear_regression.py # Train a linear regression model  
│   ├── model_comparison.py # Compare multiple models  
└── README.md               # Project documentation  
```


## Workflow and Execution:
### 1 - Data Preparation
```
python3 src/data_prep.py
```
- Operations Performed
    - One-hot encoding categorical values
    - Splitting into `train.csv` and `test.csv`
### 2 - Train a Model
Traing a `linear regression model`
```
python3 src/linear_regression.py
```
- Saves trained model to models/{model}.pk;


### 3 - Evaluate model
```
python src/model_comparison.py
```
- Outputs model performance metrics


### Notebooks
- 0_eda.ipynb - Initial exploratory data analysis on entire CDI dataset
- 1_copd.ipynb - exploratory data analysis on COPD prevalence 






['Mortality with chronic obstructive pulmonary disease as underlying cause among adults aged >= 45 years',

'Mortality with chronic obstructive pulmonary disease as underlying or contributing cause among adults aged >= 45 years',

'Hospitalization for chronic obstructive pulmonary disease as first-listed diagnosis',

'Hospitalization for chronic obstructive pulmonary disease as any diagnosis',

'Hospitalization for chronic obstructive pulmonary disease as first-listed diagnosis among Medicare-eligible persons aged >= 65 years',

'Hospitalization for chronic obstructive pulmonary disease as any diagnosis among Medicare-eligible persons aged >= 65 years',

'Emergency department visit rate for chronic obstructive pulmonary disease as first-listed diagnosis',

'Emergency department visit rate for chronic obstructive pulmonary disease as any diagnosis',

'Prevalence of chronic obstructive pulmonary disease among adults >= 18',

'Prevalence of chronic obstructive pulmonary disease among adults >= 45 years',

'Prevalence of current smoking among adults >= 18 with diagnosed chronic obstructive pulmonary disease',

'Prevalence of current smoking among adults >= 45 years with diagnosed chronic obstructive pulmonary disease',

'Pneumococcal vaccination among noninstitutionalized adults aged >= 45 years with chronic obstructive pulmonary disease',

'Prevalence of activity limitation among adults >= 45 years with diagnosed chronic obstructive pulmonary disease',

'Influenza vaccination among noninstitutionalized adults aged >= 45 years with chronic obstructive pulmonary disease',

'Prevalence of activity limitation among adults >= 18 with diagnosed chronic obstructive pulmonary disease']