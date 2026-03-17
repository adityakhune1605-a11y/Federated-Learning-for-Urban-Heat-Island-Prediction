import pandas as pd

# The data you provided
data = {
    'temperature': [35.2, 36.0, 33.5, 32.8, 37.0, 34.5],
    'humidity': [60, 62, 58, 55, 65, 59],
    'label': [1, 1, 0, 0, 1, 0]
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file without the index
df.to_csv('data.csv', index=False)
