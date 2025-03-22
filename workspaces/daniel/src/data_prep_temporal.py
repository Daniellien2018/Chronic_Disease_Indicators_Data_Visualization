import pandas as pd
from utils.util import one_hot_encoding

"""
Splits the data into Train/Test based on year
2011-2018 - Training Data
2018-2021 - Testing Data
"""

def load_data(file_path):
    """Load dataset from CSV."""
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    """Preprocess the data (e.g., handle missing values, drop columns)."""
    # No specific preprocessing needed for now
    return df  

def time_based_split(df):
    """Split data into train (2011-2018) and test (2019-2021) based on the 'year' column."""
    train_df = df[(df['Year'] >= 2011) & (df['Year'] <= 2018)]
    test_df = df[(df['Year'] >= 2019) & (df['Year'] <= 2021)]
    return train_df, test_df

def save_splits(train_df, test_df, train_file='data/processed/train.csv', test_file='data/processed/test.csv'):
    """Save the train and test splits to CSV files."""
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

if __name__ == "__main__":
    # Load data
    file_path = 'data/raw/COPD2_0.csv'
    df = load_data(file_path)

    # Preprocess data
    df = preprocess_data(df)

    # Apply one-hot encoding to categorical columns
    df = one_hot_encoding(df)

    # Perform time-based split
    train_df, test_df = time_based_split(df)

    # Save the splits to CSV
    save_splits(train_df, test_df)

    print("Time-based data split and saved successfully!")
