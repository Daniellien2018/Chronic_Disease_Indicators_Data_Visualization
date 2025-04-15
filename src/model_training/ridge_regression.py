from sklearn.linear_model import Ridge

def train_ridge(train_df):
    """Train a Ridge regression model."""
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']
    
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    
    return model