import json
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class DeFiCreditScorer:
    def __init__(self):
        self.iso_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.feature_weights = {
            'tx_count': 0.15,
            'unique_assets': 0.15,
            'avg_amount_usd': 0.1,
            'deposit_ratio': 0.2,
            'liquidation_ratio': -0.3,
            'time_variability': -0.1,
            'anomaly_score': -0.3
        }
    
    def preprocess_data(self, data):
        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        amounts = df['actionData'].apply(lambda x: float(x['amount']))
        prices = df['actionData'].apply(lambda x: float(x['assetPriceUSD']))
        df['amount_usd'] = amounts * prices
        
        wallet_features = []
        for wallet, group in df.groupby('userWallet'):
            features = {
                'wallet': wallet,
                'tx_count': len(group),
                'unique_assets': group['actionData'].apply(lambda x: x['assetSymbol']).nunique(),
                'avg_amount_usd': group['amount_usd'].mean(),
                'deposit_ratio': (group['action'] == 'deposit').mean(),
                'borrow_ratio': (group['action'] == 'borrow').mean(),
                'liquidation_ratio': (group['action'] == 'liquidationcall').mean(),
                'time_variability': group['datetime'].diff().dt.total_seconds().std()
            }
            wallet_features.append(features)
        return pd.DataFrame(wallet_features)
    
    def compute_anomaly_scores(self, features_df):
        features_df = features_df.fillna({
            'avg_amount_usd': 0,
            'deposit_ratio': 0,
            'borrow_ratio': 0,
            'liquidation_ratio': 0,
            'time_variability': 0
        })
        X = features_df[['tx_count', 'unique_assets', 'avg_amount_usd','deposit_ratio', 'borrow_ratio', 'time_variability']]
        self.iso_forest.fit(X)
        features_df['anomaly_score'] = self.iso_forest.decision_function(X)
        return features_df
    
    def calculate_credit_scores(self, features_df):
        for col in ['tx_count', 'unique_assets', 'avg_amount_usd', 'time_variability']:
            features_df[col] = self.scaler.fit_transform(features_df[[col]])
        weighted_scores = []
        for _, row in features_df.iterrows():
            score = 0
            for feature, weight in self.feature_weights.items():
                score += row[feature] * weight
            normalized_score = 1 / (1 + np.exp(-score))
            credit_score = int(normalized_score * 1000)
            weighted_scores.append(credit_score)
        features_df['credit_score'] = weighted_scores
        return features_df
    
    def get_score_ranges(self, scores):
        bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        labels = ['0-99', '100-199', '200-299', '300-399', '400-499', 
                 '500-599', '600-699', '700-799', '800-899', '900-1000']
        score_df = pd.DataFrame({'wallet': list(scores.keys()), 'score': list(scores.values())})
        score_df['range'] = pd.cut(score_df['score'], bins=bins, labels=labels, right=False)
        return score_df['range'].value_counts().sort_index()
    
    def score_wallets(self, json_data):
        data = json.loads(json_data)
        features_df = self.preprocess_data(data)
        features_df = self.compute_anomaly_scores(features_df)
        features_df = self.calculate_credit_scores(features_df)
        scores = dict(zip(features_df['wallet'], features_df['credit_score']))
        return scores

if __name__ == "__main__":
    with open('user-wallet-transactions.json', 'r') as f:
        json_data = f.read()
    scorer = DeFiCreditScorer()
    scores = scorer.score_wallets(json_data)
    
    range_counts = scorer.get_score_ranges(scores)
    print("\nWallet Count by Score Range:")
    print(range_counts.to_string())
    
    print("\nIndividual Wallet Scores:")
    print(json.dumps(scores, indent=2))