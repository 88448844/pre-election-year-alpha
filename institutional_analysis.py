import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = "institutional_data.pkl"

def run_analysis():
    print("Loading Data...")
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found. Run fetch_data.py first.")
        return

    df = pd.read_pickle(DATA_FILE)
    
    # 1. Prepare Data for Regression
    # Factos: Mkt-RF, SMB, HML. Target: SP500_Ret - RF
    # Note: RF is in the dataset as 'RF' (Risk-Free rate)
    df['Excess_Ret'] = df['SP500_Ret'] - df['RF']
    
    # Define Independent Variables (X) and Dependent Variable (y)
    X = df[['Mkt_RF', 'SMB', 'HML', 'Is_Year3']]
    X = sm.add_constant(X) # Adds a constant term (alpha)
    y = df['Excess_Ret']
    
    # 2. Daily Factor Regression (Full Sample)
    print("\n--- Multifactor Regression (Daily Data) ---")
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 1}) # Robust Standard Errors
    print(model.summary())
    
    gamma_coef = model.params['Is_Year3']
    gamma_pval = model.pvalues['Is_Year3']
    print(f"\nYear 3 Alpha Coefficient (Daily): {gamma_coef:.6f}")
    print(f"Year 3 Alpha P-Value: {gamma_pval:.6f}")
    
    # 3. Rolling OLS (Stability Check) - 1260 days (~5 years)
    print("\n--- Running Rolling OLS (Window=1260 days) ---")
    rolling = RollingOLS(y, X, window=1260).fit()
    rolling_params = rolling.params
    
    # Plot Rolling Year 3 Coefficient
    plt.figure(figsize=(12, 6))
    plt.plot(rolling_params.index, rolling_params['Is_Year3'], label='Year 3 Alpha (Rolling 5Y)', color='blue')
    plt.axhline(0, color='red', linestyle='--')
    plt.title('Rolling 5-Year Alpha Coefficient for Pre-Election Year (Year 3)')
    plt.ylabel('Alpha coef')
    plt.legend()
    plt.grid(True)
    plt.savefig('rolling_alpha.png')
    print("Saved rolling_alpha.png")
    
    # 4. Bootstrap Analysis
    print("\n--- bootstrapping Sharpe Ratios (10,000 iterations) ---")
    year3_rets = df[df['Is_Year3'] == 1]['Excess_Ret']
    other_rets = df[df['Is_Year3'] == 0]['Excess_Ret']
    
    n_sims = 10000
    diffs = []
    
    for _ in range(n_sims):
        # Resample with replacement
        sample_y3 = year3_rets.sample(n=len(year3_rets), replace=True)
        sample_other = other_rets.sample(n=len(other_rets), replace=True)
        
        # Calculate Annualized Sharpe
        sharpe_y3 = (sample_y3.mean() / sample_y3.std()) * np.sqrt(252)
        sharpe_other = (sample_other.mean() / sample_other.std()) * np.sqrt(252)
        
        diffs.append(sharpe_y3 - sharpe_other)
        
    diffs = np.array(diffs)
    p_val_boot = (diffs <= 0).sum() / n_sims
    print(f"Bootstrap P-Value (Prob that Year 3 Sharpe <= Other Sharpe): {p_val_boot:.5f}")
    
    # 5. Drawdown Analysis
    print("\n--- Drawdown Analysis ---")
    # Strategy: Invest in SP500 ONLY during Year 3. Cash (RF) otherwise.
    # Actually, simplistic view: Cash return = 0 for simplicity or use RF.
    # Let's use 0 for cash to be conservative/simple (RF adds return).
    
    df['Strategy_Ret'] = np.where(df['Is_Year3'] == 1, df['SP500_Ret'], 0.0)
    df['BuyHold_Curve'] = (1 + df['SP500_Ret']).cumprod()
    df['Strategy_Curve'] = (1 + df['Strategy_Ret']).cumprod()
    
    def get_max_dd(curve):
        peak = curve.cummax()
        dd = (curve - peak) / peak
        return dd.min()
    
    dd_bh = get_max_dd(df['BuyHold_Curve'])
    dd_strat = get_max_dd(df['Strategy_Curve'])
    
    print(f"Max Drawdown (Buy & Hold): {dd_bh:.2%}")
    print(f"Max Drawdown (Year 3 Only): {dd_strat:.2%}")
    
    # Save a comparison plot
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['BuyHold_Curve'], label='Buy & Hold', color='gray', alpha=0.6)
    plt.plot(df.index, df['Strategy_Curve'], label='Year 3 Only', color='green')
    plt.yscale('log')
    plt.title('Equity Curve: Year 3 Only vs Buy & Hold (Log Scale)')
    plt.legend()
    plt.grid(True)
    plt.savefig('equity_curve.png')
    print("Saved equity_curve.png")

if __name__ == "__main__":
    import os
    run_analysis()
