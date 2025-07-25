import requests
import pandas as pd
import numpy as np
from web3 import Web3
from datetime import datetime

# Initialize Web3 (replace with your own provider)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9f763041364a4897a7e3723ca4b5a937'))

# Compound V2/V3 contract addresses
COMPOUND_V2_COMPTROLLER = "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"
COMPOUND_V3_MAINNET = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"

# Load wallet addresses
wallet_df = pd.read_csv('Wallet_id.csv')
wallets = wallet_df['wallet_id'].tolist()

def get_compound_transactions(wallet_address):
    """Fetch Compound transactions for a wallet using Etherscan API"""
    api_key = "P8M42CPNIBCRX5E7Y4CRRJ615UJZJGM4JJ"
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == '1':
            return data['result']
        return []
    except Exception as e:
        print(f"Error fetching transactions for {wallet_address}: {e}")
        return []

def analyze_transactions(transactions):
    """Analyze transactions to extract risk features"""
    features = {
        'total_txs': 0,
        'compound_txs': 0,
        'liquidations': 0,
        'borrow_operations': 0,
        'repay_operations': 0,
        'supply_operations': 0,
        'withdraw_operations': 0,
        'high_value_txs': 0,  # Txs > 10 ETH value
        'recent_activity': 0,  # Txs in last 30 days
        'interaction_frequency': 0  # Txs per day
    }
    
    if not transactions:
        return features
    
    first_tx_time = datetime.fromtimestamp(int(transactions[0]['timeStamp']))
    last_tx_time = datetime.fromtimestamp(int(transactions[-1]['timeStamp']))
    days_active = (last_tx_time - first_tx_time).days or 1
    
    for tx in transactions:
        features['total_txs'] += 1
        
        # Check if tx is with Compound contracts
        if tx['to'].lower() in [COMPOUND_V2_COMPTROLLER.lower(), COMPOUND_V3_MAINNET.lower()]:
            features['compound_txs'] += 1
            
            # Check for liquidation events (simplified)
            if '0xea456d90' in tx['input'].lower():  # LiquidateBorrow function signature
                features['liquidations'] += 1
            elif '0xc5ebea7' in tx['input'].lower():  # Borrow function
                features['borrow_operations'] += 1
            elif '0x1e9b8b' in tx['input'].lower():  # Repay function
                features['repay_operations'] += 1
        
        # Check tx value (convert from wei to ETH)
        tx_value = float(tx['value']) / 1e18
        if tx_value > 10:
            features['high_value_txs'] += 1
            
        # Check recent activity (last 30 days)
        tx_time = datetime.fromtimestamp(int(tx['timeStamp']))
        if (datetime.now() - tx_time).days <= 30:
            features['recent_activity'] += 1
    
    features['interaction_frequency'] = features['total_txs'] / days_active
    return features

def calculate_risk_score(features):
    """Calculate risk score (0-1000) based on transaction features"""
    weights = {
        'liquidations': 300,
        'borrow_operations': 150,
        'high_value_txs': 100,
        'interaction_frequency': 200,
        'recent_activity': 150,
        'compound_tx_ratio': 100  # Compound txs / total txs
    }
    
    # Calculate compound transaction ratio
    if features['total_txs'] > 0:
        compound_ratio = features['compound_txs'] / features['total_txs']
    else:
        compound_ratio = 0
    
    # Calculate weighted score
    score = (
        features['liquidations'] * weights['liquidations'] +
        features['borrow_operations'] * weights['borrow_operations'] +
        features['high_value_txs'] * weights['high_value_txs'] +
        min(features['interaction_frequency'], 10) * weights['interaction_frequency'] +
        min(features['recent_activity'], 20) * weights['recent_activity'] +
        compound_ratio * weights['compound_tx_ratio']
    )
    
    # Normalize to 0-1000 range
    return min(int(score), 1000)

def process_wallets(wallet_list):
    """Process list of wallets and return risk scores"""
    results = []
    
    for wallet in wallet_list:
        print(f"Processing wallet: {wallet}")
        txs = get_compound_transactions(wallet)
        features = analyze_transactions(txs)
        risk_score = calculate_risk_score(features)
        
        results.append({
            'wallet_id': wallet,
            'score': risk_score,
        })
    
    return pd.DataFrame(results)

# Process all wallets
risk_scores_df = process_wallets(wallets) 

# Save results
risk_scores_df.to_csv('wallet_risk_scores.csv', index=False)
print(risk_scores_df[['wallet_address', 'risk_score']])