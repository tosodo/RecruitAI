# Quick Reference - XAUUSD Smart Money EA

## Installation
1. Copy `XAUUSD_SmartMoney_EA.mq5` to `MQL5/Experts/` folder
2. Restart MT5 or refresh experts list
3. Drag EA onto XAUUSD M5 chart

## Key Input Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| RiskPercent | 1.0 | Risk per trade as % of balance |
| ATR_Multiplier | 1.5 | Stop loss = Entry ± ATR × 1.5 |
| RR_Ratio | 2.0 | Take profit = 2× risk |
| MaxSpread | 50 | Skip trades if spread > 50 |
| SessionStart/End | 7-20 | Trading hours (UTC) |

## Strategy Flow

```
Trend Check (M15 200 EMA)
    ↓
Bias Bearish? → Look for SELL
Bias Bullish? → Look for BUY
    ↓
Price near EMA50 or Structure?
    ↓
Liquidity Sweep? (breaks high/low)
    ↓
Rejection Candle? (wick > body × 1.5)
    ↓
Execute Trade
    ↓
SL: Entry + 1.5× ATR
TP: Entry - 2× risk
```

## Entry Conditions

### SELL (Short)
- Price below 200 EMA (M15)
- Price rallies to EMA50 or recent high
- Breaks above previous high (sweeps buy stops)
- Closes below that high
- Rejection wick > body × 1.5

### BUY (Long)
- Price above 200 EMA (M15)
- Price drops to EMA50 or recent low
- Breaks below previous low (sweeps sell stops)
- Closes above that low
- Rejection wick > body × 1.5

## Risk Management
- **Max Risk**: 1% per trade
- **Stop Loss**: ATR-based (dynamic)
- **Take Profit**: 2:1 Reward:Risk
- **Break-even**: Moves to entry at 1R profit
- **No Martingale** - fixed risk per trade

## Best Trading Hours (UTC)
| Session | Hours | Notes |
|---------|-------|-------|
| London | 07:00-10:00 | High liquidity, best for sweeps |
| NY Open | 13:00-15:00 | High volatility, secondary |
| Overlap | 13:00-17:00 | Highest liquidity |

## Avoid Trading During
- Major news events (NFP, FOMC, CPI)
- Weekend gaps
- Low volatility Asian session

## Testing the EA
1. Open MT5 Strategy Tester
2. Select: XAUUSD, M5, Last 2 years
3. Model: Every tick (or 1-minute OHLC for speed)
4. Set initial deposit: $10,000
5. Run and analyze equity curve

## Common Issues & Solutions

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| No trades | Spread too high | Check MaxSpread setting |
| No trades | Outside session | Verify SessionStart/End |
| No trades | Not in trend | Wait for 200 EMA bias |
| Many losses | Sideways market | Add session filter |
| Orders rejected | Broker GMT offset | Adjust session hours |
