import pandas as pd

# Assuming df is your DataFrame
# Example DataFrame for demonstration
data = {
    'Title': ['Title1', 'Title2', 'Title3'],
    'Source': ['Source1', 'Source2', 'Source3'],
    'id': ['ID1', 'ID2', 'ID3'],
}
df = pd.DataFrame(data)

# Iterate through the DataFrame rows and print the 'Title' and 'Source' values
for index, row in df.iterrows():
    print(row['Title'], row['Source'])
