Goal: I am only looking at COPD prevalence by state, year, and stratification 


Folder Structure:
/workspaces/daniel/

- workspaces/daniel/
    - data/
        - processed/
        - raw/
    - models/
        - serialized models
    - notebooks/
        - 0_eda.ipynb
        - 1_model_training.ipynb
        - 2_evaluation.ipynb
        - 3_forecasting.ipynb
    - src/
        - utils/
        - data_prep.py
        - {model}_training.py
        

Process:
RUN EVERYTHING IN /project/workspaces/daniel
- src/data_prep.py 
    - one-hot encoding
    - prepare train.csv and test.csv
- src/linear_regression.py # train a linear regression model
    - save to models/{model}.pkl
- src/model_comparison.py
    - Compare model outputs

Questions:




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