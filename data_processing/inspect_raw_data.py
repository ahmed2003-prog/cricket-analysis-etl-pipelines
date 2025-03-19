import pandas as pd

# Load CSV files
batting_df = pd.read_csv("batting_data.csv")
bowling_df = pd.read_csv("bowling_data.csv")
fielding_df = pd.read_csv("fielding_data.csv")
squad_df = pd.read_csv("squad.csv")
# Function to clean data
def clean_dataframe(df):
    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values
    for col in df.columns:
        if df[col].dtype == 'object':  # If column is categorical
            df[col].fillna("Unknown", inplace=True)
        else:  # If column is numerical
            df[col].fillna(0, inplace=True)

    return df

# Clean each dataset
batting_df = clean_dataframe(batting_df)
bowling_df = clean_dataframe(bowling_df)
fielding_df = clean_dataframe(fielding_df)
squad_df = clean_dataframe(squad_df)

# Display cleaned data summary
print("Batting Data (Missing Values):")
print(batting_df.isnull().sum())

print("\nBowling Data (First 5 Rows):")
print(bowling_df.head())

print("\nFielding Data (First 5 Rows):")
print(fielding_df.head())

# Save cleaned data
batting_df.to_csv("cleaned_batting_data.csv", index=False)
bowling_df.to_csv("cleaned_bowling_data.csv", index=False)
fielding_df.to_csv("cleaned_fielding_data.csv", index=False)
squad_df.to_csv("cleaned_squad_data.csv", index=False)
print("\nCleaned data saved successfully!")
