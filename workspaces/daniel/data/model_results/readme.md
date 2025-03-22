# Model Results

## Metric Descriptions:
1) MAE (Mean Absolute Error)
- Measures the average magnitude of the errors in your predictions, without considering direction
- Intuitive: on average, how much predictions differ from actual values
- Lower MAE is better

2) MSE (Mean Squared Error)
- Measures the average of the squared differences between predicted and actual values.
- Intuitive: Penalizes larger errors more heavily due to the squaring, making it sensitive to outliers.
- Lower MSE is better

3) RMSE (Root Mean Squared Error)
- The square root of MSE, providing the error in the same unit as the target variable.
- Intuitive: It gives a clearer idea of the magnitude of errors in the same scale as the target variable.
- Lower RMSE is better.

3) R2 (Coefficient of Determination)
- Indicates how well the model explains the variance in the target variable.
- Intuitive: R2 = 1 = perfect fit, R2 < 0 = Worse than predicting the mean, R2 = 0 = No explanatory power
- Higher R2 is better.


## Results

3/21 - Random Train/Test Split, One-Hot
|Model|MAE|MSE|RMSE|R^2|
|---|---|---|---|---|
|Linear Regression|1.0348|2.555|1.598|0.703|
|Polynomial Regression|1.79e^4|7.52e^10|2.74e^5|-8.73e^9|
|Random Forest|1.001|2.744|1.656|0.681|
|Gradient Descent|7.59e^14|5.77e+29|7.59e^14|-6.69e+28|
|Ridge Regression|1.046|2.634|1.623|0.694|
|Lasso Regression|1.834|6.298|2.509|0.269|
|Elastic Net Regression|1.838|6.331|2.516|0.265|

Takeaways:
- Linear Regression leads with lowest MSE, RMSE, and Higher R2
- Ridge Regression performs quite well, with R2=69, and only slightly higher MAE,MSE,RMSE
- Random Forest is close second with marginally better MAE, but lower R2
- Polynomial and GD both have extreme errors and very negative R2, indicating overfit/unstable
- Lasso and Elastic have higher MAE,MSE,RMSE, and very low R2 

3/21 - Ordinal Train/Test Split, One-hot

|Model|MAE|MSE|RMSE|R^2|
|---|---|---|---|---|
|Linear Regression|1.153|3.033|1.741|0.611|
|Polynomial Regression|1.373|18.94|4.352|-1.431|
|Random Forest|1.167|3.461|1.860|0.556|
|Gradient Descent|9.39*e^11|8.8*e^24|9.39*e^11|-1.1*e^27|
|Ridge Regression|1.163|3.046|1.745|0.608|
|Lasso Regression|1.924|5.995|2.448|0.231|
|Elastic Net Regression|1.941|5.964|2.442|0.235|

Takeaways:
- Linear and Ridge still perform the best, both explaining 61% of the variance 
- Random Forest still performs well, but with a drop in 
