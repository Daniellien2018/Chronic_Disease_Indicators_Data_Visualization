import pandas as pd
from sklearn.linear_model import LinearRegression

def train_linear_regression(train_df):
    """Train a linear regression model."""
    # Select features and target variable - Use all features except the response
    X_train = train_df.drop('Mortality', axis=1) 
    y_train = train_df['Mortality']
    
    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model
