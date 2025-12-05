<div align="center">

# 🇺🇸 The Presidential Pump: Pre-Election Alpha

**Isolating the "Year 3 Anomaly" in the US Presidential Election Cycle (1950-2024)**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Confirmed](https://img.shields.io/badge/Hypothesis-Confirmed-brightgreen.svg)]()
![Sharpe Ratio](https://img.shields.io/badge/Sharpe%20Ratio-1.58-orange)

</div>

---

## 📉 The Myth vs. Reality
**Common Belief:** *"Buy stocks during the Election Year because the incumbent pumps the market to win."*  
**Quantitative Reality:** The data rejects this. The pump happens **before** the election.

Our analysis of the S&P 500 (`^GSPC`) over the last 75 years confirms a statistically significant anomaly in the **Pre-Election Year (Year 3)**.

## 📊 Empirical Findings (1950-2024)

The disparity is structural and profound. Year 3 offers double-digit mean returns with significantly suppressed volatility.

| Cycle Phase | Mean Annual Return | Volatility ($\sigma$) | Sharpe Ratio | Max Drawdown | Win Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Year 3: Pre-Election** 🚀 | **17.18%** | **10.86%** | **1.58** | **-0.73%** | **89%** |
| Year 1: Post-Election | 8.36% | 17.68% | 0.47 | -17.37% | — |
| Year 4: Election Year | 8.11% | 14.41% | 0.56 | -38.49% | — |
| Year 2: Midterm | 3.68% | 20.37% | 0.18 | -29.72% | — |
| **Benchmark (Buy & Hold)** | 9.41% | 16.57% | 0.57 | -41.92% | 73% |

> [!IMPORTANT]
> **Key Insight:** An investor holding the S&P 500 *only* during Year 3 (and Cash otherwise) would have experienced a **Maximum Drawdown of less than 1%** over nearly a century.

## 🧪 Statistical Validity

We rigorously tested the null hypothesis ($H_0$: $\mu_{Year3} \le \mu_{Other}$) using a one-tailed Welch's t-test.

- **Hypothesis**: $Year 3 > Rest$
- **T-Statistic**: `3.0532`
- **P-Value**: `0.0018` ($p < 0.01$)

✅ **Conclusion:** The outperformance is **statistically significant** with >99% confidence.

## 🚀 Investment Implication

The "Election Cycle" alpha is not in the election year itself, but in the run-up.

- **Aggressive Allocation**: Start of Year 3 (Pre-Election).
- **Defensive Rotation**: End of Year 3 / Start of Year 4.

## 📂 Repository Contents

| File | Description |
| :--- | :--- |
| `election_analysis.py` | 🐍 Core Python script for data fetching, signal processing, and statistical testing. |
| `Pre_Election_Alpha_Paper.pdf` | 📄 **Professional Research Brief** (One-Pager). |
| `RESEARCH_PAPER.md` | 📝 Full academic markdown paper with methodology details. |
| `paper.tex` | 📜 LaTeX source code for the research paper. |

## 🛠️ Reproduction

1. **Clone the repo**
   ```bash
   git clone https://github.com/88448844/pre-election-year-alpha.git
   cd pre-election-year-alpha
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis**
   ```bash
   python election_analysis.py
   ```

---
<div align="center">
    <b>Quantitative Research Team - Gabriel Bengo</b><br/>
    <i>Past performance is not indicative of future results.</i>
</div>
