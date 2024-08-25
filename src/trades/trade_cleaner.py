import pandas as pd

trades = pd.read_csv('data/trades/fantrax_8_25_24_trades.csv')

trades['Date (PDT)'] = pd.to_datetime(trades['Date (PDT)'])

# Sort by date and assign unique trade numbers
trades['Trade Number'] = (trades['Date (PDT)'].diff() != pd.Timedelta(0)).cumsum()

# Create a function to combine assets
def combine_assets(group):
    return ', '.join(group['Player'].astype(str))

# Group by Trade Number and From/To teams
grouped = trades.groupby(['Trade Number', 'From', 'To']).apply(combine_assets).reset_index()
grouped.columns = ['Trade Number', 'From Team', 'To Team', 'Assets']

# Pivot the table to have assets for each team in separate columns
result = grouped.pivot(index='Trade Number', columns='To Team', values='Assets').reset_index()
result.columns.name = None

# Rename columns
result = result.rename(columns={col: f"{col} Received" for col in result.columns if col != 'Trade Number'})

# Add trade date
trade_dates = trades.groupby('Trade Number')['Date (PDT)'].first().reset_index()
result = result.merge(trade_dates, on='Trade Number')

# Reorder columns
cols = ['Trade Number', 'Date (PDT)'] + [col for col in result.columns if col not in ['Trade Number', 'Date (PDT)']]
result = result[cols]

print(result.head())