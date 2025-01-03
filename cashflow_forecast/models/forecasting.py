import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import seasonal_decompose

class LendingCashflowModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.seasonal_patterns = None
        
    def preprocess_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess bank statement data"""
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df['net_cashflow'] = df['inflow'] - df['outflow']
        
        monthly_data = df.resample('M', on='date').agg({
            'inflow': 'sum',
            'outflow': 'sum',
            'net_cashflow': 'sum'
        }).reset_index()
        
        return monthly_data

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract relevant features for forecasting"""
        features = pd.DataFrame()
        
        for window in [3, 6, 12]:
            features[f'inflow_ma_{window}'] = df['inflow'].rolling(window=window).mean()
            features[f'outflow_ma_{window}'] = df['outflow'].rolling(window=window).mean()
            features[f'net_ma_{window}'] = df['net_cashflow'].rolling(window=window).mean()
            features[f'inflow_std_{window}'] = df['inflow'].rolling(window=window).std()
            features[f'outflow_std_{window}'] = df['outflow'].rolling(window=window).std()
        
        if len(df) >= 12:
            decomposition = seasonal_decompose(df['net_cashflow'], period=12, extrapolate_trend='freq')
            self.seasonal_patterns = decomposition.seasonal
            features['seasonal'] = decomposition.seasonal
        
        return features

    def calculate_risk_metrics(self, df: pd.DataFrame) -> dict:
        """Calculate key risk metrics"""
        return {
            'operating_cash_flow_ratio': df['net_cashflow'].mean() / df['outflow'].mean(),
            'cash_flow_volatility': df['net_cashflow'].std() / df['net_cashflow'].mean(),
            'negative_months_ratio': (df['net_cashflow'] < 0).mean(),
            'trend_strength': np.corrcoef(range(len(df)), df['net_cashflow'])[0,1],
            'average_monthly_coverage': df['inflow'].mean() / df['outflow'].mean()
        }

    def train_model(self, df: pd.DataFrame, features: pd.DataFrame):
        """Train the forecasting model"""
        X = features.dropna()
        y = df['net_cashflow'].iloc[len(df)-len(X):]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def generate_forecast(self, df: pd.DataFrame, features: pd.DataFrame, months: int = 12) -> pd.Series:
        """Generate cash flow forecasts"""
        forecasts = []
        current_features = features.iloc[-1:]
        
        for _ in range(months):
            scaled_features = self.scaler.transform(current_features)
            prediction = self.model.predict(scaled_features)[0]
            
            if self.seasonal_patterns is not None:
                prediction += self.seasonal_patterns[len(forecasts) % len(self.seasonal_patterns)]
            
            forecasts.append(prediction)
            current_features = self._update_features(current_features, prediction)
        
        return pd.Series(forecasts)

    def calculate_stress_scenarios(self, baseline_forecast: pd.Series) -> dict:
        """Generate stress test scenarios"""
        return {
            'baseline': baseline_forecast,
            'pessimistic': baseline_forecast * 0.8,  # 20% reduction
            'optimistic': baseline_forecast * 1.2,   # 20% increase
            'severe_stress': baseline_forecast * 0.6  # 40% reduction
        }

    def _update_features(self, features: pd.DataFrame, new_prediction: float) -> pd.DataFrame:
        """Update features for the next prediction"""
        updated = features.copy()
        
        for window in [3, 6, 12]:
            updated[f'net_ma_{window}'] = (features[f'net_ma_{window}'] * (window-1) + new_prediction) / window
        
        return updated