import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to load and concatenate multiple CSV files
def load_exchange_rate_data(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    dfs = [pd.read_csv(os.path.join(folder_path, file)) for file in files]
    df = pd.concat(dfs, ignore_index=True)
    return df

# Load your dataset folder
data_folder = 'C:/Users/Sakshi.LAPTOP-FJD923PH/Desktop/NewCsvFiles'  # Update with the path to your folder
df = load_exchange_rate_data(data_folder)

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')

# Set 'Date' column as the index
df.set_index('Date', inplace=True)

# Take user input for the second currency
user_input_currency = input("Enter the second currency (e.g., GBP): ")
user_input_currency = user_input_currency.upper().strip()  # Convert to uppercase and remove leading/trailing spaces

# Find the closest matching column name in the DataFrame
selected_currency_pair = next((col for col in df.columns if user_input_currency in col.upper()), None)

if selected_currency_pair is None:
    print(f"Could not find a matching currency pair for '{user_input_currency}'. Please check your input.")
    exit()

# Get user input for the time period
user_input_time_period = input("Enter the time period (e.g., 'D' for day, 'W' for week): ")
selected_time_period = user_input_time_period.upper()

# Filter data based on user selection
filtered_df = df[selected_currency_pair].resample(selected_time_period).mean()

# Find peak and trough dates
peak_date = filtered_df.idxmax()
trough_date = filtered_df.idxmin()

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(filtered_df.index, filtered_df.values, label=f'{selected_currency_pair} Exchange Rate')

# Highlight peak and trough points on the chart
plt.scatter([peak_date, trough_date], [filtered_df.loc[peak_date], filtered_df.loc[trough_date]],
            color=['green', 'red'], marker='o', label=['Peak', 'Trough'])

plt.title(f'{selected_currency_pair} Exchange Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.grid(True)
plt.show()