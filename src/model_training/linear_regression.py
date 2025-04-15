from sklearn.linear_model import LinearRegression

def train_linear_regression(train_df):
    """Train a linear regression model."""
    X_train = train_df.drop('Mortality', axis=1) 
    y_train = train_df['Mortality']
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model