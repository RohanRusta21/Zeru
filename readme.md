# DeFi Credit Scoring System

## Overview
This system implements a credit scoring mechanism for DeFi wallets based on transaction history analysis using a hybrid anomaly detection and weighted feature scoring approach.

## Table of Contents
- [Methodology](#methodology)
- [System Architecture](#system-architecture)
- [Processing Flow](#processing-flow)

## Methodology

### Hybrid Approach
Combines two techniques:
1. **Isolation Forest Anomaly Detection**
   - Identifies unusual transaction patterns
   - Generates anomaly scores for each wallet

2. **Weighted Feature Scoring**
   - Combines 7 key transaction features
   - Uses domain-informed weights
   - Normalizes to 0-1000 credit score range

### Why This Approach?
- Handles complex DeFi transaction patterns
- Balances statistical robustness with interpretability
- Adaptable to different DeFi protocols

## System Architecture

### Components
| Component | Purpose | Key Technologies |
|-----------|---------|------------------|
| Data Preprocessor | Parses raw JSON, extracts features | Pandas, Datetime |
| Anomaly Detector | Identifies suspicious wallets | Scikit-Learn IsolationForest |
| Credit Scorer | Calculates final scores | StandardScaler, Sigmoid |

### Feature Weights
| Feature | Weight | Impact |
|---------|--------|--------|
| tx_count | 0.15 | Positive |
| unique_assets | 0.15 | Positive |
| avg_amount_usd | 0.1 | Positive |
| deposit_ratio | 0.2 | Positive |
| liquidation_ratio | -0.3 | Negative |
| time_variability | -0.1 | Negative |
| anomaly_score | -0.3 | Negative |

## Processing Flow

```mermaid
graph LR
    A[JSON Input] --> B[Preprocessing]
    B --> C[Feature Extraction]
    C --> D[Anomaly Scoring]
    D --> E[Normalization]
    E --> F[Weighted Combination]
    F --> G[Credit Scores]