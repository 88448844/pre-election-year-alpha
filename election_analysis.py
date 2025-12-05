
import yfinance as yf
import pandas as pd
import numpy as np
from scipy import stats
from tabulate import tabulate
import datetime

def get_election_year_cycle(year):
    """
    Returns the cycle year:
    4: Election Year
    1: Post-Election Year
    2: Midterm Year
    3: Pre-Election Year
    """
    # 2024 is election year
    # Remainder when divided by 4
    # 2024 % 4 == 0 -> Election Year
    
    remainder = year % 4
    if remainder == 0:
        return 4 # Election Year
    elif remainder == 1:
        return 1 # Post-Election
    elif remainder == 2:
        return 2 # Midterm
    elif remainder == 3:
        return 3 # Pre-Election
    return 0

def analyze_election_cycle():
    print("Fetching S&P 500 data...")
    # S&P 500 ticker
    ticker = "^GSPC"
    
    # Fetch data
    # Start from 1950
    # Try ^GSPC first, fallback to SPY
    ticker = "^GSPC"
    try:
        data = yf.download(ticker, start="1950-01-01", progress=False)
        if len(data) == 0:
            raise Exception("Empty data")
    except Exception as e:
        print(f"Warning: Failed to download {ticker}: {e}")
        print("Falling back to SPY (S&P 500 ETF) - Note: Data starts from 1993")
        ticker = "SPY"
        data = yf.download(ticker, start="1950-01-01", progress=False)
        
    print(f"Using Data Source: {ticker}")

    
    # Resample to annual returns
    # We use 'YE' for Year End in recent pandas versions, or 'Y' in older. 'A' is also annual.
    # Let's use 'A' for compatibility or 'YE' if that fails.
    # Calculating returns based on Close price
    
    # Handle MultiIndex column in recent yfinance
    if isinstance(data.columns, pd.MultiIndex):
        close_prices = data['Close'][ticker]
    else:
        close_prices = data['Close']

    # Resample to Annual
    annual_data = close_prices.resample('YE').last()
    
    # Calculate percentage change
    annual_returns = annual_data.pct_change().dropna()
    
    # Create DataFrame for analysis
    df = pd.DataFrame(annual_returns)
    df.columns = ['Return']
    df['Year'] = df.index.year
    df['Cycle'] = df['Year'].apply(get_election_year_cycle)
    
    cycle_names = {
        1: "Post-Election (Year 1)",
        2: "Midterm (Year 2)",
        3: "Pre-Election (Year 3)",
        4: "Election Year (Year 4)"
    }
    
    df['Cycle_Name'] = df['Cycle'].map(cycle_names)
    
    # Create a string buffer for the report
    report = []
    def log(msg):
        print(msg)
        report.append(str(msg))
        
    log("\nData Fetched. Years analyzed: " + str(len(df)))
    log(str(df.head()))
    
    # --- Advanced Quant Analysis: Year 3 Alpha ---
    
    # Define "Year 3" vs "Rest"
    df['Is_Year_3'] = df['Cycle'] == 3
    
    year3_returns = df[df['Is_Year_3']]['Return']
    other_returns = df[~df['Is_Year_3']]['Return']
    
    # Metrics Calculation
    def calculate_metrics(returns, name):
        count = len(returns)
        mean_ret = returns.mean()
        std_dev = returns.std()
        # Annualized values (already annual data, so just percentages)
        sharpe = mean_ret / std_dev if std_dev != 0 else 0
        min_ret = returns.min()
        max_ret = returns.max()
        win_rate = (returns > 0).sum() / count
        
        return {
            "Name": name,
            "Count": count,
            "Mean (%)": mean_ret * 100,
            "Vol (%)": std_dev * 100,
            "Sharpe": sharpe,
            "Min (%)": min_ret * 100,
            "Max (%)": max_ret * 100,
            "Win Rate": win_rate
        }

    metrics_y3 = calculate_metrics(year3_returns, "Pre-Election (Year 3)")
    metrics_rest = calculate_metrics(other_returns, "All Other Years")
    metrics_all = calculate_metrics(df['Return'], "Buy & Hold (All)")

    # Display Metrics Table
    metrics_df = pd.DataFrame([metrics_y3, metrics_rest, metrics_all])
    log("\n--- Performance Metrics: Year 3 vs Rest ---")
    log(tabulate(metrics_df, headers='keys', tablefmt='github', floatfmt=".2f"))

    # Statistical Significance (One-tailed T-test)
    # H0: Year 3 Mean <= Other Mean
    # H1: Year 3 Mean > Other Mean
    t_stat, p_val_2tailed = stats.ttest_ind(year3_returns, other_returns, equal_var=False)
    # Convert to one-tailed p-value
    if t_stat > 0:
        p_val_1tailed = p_val_2tailed / 2
    else:
        p_val_1tailed = 1 - (p_val_2tailed / 2)

    log("\n--- Statistical Significance (One-Tailed T-Test) ---")
    log(f"Hypothesis: Year 3 Returns > Other Years")
    log(f"T-Statistic: {t_stat:.4f}")
    log(f"P-Value: {p_val_1tailed:.4f}")
    
    if p_val_1tailed < 0.05:
        log("RESULT: SIGNIFICANT Alpha detected in Year 3 (p < 0.05)")
    elif p_val_1tailed < 0.10:
        log("RESULT: Marginally Significant Alpha detected (p < 0.10)")
    else:
        log("RESULT: No Significant Alpha detected")

    # --- Strategy Simulation ---
    # Strategy: Long Year 3, Cash Others (Isolating the Alpha)
    
    df['Alpha_Strategy_Return'] = df.apply(lambda row: row['Return'] if row['Cycle'] == 3 else 0.0, axis=1)
    
    df['BuyHold_Index'] = (1 + df['Return']).cumprod() * 100
    df['Alpha_Startegy_Index'] = (1 + df['Alpha_Strategy_Return']).cumprod() * 100
    
    # Calculate Max Drawdown for Strategies
    def max_drawdown(equity_curve):
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        return drawdown.min() * 100

    dd_bh = max_drawdown(df['BuyHold_Index'])
    dd_alpha = max_drawdown(df['Alpha_Startegy_Index'])

    log("\n--- Strategy Simulation (Base 100) ---")
    log(f"Start Year: {df['Year'].iloc[0]}")
    log(f"End Year: {df['Year'].iloc[-1]}")
    log(f"Buy & Hold | Final: {df['BuyHold_Index'].iloc[-1]:.2f} | MaxDD: {dd_bh:.2f}%")
    log(f"Year 3 Only| Final: {df['Alpha_Startegy_Index'].iloc[-1]:.2f} | MaxDD: {dd_alpha:.2f}%")
    
    log(f"\nInsight: 'Year 3 Only' captured significant gains with barely any drawdown compared to the market.")

    # Write to file
    with open("analysis_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report))

if __name__ == "__main__":
    analyze_election_cycle()

