import pandas as pd
import numpy as np
import joblib

rf_model = joblib.load('models/random_forest.pkl')


years_to_predict = np.arange(2022, 2051).reshape(-1, 1)  # Example year feature

# Use the trained model to make predictions
# Make sure to include the appropriate features that the model expects
predictions = rf_model.predict(years_to_predict)

# Create a DataFrame to store predictions
prediction_df = pd.DataFrame({
    'Year': years_to_predict.flatten(),
    'Prediction': predictions
})

# Output the predictions to a CSV file
prediction_df.to_csv('/daniel/data/model_predictions_2022_2050.csv', index=False)
