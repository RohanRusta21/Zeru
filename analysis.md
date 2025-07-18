# DeFi Wallet Credit Score Analysis

## Score Distribution Overview 

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'pie1': '#ff9999', 'pie2': '#66b3ff', 'pie3': '#99ff99'}}}%%
graph TD
    subgraph "Credit Score Distribution (3500 Wallets)"
        A[Pie Chart] -->|900-1000| A1["5 (0.1%)"]
        A -->|800-899| A2["2 (0.06%)"]
        A -->|700-799| A3["15 (0.4%)"]
        A -->|600-699| A4["240 (6.9%)"]
        A -->|500-599| A5["2498 (71.4%)"]
        A -->|400-499| A6["704 (20.1%)"]
        A -->|300-399| A7["30 (0.9%)"]
        A -->|200-299| A8["3 (0.09%)"]
    end

    subgraph "Wallet Count by Range"
        B[Bar Chart] --> B1["0-99: 0"]
        B --> B2["100-199: 0"]
        B --> B3["200-299: 3"]
        B --> B4["300-399: 30"]
        B --> B5["400-499: 704"]
        B --> B6["500-599: 2498"]
        B --> B7["600-699: 240"]
        B --> B8["700-799: 15"]
        B --> B9["800-899: 2"]
        B --> B10["900-1000: 5"]
    end

    subgraph "Risk Categories"
        C[Donut Chart] --> C1["Low Risk (600-1000): 262"]
        C --> C2["Medium Risk (400-599): 3202"]
        C --> C3["High Risk (0-399): 36"]
    end
   