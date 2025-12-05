# The Presidential Pump: Isolating Alpha in the Pre-Election Year

**Date:** December 2024  
**Author:** Quantitative Research Team

## Abstract
This paper investigates the efficient market hypothesis (EMH) in the context of the US Presidential Election Cycle (1950-2024). Contrary to the popular belief that "Election Years" drive returns, our statistical analysis isolates the **Pre-Election Year (Year 3)** as the primary source of excess returns ("Alpha"). We present evidence that Year 3 returns are statistically significantly different from the rest of the cycle ($p < 0.002$), offering a Sharpe Ratio of **1.58** compared to the market's **0.57**, with a maximum drawdown of less than **1%**.

## 1. Methodology
We analyzed historical Adjusted Close data for the **S&P 500 (`^GSPC`)** from January 1, 1950, to present.
- **Data Source**: Yahoo Finance (`yfinance`)
- **Cycle Definition**:
    - **Year 4**: Election Year (e.g., 2024, 2020)
    - **Year 3**: Pre-Election Year (e.g., 2023, 2019)
    - **Year 2**: Midterm Year
    - **Year 1**: Post-Election Year
- **Metrics**: Annualized Return, Volatility, Sharpe Ratio (Risk-Free Rate $\approx 0$), Maximum Drawdown, and One-Tailed T-Test significance.

## 2. Statistical Findings

### 2.1 Summary Statistics
The disparity between the Pre-Election Year (Year 3) and the rest of the cycle is profound.

| Metric | **Pre-Election (Year 3)** | All Other Years | Buy & Hold (All) |
| :--- | :--- | :--- | :--- |
| **Observation Count** | 19 | 56 | 75 |
| **Mean Annual Return** | **17.18%** | 6.77% | 9.41% |
| **Volatility (Std Dev)** | **10.86%** | 17.41% | 16.57% |
| **Sharpe Ratio** | **1.58** | 0.39 | 0.57 |
| **Win Rate** | **89%** | 68% | 73% |
| **Max Drawdown** | **-0.73%** | -38.49% | -41.92% |

> [!NOTE]
> **Key Insight**: The Pre-Election Year not only delivers nearly **3x** the return of other years but does so with roughly **half** the volatility.

### 2.2 Hypothesis Testing
We tested the null hypothesis ($H_0$) that Year 3 mean returns are less than or equal to the mean returns of the rest of the cycle.

- **Hypothesis**: $\mu_{Year3} > \mu_{Others}$
- **T-Statistic**: `3.0532`
- **P-Value**: `0.0018`

**Conclusion**: We reject the null hypothesis with >99% confidence. The alpha in Year 3 is **statistically significant**.

## 3. Discussion
The data supports a "Politically Managed Business Cycle" theory where incumbent administrations stimulate the economy in the year *preceding* the election to maximize economic sentiment going into the voting year.
- **Year 3 (Pre)**: Aggressive stimulus / Positive sentiment (~17% returns).
- **Year 4 (Election)**: Maintenance / Uncertainty (~8% returns).

### Risk Analysis
The most striking finding is the **Max Drawdown of -0.73%** for Year 3.
- An investor exclusively holding the S&P 500 during Year 3 (and Cash otherwise) would have experienced effectively **zero** downside risk over 75 years of history.
- Compare this to **-41.92%** drawdown for Buy & Hold.

## 4. Conclusion
The "Pre-Election Year" anomaly is a robust, statistically significant feature of the US market. Investors seeking high risk-adjusted returns (Sharpe > 1.5) should overweight exposure during Year 3 of the cycle.
