# XAUUSD Smart Money Trading System - Strategy Notes

## Concept

The strategy is based on **smart money liquidity detection** - identifying where institutional players trap retail traders by taking out buy-stops (above highs) or sell-stops (below lows), then fade the move.

## Core Logic

### Entry Philosophy
> "When price takes liquidity above a key level and fails to hold — that's where smart money sells."

## Components

### 1. Trend Bias (HTF)
- **200 EMA on M15** determines directional bias
- Price above EMA → bullish bias → look for buy setups
- Price below EMA → bearish bias → look for sell setups

### 2. Liquidity Sweep Detection

#### SELL Setup (Buy-side Liquidity Grab)
1. Price breaks **above previous high** (takes buy stops)
2. Candle **closes back below** that high
3. **Rejection candle** forms (upper wick > body × 1.5)
4. Price is near resistance (EMA50 or recent structure)
5. **Bias is bearish** (price below 200 EMA)

#### BUY Setup (Sell-side Liquidity Grab)
1. Price breaks **below previous low** (takes sell stops)
2. Candle **closes back above** that low
3. **Rejection candle** forms (lower wick > body × 1.5)
4. Price is near support (EMA50 or recent structure)
5. **Bias is bullish** (price above 200 EMA)

### 3. Confirmation Filters
- Session filter: 07:00-20:00 UTC (London + NY overlap)
- Spread filter: Max 50 points
- Displacement filter: Strong move confirmation (> 20 points)

### 4. Risk Management
- **Stop Loss**: 1.5 × ATR from entry
- **Take Profit**: 2.0 × risk (2:1 RR)
- **Position Sizing**: 1% risk per trade
- **Break-even**: Move to entry when 1R achieved
- **Trailing Stop**: Optional (starts at 2R, trails at 0.5× ATR)

## Why This Works

| Element | Retail Behavior | Smart Money Behavior |
|---------|-----------------|---------------------|
| Break of high | Buy breakout | Sell into liquidity |
| Break of low | Sell breakdown | Buy into liquidity |
| Rejection | Ignore / average down | Add to position |
| Result | Trapped | Profits |

## Timeframe Rationale

- **M15**: Trend direction (smoother, less noise)
- **M5**: Entry timing (precise, avoids false signals)

## Expected Performance

Based on the strategy logic:
- Win rate target: 40-50%
- Average RR: 2:1
- Best sessions: London + NY overlap
- Worst conditions: Low volatility, news events

## Limitations

1. Cannot detect **true order book** - only price action proxies
2. **News events** can override technical logic
3. **Gaps** on weekends can trigger false signals
4. Requires **liquid market** - may not work on exotic pairs

## Evolving the Strategy

### Level 2 Enhancements
- Multi-sweep detection (equal highs/lows pools)
- Volume confirmation (increased vol = institutional)
- Session-specific parameters (London vs NY)

### Level 3 Enhancements
- Machine learning for sweep quality classification
- Correlation with USD news calendar
- Multi-timeframe confluence (Weekly/Daily bias)

## Files Structure

```
XAUUSD_SmartMoney_EA/
├── XAUUSD_SmartMoney_EA.mq5     # MT5 Expert Advisor
├── backtest_engine.py           # Python backtester
├── default.set                   # MT5 strategy tester preset
├── README.md                    # Quick start guide
└── docs/
    └── strategy_notes.md        # This file
```
