# DeFi Wallet Credit Score Analysis

## Score Distribution Overview 

```mermaid
pie title Credit Score Distribution
    "900-1000 (Elite)": 5
    "800-899 (Excellent)": 2
    "700-799 (Very Good)": 15
    "600-699 (Good)": 240
    "500-599 (Fair)": 2498
    "400-499 (Below Average)": 704
    "300-399 (Risky)": 30
    "200-299 (High Risk)": 3
    "100-199 (Very High Risk)": 0
    "0-99 (Extreme Risk)": 0

xychart-beta
    title "Wallet Count by Score Range"
    x-axis "Score Range" [0-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 800-899, 900-1000]
    y-axis "Number of Wallets" 0-->2500
    bar [0, 0, 3, 30, 704, 2498, 240, 15, 2, 5]

pie title Risk Category Breakdown
    showData
    "Low Risk (600-1000)": 262
    "Medium Risk (400-599)": 3202
    "High Risk (0-399)": 33