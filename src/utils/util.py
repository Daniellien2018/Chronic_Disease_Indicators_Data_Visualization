
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def one_hot_encoding(df):
    #Check for categorical Columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    # Perform One-Hot Encoding on categorical Columns
    # Drop first to avoid the Dummy Variable Trap to avoid multicollinearity
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df

def save_model(model, model_name, model_dir='../daniel/models'):
    """Save the trained model to disk."""
    os.makedirs(model_dir, exist_ok=True) 
    model_path = os.path.join(model_dir, f"{model_name}.pkl")
    
    joblib.dump(model, model_path)
    print(f"Model saved at: {model_path}")

def load_model(model_name, model_dir='../models'):
    """Load a saved model from disk."""
    model_path = os.path.join(model_dir, f"{model_name}.pkl")
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print(f"Model loaded from: {model_path}")
        return model
    else:
        raise FileNotFoundError(f"Model {model_name} not found in {model_dir}")

def evaluate_model(model, test_df):
    """Evaluate the model on the test set and return metrics."""
    X_test = test_df.drop('Mortality', axis=1)
    y_test = test_df['Mortality']
    # Generate predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    return mae, mse, rmse, r2
