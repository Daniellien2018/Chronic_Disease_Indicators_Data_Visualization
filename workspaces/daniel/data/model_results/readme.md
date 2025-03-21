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


3/21 - Random Train/Test Split, One-Hot
Model,MAE,MSE,RMSE,R²
polynomial_regression,17922.470924333746,75262541897.96758,274340.1937339251,-8735090082.721975
gradient_descent,759579378838567.6,5.7696220498025544e+29,759580282116548.5,-6.69631493743303e+28
linear_regression,1.0348039165311231,2.555497212314177,1.598592259556569,0.7034049369668243
random_forest,1.0013167938931296,2.744908190839693,1.6567764456436762,0.6814215981299654

Takeaways:
- Linear Regression leads with lowest MSE, RMSE, and Higher R2
- Random Forest is close second with marginally better MAE, but lower R2

3/21 - Ordinal Train/Test Split, One-hot

