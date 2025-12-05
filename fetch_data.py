import yfinance as yf
import pandas as pd
import pandas_datareader.data as web
import datetime
import os

CACHE_FILE = "institutional_data.pkl"

def fetch_data():
    print("Fetching Daily S&P 500 Data (^GSPC)...")
    sp500 = yf.download("^GSPC", start="1950-01-01", progress=False)
    
    print("Columns (Before Cleanup):", sp500.columns)
    
    # Handle MultiIndex columns (common in new yfinance)
    if isinstance(sp500.columns, pd.MultiIndex):
        try:
            # Try to get 'Adj Close' level if it exists, else just drop the ticker level
            if 'Adj Close' in sp500.columns.get_level_values(0):
                sp500 = sp500['Adj Close']
            else:
                sp500.columns = sp500.columns.get_level_values(0)
        except Exception as e:
            print(f"Error handling MultiIndex: {e}")
            
    # Check if 'Adj Close' exists, else use 'Close'
    if 'Adj Close' in sp500.columns:
        price_col = 'Adj Close'
    elif 'Close' in sp500.columns:
        price_col = 'Close'
        print("Warning: 'Adj Close' not found. Using 'Close'.")
    elif isinstance(sp500, pd.Series):
         # If it became a Series (single column), rename to have a name we use
         sp500 = sp500.to_frame(name='Adj Close')
         price_col = 'Adj Close'
    else:
        # If sp500 is a dataframe but has no close column...
        print(f"Error: Could not find price column. Available: {sp500.columns}")
        return

    # Calculate Daily Returns
    sp500['Return'] = sp500[price_col].pct_change()
    sp500 = sp500.dropna()
    print(f"S&P 500 Data Cleaned: {len(sp500)} daily observations")

    print("Fetching Fama-French 3-Factor Data...")
    try:
        # F-F Research Data Factors (Daily)
        ff_data = web.DataReader('F-F_Research_Data_Factors_daily', 'famafrench', start="1950-01-01")[0]
        # FF data is in percent (e.g., 0.5 for 0.5%), convert to decimal
        ff_data = ff_data / 100.0
        print(f"Fama-French Data Fetched: {len(ff_data)} daily observations")
    except Exception as e:
        print(f"Error fetching Fama-French data: {e}")
        return None

    # Merge Data
    print("Merging Datasets...")
    # FF data index is usually just Date, ensure both are datetime
    sp500.index = pd.to_datetime(sp500.index)
    ff_data.index = pd.to_datetime(ff_data.index)

    merged = pd.merge(sp500[['Return']], ff_data, left_index=True, right_index=True, how='inner')
    merged.rename(columns={'Return': 'SP500_Ret', 'Mkt-RF': 'Mkt_RF'}, inplace=True)
    
    # Add Cycle Logic (Year 3 Dummy)
    # Logic: Year 3 is when (Year % 4) == 3. 
    # E.g., 2023 % 4 = 3 (Pre-Election). 2020 % 4 = 0 (Election).
    merged['Year'] = merged.index.year
    merged['Cycle_Year'] = merged['Year'] % 4
    # Note: 0 is Election, 1 is Post-Election, 2 is Midterm, 3 is Pre-Election
    
    merged['Is_Year3'] = (merged['Cycle_Year'] == 3).astype(int)
    merged['Is_Election'] = (merged['Cycle_Year'] == 0).astype(int)
    
    print(f"Final Merged Dataset: {len(merged)} rows")
    merged.to_pickle(CACHE_FILE)
    print(f"Data saved to {CACHE_FILE}")
    print(merged.head())
    print(merged.tail())
    return merged

if __name__ == "__main__":
    fetch_data()
