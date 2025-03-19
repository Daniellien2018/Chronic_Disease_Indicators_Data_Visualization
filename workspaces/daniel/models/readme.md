# Model Building


Dataset Location: 
/home/daniel.lien/dev/homework/data/Single_Questions/COPD2_0.csv


Question:
- COPD2_0: Prevalence of chronic obstructive pulmonary disease among adults >= 18

Response Variable: 
- Crude Prevalance, %

Goal:
- Predict future COPD Prevalences for 2022-2030

Models to Build:
- Linear Regression - Baseline model 
- Polynomial Regression - Captures mild non-linearity
- Random Forest Regression - Handle complex, non-linear relationships
- XGBoost - Handle complex, non-linear relationships
- ARIMA - Hanldes time-series data

Metrics to Evaluate:
- Mean Absolute Error
- Mean Squared Error
- Root Mean Squared Errors
- R2 (Coefficient of Determination)

Data Preparation Strategies
- Random Splitting - Baseline, not suitable for final model validation
- Time Based Splitting - More realistic for forecasting futures
- Rolling Cross-Validation - Enhances robustness of model across multiple time windows


Drawbacks:
- Regression only works with numerical values, therefore both state and stratification need to be one-hot encoded
    - Loss of information on stratification 
    - Increase in Dimensionality can lead to overfitting
    - One-hot Encoding on States can lead to sparsity (results in a sparse matrix). This can make it harder for the model to learn generalizable patterns 
        - Drop first col to avoid Dummy Variable Trap
- Consider regularization techniques like Ridge or Lasso to reduce overfitting 
- The Time series problem 
-


USE One Hot encoding, but add a regularization techinque (ridge, lasso) to reduce the overfit 