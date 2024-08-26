import pandas as pd

# Read the CSV file
trades = pd.read_csv('data/trades/fantrax_8_25_24_trades.csv')

# Convert date to datetime
trades['Date (PDT)'] = pd.to_datetime(trades['Date (PDT)'], format='%a %b %d, %Y, %I:%M%p')

# Sort by date
trades = trades.sort_values('Date (PDT)')

# Create a Trade Number based on unique dates
trades['Trade Number'] = trades['Date (PDT)'].astype('int64').rank(method='dense').astype(int)

# Create a summary DataFrame
summary = []
for trade_num, trade_group in trades.groupby('Trade Number'):
    trade_date = trade_group['Date (PDT)'].iloc[0]
    trade_summary = {'Trade Number': trade_num, 'Date': trade_date}
    
    involved_teams = set(trade_group['From']) | set(trade_group['To'])
    for team in involved_teams:
        sent = trade_group[trade_group['From'] == team]['Player'].tolist()
        received = trade_group[trade_group['To'] == team]['Player'].tolist()
        trade_summary[f"{team} Sent"] = ', '.join(sent) if sent else 'None'
        trade_summary[f"{team} Received"] = ', '.join(received) if received else 'None'
    
    summary.append(trade_summary)

result = pd.DataFrame(summary)

# Reorder columns
cols = ['Trade Number', 'Date'] + sorted([col for col in result.columns if col not in ['Trade Number', 'Date']])
result = result[cols]

# Display the first few rows of the result
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Don't wrap to multiple lines
print(result.head())
print(result.columns)

# Optionally, save the result to a CSV file
result.to_csv('data/trades/trade_summary.csv', index=False)