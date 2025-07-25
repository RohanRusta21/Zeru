# Wallet Risk Scoring Framework for Compound Protocol

![DeFi Risk Analysis](https://img.shields.io/badge/DeFi-Risk_Analysis-blue)
![Compound Protocol](https://img.shields.io/badge/Protocol-Compound_V2%2FV3-green)
![Scoring Scale](https://img.shields.io/badge/Scoring-0_to_1000-orange)

A data-driven framework to assess wallet risk exposure in Compound Finance's lending/borrowing protocols.

## Table of Contents
- [Features](#features)
- [Methodology](#methodology)
- [Risk Indicators](#risk-indicators)


## Features
✔ **Comprehensive Risk Scoring** (0-1000 scale)  
✔ **Multi-Source Data Collection** (Etherscan, Subgraph, Web3)  
✔ **Weighted Risk Indicators** (Liquidations, Borrowing, Collateral, etc.)  
✔ **Scalable Architecture** (Batch processing, caching)  
✔ **Validation Framework** (Historical backtesting)  

## Methodology
### Data Collection
- **Primary Sources:**
  - Ethereum blockchain via Etherscan API/Web3
  - Compound Subgraph (The Graph protocol)
- **Secondary Verification:**
  - DeFi Llama/Risk APIs
  - On-chain analytics tools

### Scoring Formula
Risk Score =
(Liquidation Score × 0.30) +
(Borrowing Score × 0.20) +
(Collateral Score × 0.15) +
(Health Factor Score × 0.15) +
(Transaction Velocity Score × 0.10) +
(Cross-Protocol Score × 0.10)

## Risk Indicators
| Indicator               | Weight | Description                          |
|-------------------------|--------|--------------------------------------|
| Liquidations            | 30%    | Count of `LiquidateBorrow` events    |
| Borrow Frequency        | 20%    | Leverage risk assessment             |
| Collateral Diversity    | 15%    | Herfindahl index of assets           |
| Health Factor Trends    | 15%    | Proximity to liquidation             |
| Transaction Velocity    | 10%    | Activity pattern analysis            |
| Cross-Protocol Exposure | 10%    | External DeFi risk                   |


