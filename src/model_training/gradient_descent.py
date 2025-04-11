import pandas as pd
from sklearn.linear_model import SGDRegressor

def train_gradient_descent(train_df):
    """Train a Stochastic Gradient Descent regression model."""
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']
    
    model = SGDRegressor(max_iter=1000, tol=1e-3)
    model.fit(X_train, y_train)
    
    return model
