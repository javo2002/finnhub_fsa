
import pandas as pd

# Path to the CSV file
file_path = 'screener.csv'

'''
Time exported: 7:00 AM - 10:00 AM
'''

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, delimiter=',')

# Assuming the column representing stock changes is named 'Stock Change' or similar
# You may need to replace 'Stock Change' with the actual column name in your CSV file
stock_change_column = 'Change'  # Replace with your actual column name

# Drop rows with NaN values in the stock change column
df.dropna(subset=[stock_change_column], inplace=True)

tickers = list(df['Ticker'].unique())
print(tickers)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)


ticker_change_dict = dict(zip(df['Ticker'], df[stock_change_column]))

# Print the dictionary
# print("Ticker-Change Dictionary:", ticker_change_dict)

# Print the retrieved tickers
# print(tickers)

