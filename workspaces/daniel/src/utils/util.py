import pandas as pd


def one_hot_encoding(df):
    #Check for categorical Columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    # Perform One-Hot Encoding on categorical Columns
    # Drop first to avoid the Dummy Variable Trap to avoid multicollinearity
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    return df