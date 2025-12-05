import nbformat as nbf

nb = nbf.v4.new_notebook()

# Title and Introduction
title_cell = nbf.v4.new_markdown_cell("""# 🏛️ Institutional Grade Research: The Pre-Election Alpha
**Author:** Gabriel Bengo (Quantitative Research Team)  
**Date:** December 2024

## Abstract
This notebook performs a rigorous factor-based analysis of the US Presidential Election Cycle (1950-2024). We test the hypothesis that **Year 3 (Pre-Election)** delivers statistically significant alpha after controlling for standard risk factors (Market, Size, Value).

### Methodology
1. **Data**: Daily S&P 500 returns and Fama-French 3-Factors.
2. **Model**: Rolling OLS Regression ($R - R_f = \alpha + \beta_{Mkt} + \beta_{SMB} + \beta_{HML} + \gamma Year3$)
3. **Validation**: HAC Robust Standard Errors & Bootstrap Resampling (10,000 iterations).
4. **Reality Check**: Daily Drawdown analysis.
""")

# Imports
import_cell = nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set Style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context('talk')""")

# Load Data
load_data_cell = nbf.v4.new_code_cell("""# Load pre-fetched data (see fetch_data.py)
try:
    df = pd.read_pickle("institutional_data.pkl")
    print(f"Loaded {len(df)} daily observations from 1950-2024")
except FileNotFoundError:
    print("Error: institutional_data.pkl not found. Please run fetch_data.py first.")
    
df.head()""")

# Regression Section
reg_intro = nbf.v4.new_markdown_cell("""## 1. Multifactor Regression
We control for Market Risk (Beta), Size (SMB), and Value (HML) to ensure the 'Year 3' effect isn't just a proxy for risk exposure.""")

reg_code = nbf.v4.new_code_cell("""# Define Variables
df['Excess_Ret'] = df['SP500_Ret'] - df['RF']
X = df[['Mkt_RF', 'SMB', 'HML', 'Is_Year3']]
X = sm.add_constant(X)
y = df['Excess_Ret']

# Run OLS with Newey-West (HAC) Robust Errors (Lag=1)
model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 1})
print(model.summary())""")

# Rolling Alpha
rolling_intro = nbf.v4.new_markdown_cell("""## 2. Stability Analysis: Rolling Alpha
Is the alpha structural or episodic? We run a 5-year (1260 day) rolling regression to track the $\gamma$ coefficient over time.""")

rolling_code = nbf.v4.new_code_cell("""# Rolling OLS
rolling = RollingOLS(y, X, window=1260).fit()
rolling_params = rolling.params

# Plot
plt.figure(figsize=(12, 6))
plt.plot(rolling_params.index, rolling_params['Is_Year3'], label='Year 3 Alpha (5Y Rolling)', color='#1f77b4')
plt.axhline(0, color='red', linestyle='--', alpha=0.5)
plt.fill_between(rolling_params.index, rolling_params['Is_Year3'], 0, where=(rolling_params['Is_Year3']>=0), color='green', alpha=0.1)
plt.title('Time-Varying Alpha: Pre-Election Year Coefficient')
plt.ylabel('Alpha Coefficient')
plt.legend()
plt.show()""")

# Bootstrap
boot_intro = nbf.v4.new_markdown_cell("""## 3. Bootstrap Validation
We resample the returns 10,000 times (with replacement) to build a distribution of Sharpe Ratios. This tests if the outperformance is statistically distinguishable from luck.""")

boot_code = nbf.v4.new_code_cell("""year3_rets = df[df['Is_Year3'] == 1]['Excess_Ret']
other_rets = df[df['Is_Year3'] == 0]['Excess_Ret']

n_sims = 10000
diffs = []

print(f"Running {n_sims} bootstrap simulations...")
for _ in range(n_sims):
    # Resample
    s_y3 = year3_rets.sample(n=len(year3_rets), replace=True)
    s_ot = other_rets.sample(n=len(other_rets), replace=True)
    
    # Calc Annualized Sharpe
    sh_y3 = (s_y3.mean() / s_y3.std()) * np.sqrt(252)
    sh_ot = (s_ot.mean() / s_ot.std()) * np.sqrt(252)
    
    diffs.append(sh_y3 - sh_ot)

diffs = np.array(diffs)
p_val = (diffs <= 0).sum() / n_sims

plt.figure(figsize=(10, 6))
sns.histplot(diffs, kde=True, color='purple')
plt.axvline(0, color='red', linestyle='--')
plt.title(f'Bootstrap Distribution (Year 3 Sharpe - Other Sharpe)\\nP-Value: {p_val:.5f}')
plt.xlabel('Sharpe Ratio Difference')
plt.show()

print(f"Bootstrap P-Value: {p_val:.5f}")""")

# Drawdown
dd_intro = nbf.v4.new_markdown_cell("""## 4. Realistic Risk: Drawdown Analysis
Using daily data allows us to see the *true* pain an investor would feel. Annual data masks intra-year crashes.""")

dd_code = nbf.v4.new_code_cell("""# Strategy: Long SP500 in Year 3, Cash (0%) otherwise
# Note: Cash return is simplified to 0 nominal.
df['Strategy_Ret'] = np.where(df['Is_Year3'] == 1, df['SP500_Ret'], 0.0)

# Calculate Curves
df['BuyHold_Curve'] = (1 + df['SP500_Ret']).cumprod()
df['Strategy_Curve'] = (1 + df['Strategy_Ret']).cumprod()

# Calculate Drawdowns
def calc_dd(series):
    peak = series.cummax()
    return (series - peak) / peak

df['BH_DD'] = calc_dd(df['BuyHold_Curve'])
df['Strat_DD'] = calc_dd(df['Strategy_Curve'])

print(f"Max Drawdown (Buy & Hold): {df['BH_DD'].min():.2%}")
print(f"Max Drawdown (Year 3 Only): {df['Strat_DD'].min():.2%}")

# Plot Logs
plt.figure(figsize=(12, 6))
plt.plot(df.index, np.log10(df['BuyHold_Curve']), label='Buy & Hold (Log)', color='gray', alpha=0.5)
plt.plot(df.index, np.log10(df['Strategy_Curve']), label='Year 3 Only (Log)', color='green')
plt.title('Log Equity Curve: 75 Years of Compounding')
plt.ylabel('Log Wealth')
plt.legend()
plt.show()

# Plot Underwater
plt.figure(figsize=(12, 4))
plt.fill_between(df.index, df['Strat_DD'], 0, color='red', alpha=0.3, label='Year 3 Drawdown')
plt.title('Underwater Plot: Year 3 Strategy Risk')
plt.ylabel('Drawdown')
plt.legend()
plt.show()""")

nb.cells = [title_cell, import_cell, load_data_cell, reg_intro, reg_code, rolling_intro, rolling_code, boot_intro, boot_code, dd_intro, dd_code]

with open('Institutional_Research.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook generated: Institutional_Research.ipynb")
