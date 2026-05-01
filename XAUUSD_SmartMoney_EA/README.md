# XAUUSD Smart Money EA - PUPrime MT5

## Overview
A bidirectional MT5 Expert Advisor implementing a **smart money liquidity sweep strategy** for XAUUSD trading on PUPrime broker.

## Strategy Components
- **Trend Bias**: 200 EMA (M15) for direction
- **Entry Trigger**: Liquidity sweep detection (break of highs/lows → rejection)
- **Confirmation**: Rejection candle (wick > body × 1.5) + strong displacement
- **Risk Management**: ATR-based stops, 2:1 RR, 1% risk per trade
- **Filters**: Session filter (07:00-20:00 UTC), spread cap (50 points)

## Files
```
├── XAUUSD_SmartMoney_EA.mq5   # Main EA file
├── backtest/
│   └── backtest_engine.py      # Python backtesting engine
├── config/
│   └── default.set             # MT5 strategy tester settings
└── docs/
    └── strategy_notes.md       # Detailed strategy documentation
```

## Installation
1. Copy `XAUUSD_SmartMoney_EA.mq5` to MT5 data folder
   - Path: `MQL5/Experts/`
2. Open MT5 → Navigator → Experts → drag onto chart
3. Configure inputs or use default settings

## Default Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| RiskPercent | 1.0% | Risk per trade |
| ATR_Multiplier | 1.5 | Stop loss distance |
| RR_Ratio | 2.0 | Reward:Risk |
| ATR_Period | 14 | ATR calculation period |
| HTF_Period | M15 | Higher timeframe for bias |
| LTF_Period | M5 | Lower timeframe for execution |
| LiquidityLookback | 20 | Candles to detect sweep |

## Supported Symbol
- **XAUUSD** (Gold vs US Dollar) on PUPrime

## Risk Warning
This EA is for **personal use** and is provided as-is. Always backtest before live trading.
