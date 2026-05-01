#!/usr/bin/env python3
"""
XAUUSD Smart Money EA - Backtesting Engine
Personal Use - PUPrime Strategy Testing

Requires: pip install pandas numpy ta mplfinance
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

class SmartMoneyBacktester:
    def __init__(self, data_path: str = None):
        self.data = None
        self.results = []
        self.parameters = {
            'ema200_period': 200,
            'ema50_period': 50,
            'atr_period': 14,
            'atr_sl_multiplier': 1.5,
            'rr_ratio': 2.0,
            'risk_percent': 1.0,
            'wick_body_ratio': 1.5,
            'lookback': 20,
            'session_start': 7,
            'session_end': 20,
            'max_spread': 50
        }
        
    def load_data(self, csv_path: str):
        """Load OHLCV data from CSV"""
        self.data = pd.read_csv(csv_path, parse_dates=['time'])
        self.data.set_index('time', inplace=True)
        self.data.sort_index(inplace=True)
        print(f"Loaded {len(self.data)} bars from {csv_path}")
        
    def calculate_indicators(self):
        """Calculate EMA and ATR indicators"""
        self.data['ema200'] = self.data['close'].ewm(span=self.parameters['ema200_period']).mean()
        self.data['ema50'] = self.data['close'].ewm(span=self.parameters['ema50_period']).mean()
        
        # True Range calculation
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        self.data['atr'] = tr.rolling(window=self.parameters['atr_period']).mean()
        
        # Session filter (hour)
        self.data['hour'] = self.data.index.hour
        self.data['in_session'] = (
            (self.data['hour'] >= self.parameters['session_start']) & 
            (self.data['hour'] <= self.parameters['session_end'])
        )
        
        # Spread simulation (use typical XAUUSD spread)
        self.data['spread'] = 30  # default 30 points
        
    def detect_liquidity_sweep(self, idx: int, direction: str):
        """Detect liquidity sweep pattern"""
        lookback = self.parameters['lookback']
        
        if direction == 'sell':
            # Price near resistance (EMA50 or recent high)
            recent_high = self.data['high'].iloc[idx - lookback:idx].max()
            zone_dist = self.data['atr'].iloc[idx] * 0.5
            price = self.data['close'].iloc[idx]
            
            near_zone = (abs(price - self.data['ema50'].iloc[idx]) < zone_dist or
                        abs(price - recent_high) < zone_dist)
            
            if not near_zone:
                return False
                
            # Sweep: current high breaks recent high
            swept = self.data['high'].iloc[idx] > recent_high
            # Rejected: close below recent high
            rejected = self.data['close'].iloc[idx] < recent_high
            
            # Candle rejection
            body = abs(self.data['close'].iloc[idx] - self.data['open'].iloc[idx])
            wick = self.data['high'].iloc[idx] - max(self.data['open'].iloc[idx], self.data['close'].iloc[idx])
            rejection_candle = wick > body * self.parameters['wick_body_ratio']
            
            # Strong move
            displacement = self.data['open'].iloc[idx] - self.data['close'].iloc[idx]
            strong_move = displacement > 20 * (self.data['close'].iloc[idx] - self.data['close'].iloc[idx-1]) / 100
            
            return swept and rejected and rejection_candle
            
        else:  # buy
            recent_low = self.data['low'].iloc[idx - lookback:idx].min()
            zone_dist = self.data['atr'].iloc[idx] * 0.5
            price = self.data['close'].iloc[idx]
            
            near_zone = (abs(price - self.data['ema50'].iloc[idx]) < zone_dist or
                        abs(price - recent_low) < zone_dist)
            
            if not near_zone:
                return False
                
            swept = self.data['low'].iloc[idx] < recent_low
            rejected = self.data['close'].iloc[idx] > recent_low
            
            body = abs(self.data['close'].iloc[idx] - self.data['open'].iloc[idx])
            wick = min(self.data['open'].iloc[idx], self.data['close'].iloc[idx]) - self.data['low'].iloc[idx]
            rejection_candle = wick > body * self.parameters['wick_body_ratio']
            
            displacement = self.data['close'].iloc[idx] - self.data['open'].iloc[idx]
            strong_move = displacement > 20 * (self.data['close'].iloc[idx] - self.data['close'].iloc[idx-1]) / 100
            
            return swept and rejected and rejection_candle
    
    def run_backtest(self, initial_balance: float = 10000):
        """Run backtest simulation"""
        balance = initial_balance
        position = None
        equity_curve = []
        
        for idx in range(self.parameters['ema200_period'], len(self.data)):
            row = self.data.iloc[idx]
            
            # Check session filter
            if not row['in_session']:
                continue
                
            # Check spread
            if row['spread'] > self.parameters['max_spread']:
                continue
                
            # Determine bias
            bullish = row['close'] > row['ema200']
            bearish = row['close'] < row['ema200']
            
            if position is None:
                # Check for sell signal
                if bearish and self.detect_liquidity_sweep(idx, 'sell'):
                    sl = row['close'] + row['atr'] * self.parameters['atr_sl_multiplier']
                    tp = row['close'] - row['atr'] * self.parameters['atr_sl_multiplier'] * self.parameters['rr_ratio']
                    risk = (sl - row['close']) / row['close'] * 100
                    position = {
                        'type': 'sell',
                        'entry': row['close'],
                        'sl': sl,
                        'tp': tp,
                        'risk': risk,
                        'entry_bar': idx
                    }
                # Check for buy signal
                elif bullish and self.detect_liquidity_sweep(idx, 'buy'):
                    sl = row['close'] - row['atr'] * self.parameters['atr_sl_multiplier']
                    tp = row['close'] + row['atr'] * self.parameters['atr_sl_multiplier'] * self.parameters['rr_ratio']
                    risk = (row['close'] - sl) / row['close'] * 100
                    position = {
                        'type': 'buy',
                        'entry': row['close'],
                        'sl': sl,
                        'tp': tp,
                        'risk': risk,
                        'entry_bar': idx
                    }
            
            elif position:
                # Check for exit
                if position['type'] == 'sell':
                    if row['low'] <= position['tp']:
                        pnl = position['risk'] * self.parameters['rr_ratio']
                        balance *= (1 + pnl/100)
                        self.results.append({'type': 'sell', 'pnl': pnl, 'balance': balance})
                        position = None
                    elif row['high'] >= position['sl']:
                        pnl = -position['risk']
                        balance *= (1 + pnl/100)
                        self.results.append({'type': 'sell', 'pnl': pnl, 'balance': balance})
                        position = None
                else:  # buy
                    if row['high'] >= position['tp']:
                        pnl = position['risk'] * self.parameters['rr_ratio']
                        balance *= (1 + pnl/100)
                        self.results.append({'type': 'buy', 'pnl': pnl, 'balance': balance})
                        position = None
                    elif row['low'] <= position['sl']:
                        pnl = -position['risk']
                        balance *= (1 + pnl/100)
                        self.results.append({'type': 'buy', 'pnl': pnl, 'balance': balance})
                        position = None
            
            equity_curve.append({'time': row.name, 'balance': balance})
        
        return pd.DataFrame(equity_curve), balance
    
    def print_summary(self, final_balance: float, initial_balance: float):
        """Print backtest results summary"""
        results_df = pd.DataFrame(self.results)
        
        print("\n" + "="*60)
        print("BACKTEST RESULTS SUMMARY")
        print("="*60)
        print(f"Initial Balance: ${initial_balance:,.2f}")
        print(f"Final Balance:   ${final_balance:,.2f}")
        print(f"Total Return:    {((final_balance/initial_balance)-1)*100:.2f}%")
        
        if len(results_df) > 0:
            wins = results_df[results_df['pnl'] > 0]
            losses = results_df[results_df['pnl'] < 0]
            print(f"Total Trades:    {len(results_df)}")
            print(f"Win Rate:       {len(wins)/len(results_df)*100:.1f}%")
            print(f"Wins:           {len(wins)}")
            print(f"Losses:         {len(losses)}")
            print(f"Avg Win:        {wins['pnl'].mean():.2f}%")
            print(f"Avg Loss:       {losses['pnl'].mean():.2f}%")
            print(f"Max Drawdown:   {(results_df['balance'].cummax() - results_df['balance']).max():.2f}%")
            
            # Calculate Sharpe ratio
            returns = results_df['pnl']
            sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
            print(f"Sharpe Ratio:   {sharpe:.2f}")
        
        print("="*60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='XAUUSD Smart Money EA Backtester')
    parser.add_argument('--data', '-d', required=True, help='CSV file with OHLCV data')
    parser.add_argument('--balance', '-b', type=float, default=10000, help='Initial balance')
    args = parser.parse_args()
    
    backtester = SmartMoneyBacktester()
    backtester.load_data(args.data)
    backtester.calculate_indicators()
    equity_curve, final_balance = backtester.run_backtest(args.balance)
    backtester.print_summary(final_balance, args.balance)
    
    # Save equity curve
    equity_curve.to_csv('equity_curve.csv', index=False)
    print("\nEquity curve saved to equity_curve.csv")

if __name__ == '__main__':
    main()
