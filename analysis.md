# DeFi Wallet Credit Score Analysis

## Score Distribution Overview 

```mermaid
pie title Credit Score Distribution
    "Range with count of Credit Score"
    "900-1000 (Elite) = 5": 5
    "800-899 (Excellent) = 2": 2
    "700-799 (Very Good) = 15": 15
    "600-699 (Good) = 240": 240
    "500-599 (Fair) = 2498": 2498
    "400-499 (Below Average) = 704": 704
    "300-399 (Risky) = 30": 30
    "200-299 (High Risk) = 3": 3
    "100-199 (Very High Risk) = 0": 0
    "0-99 (Extreme Risk) = 0": 0

```

```mermaid

xychart-beta
    title "Wallet Count by Score Range"
    x-axis "Score Range" [0-99, 100-199, 200-299, 300-399, 400-499, 500-599, 600-699, 700-799, 800-899, 900-1000]
    y-axis "Number of Wallets" 0-->2600
    bar [0, 0, 3, 30, 704, 2498, 240, 15, 2, 5]
```
```mermaid
xychart-beta
    title "Cumulative % of Wallets by Score (3500 Wallets Total)"
    x-axis "Credit Score" [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    y-axis "% of Wallets" 0-->100
    line [0, 0, 0.09, 0.94, 21.1, 92.5, 99.4, 99.9, 100, 100, 100]