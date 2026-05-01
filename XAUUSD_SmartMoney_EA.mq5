//+------------------------------------------------------------------+
//|                                          XAUUSD Smart Money EA   |
//|                                    Personal Use - PUPrime MT5    |
//+------------------------------------------------------------------+
#property copyright "Smart Money Trading System"
#property version   "1.00"
#property strict

//+------------------------------------------------------------------+
//| INPUTS - Risk & Money Management                                 |
//+------------------------------------------------------------------+
input group "=== Risk Settings ==="
input double   RiskPercent        = 1.0;        // Risk per trade (%)
input int      MaxSpread          = 50;         // Max spread (points)
input double   ATR_Multiplier     = 1.5;        // SL distance in ATR units
input double   RR_Ratio           = 2.0;        // Reward:Risk ratio
input int      ATR_Period         = 14;         // ATR period

input group "=== Time Filter ==="
input bool     UseSessionFilter   = true;       // Use trading session filter
input int      SessionStartHour   = 7;          // Session start hour (UTC)
input int      SessionEndHour     = 20;         // Session end hour (UTC)

input group "=== Indicator Settings ==="
input int      EMA200_Period      = 200;        // 200 EMA period
input int      EMA50_Period       = 50;         // 50 EMA period
input int      HTF_Period         = PERIOD_M15; // Higher timeframe for bias
input int      LTF_Period         = PERIOD_M5;  // Lower timeframe for execution
input int      LiquidityLookback  = 20;         // Candles to look back for liquidity

input group "=== Trade Management ==="
input bool     UseBreakEven       = true;       // Move SL to break-even
input double   BreakEvenAtRR      = 1.0;        // Move BE when RR reached
input bool     UseTrailingStop    = false;      // Use trailing stop
input double   TrailTriggerRR     = 2.0;        // Start trailing after RR
input double   TrailDistance      = 0.5;        // Trail distance in ATR

input group "=== Filters ==="
input bool     RequireRejection   = true;       // Require rejection candle
input double   MinWickBodyRatio   = 1.5;        // Minimum wick to body ratio
input bool     CloseOnOpposite    = true;       // Close on opposite signal

//+------------------------------------------------------------------+
//| Global Variables                                                  |
//+------------------------------------------------------------------+
int ema200Handle, ema50Handle, atrHandle;
double ema200[], ema50[], atr[];
datetime lastTradeTime = 0;
int slippage = 5;

//+------------------------------------------------------------------+
//| Expert Initialization                                             |
//+------------------------------------------------------------------+
int OnInit()
{
   ema200Handle = iMA(_Symbol, HTF_Period, EMA200_Period, 0, MODE_EMA, PRICE_CLOSE);
   ema50Handle  = iMA(_Symbol, LTF_Period, EMA50_Period, 0, MODE_EMA, PRICE_CLOSE);
   atrHandle    = iATR(_Symbol, LTF_Period, ATR_Period);
   
   if(ema200Handle == INVALID_HANDLE || ema50Handle == INVALID_HANDLE || atrHandle == INVALID_HANDLE)
   {
      Print("Failed to create indicator handles!");
      return(INIT_FAILED);
   }
   
   ArraySetAsSeries(ema200, true);
   ArraySetAsSeries(ema50, true);
   ArraySetAsSeries(atr, true);
   
   Print("XAUUSD Smart Money EA Initialized");
   Print("Broker: PUPrime | Symbol: ", _Symbol);
   Print("Risk: ", DoubleToString(RiskPercent, 2), "% | RR: ", DoubleToString(RR_Ratio, 1));
   
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert Deinitialization                                          |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   if(ema200Handle != INVALID_HANDLE) IndicatorRelease(ema200Handle);
   if(ema50Handle  != INVALID_HANDLE) IndicatorRelease(ema50Handle);
   if(atrHandle    != INVALID_HANDLE) IndicatorRelease(atrHandle);
   
   Print("EA Deinitialized. Reason: ", reason);
}

//+------------------------------------------------------------------+
//| Expert Tick Function                                              |
//+------------------------------------------------------------------+
void OnTick()
{
   ManagePositions();
   
   if(!IsNewBar()) return;
   
   if(UseSessionFilter && !IsInTradingSession()) return;
   if(!IsSpreadAcceptable()) return;
   if(PositionsTotal() > 0) return;
   
   if(!CopyIndicators()) return;
   
   double price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   bool bullishBias = price > ema200[0];
   bool bearishBias = price < ema200[0];
   
   bool sellSignal = DetectSellSetup(bearishBias, price);
   bool buySignal  = DetectBuySetup(bullishBias, price);
   
   if(sellSignal)
      ExecuteSell(price);
   else if(buySignal)
      ExecuteBuy(price);
}

//+------------------------------------------------------------------+
//| Detect SELL Setup (Buy-side Liquidity Sweep)                     |
//+------------------------------------------------------------------+
bool DetectSellSetup(bool bearishBias, double price)
{
   if(!bearishBias) return false;
   
   double prevHigh = iHigh(_Symbol, LTF_Period, 
      iHighest(_Symbol, LTF_Period, MODE_HIGH, LiquidityLookback, 2));
   
   double zoneDistance = atr[0] * 0.5;
   bool nearResistance = (MathAbs(price - ema50[0]) < zoneDistance) ||
                         (MathAbs(price - prevHigh) < zoneDistance);
   
   if(!nearResistance) return false;
   
   double high1  = iHigh(_Symbol, LTF_Period, 1);
   double close1 = iClose(_Symbol, LTF_Period, 1);
   double open1  = iOpen(_Symbol, LTF_Period, 1);
   
   bool sweptHigh      = high1 > prevHigh;
   bool failedBreakout = close1 < prevHigh;
   
   bool rejection = false;
   if(RequireRejection)
   {
      double body      = MathAbs(close1 - open1);
      double upperWick = high1 - MathMax(open1, close1);
      rejection = (upperWick > body * MinWickBodyRatio);
   }
   else
   {
      rejection = true;
   }
   
   double displacement = open1 - close1;
   bool strongMove = (displacement > 20 * _Point);
   
   return sweptHigh && failedBreakout && rejection && strongMove;
}

//+------------------------------------------------------------------+
//| Detect BUY Setup (Sell-side Liquidity Sweep)                     |
//+------------------------------------------------------------------+
bool DetectBuySetup(bool bullishBias, double price)
{
   if(!bullishBias) return false;
   
   double prevLow = iLow(_Symbol, LTF_Period, 
      iLowest(_Symbol, LTF_Period, MODE_LOW, LiquidityLookback, 2));
   
   double zoneDistance = atr[0] * 0.5;
   bool nearSupport = (MathAbs(price - ema50[0]) < zoneDistance) ||
                      (MathAbs(price - prevLow) < zoneDistance);
   
   if(!nearSupport) return false;
   
   double low1   = iLow(_Symbol, LTF_Period, 1);
   double close1 = iClose(_Symbol, LTF_Period, 1);
   double open1  = iOpen(_Symbol, LTF_Period, 1);
   
   bool sweptLow       = low1 < prevLow;
   bool failedBreakout = close1 > prevLow;
   
   bool rejection = false;
   if(RequireRejection)
   {
      double body      = MathAbs(close1 - open1);
      double lowerWick = MathMin(open1, close1) - low1;
      rejection = (lowerWick > body * MinWickBodyRatio);
   }
   else
   {
      rejection = true;
   }
   
   double displacement = close1 - open1;
   bool strongMove = (displacement > 20 * _Point);
   
   return sweptLow && failedBreakout && rejection && strongMove;
}

//+------------------------------------------------------------------+
//| Execute SELL Order                                                |
//+------------------------------------------------------------------+
void ExecuteSell(double price)
{
   double sl = price + atr[0] * ATR_Multiplier;
   double tp = price - atr[0] * ATR_Multiplier * RR_Ratio;
   double stopPoints = (sl - price) / _Point;
   double lot = CalculateLotSize(stopPoints);
   
   MqlTradeRequest request = {};
   MqlTradeResult result = {};
   
   ZeroMemory(request);
   ZeroMemory(result);
   
   request.action    = TRADE_ACTION_DEAL;
   request.symbol    = _Symbol;
   request.volume    = lot;
   request.type      = ORDER_TYPE_SELL;
   request.price     = price;
   request.sl        = sl;
   request.tp        = tp;
   request.deviation = slippage;
   request.comment   = "SmartMoney_SELL";
   
   if(!OrderSend(request, result))
   {
      Print("OrderSend failed. Error: ", GetLastError());
      return;
   }
   
   if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
   {
      Print("SELL order placed. Ticket: ", result.order);
      lastTradeTime = TimeCurrent();
   }
   else
   {
      Print("Order failed. Retcode: ", result.retcode);
   }
}

//+------------------------------------------------------------------+
//| Execute BUY Order                                                 |
//+------------------------------------------------------------------+
void ExecuteBuy(double price)
{
   double sl = price - atr[0] * ATR_Multiplier;
   double tp = price + atr[0] * ATR_Multiplier * RR_Ratio;
   double stopPoints = (price - sl) / _Point;
   double lot = CalculateLotSize(stopPoints);
   
   MqlTradeRequest request = {};
   MqlTradeResult result = {};
   
   ZeroMemory(request);
   ZeroMemory(result);
   
   request.action    = TRADE_ACTION_DEAL;
   request.symbol    = _Symbol;
   request.volume    = lot;
   request.type      = ORDER_TYPE_BUY;
   request.price     = price;
   request.sl        = sl;
   request.tp        = tp;
   request.deviation = slippage;
   request.comment   = "SmartMoney_BUY";
   
   if(!OrderSend(request, result))
   {
      Print("OrderSend failed. Error: ", GetLastError());
      return;
   }
   
   if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
   {
      Print("BUY order placed. Ticket: ", result.order);
      lastTradeTime = TimeCurrent();
   }
   else
   {
      Print("Order failed. Retcode: ", result.retcode);
   }
}

//+------------------------------------------------------------------+
//| Calculate Lot Size Based on Risk                                 |
//+------------------------------------------------------------------+
double CalculateLotSize(double stopPoints)
{
   if(stopPoints <= 0) return 0.01;
   
   double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount = accountBalance * (RiskPercent / 100.0);
   
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double pointValue = tickValue / tickSize * _Point;
   
   double lot = riskAmount / (stopPoints * pointValue);
   
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   
   lot = MathMax(minLot, MathMin(maxLot, lot));
   lot = MathFloor(lot / lotStep) * lotStep;
   
   return NormalizeDouble(lot, 2);
}

//+------------------------------------------------------------------+
//| Manage Open Positions                                             |
//+------------------------------------------------------------------+
void ManagePositions()
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(!PositionSelect(_Symbol)) continue;
      
      ulong ticket = PositionGetTicket(i);
      double entry = PositionGetDouble(POSITION_PRICE_OPEN);
      double sl = PositionGetDouble(POSITION_SL);
      double price = PositionGetDouble(POSITION_PRICE_CURRENT);
      ENUM_POSITION_TYPE posType = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      
      double currentRR = 0;
      if(posType == POSITION_TYPE_SELL)
         currentRR = (entry - price) / (entry - sl);
      else
         currentRR = (price - entry) / (sl - entry);
      
      // Break-even
      if(UseBreakEven && currentRR >= BreakEvenAtRR)
      {
         if(posType == POSITION_TYPE_SELL && price > entry)
            ModifyPosition(ticket, entry, PositionGetDouble(POSITION_TP));
         else if(posType == POSITION_TYPE_BUY && price < entry)
            ModifyPosition(ticket, entry, PositionGetDouble(POSITION_TP));
      }
      
      // Trailing stop
      if(UseTrailingStop && currentRR >= TrailTriggerRR)
      {
         double trailDist = atr[0] * TrailDistance;
         if(posType == POSITION_TYPE_SELL)
         {
            double newSL = price + trailDist;
            if(newSL < sl || sl == 0)
               ModifyPosition(ticket, newSL, PositionGetDouble(POSITION_TP));
         }
         else
         {
            double newSL = price - trailDist;
            if(newSL > sl || sl == 0)
               ModifyPosition(ticket, newSL, PositionGetDouble(POSITION_TP));
         }
      }
   }
}

//+------------------------------------------------------------------+
//| Modify Position SL/TP                                            |
//+------------------------------------------------------------------+
void ModifyPosition(ulong ticket, double newSL, double newTP)
{
   MqlTradeRequest request = {};
   MqlTradeResult result = {};
   
   ZeroMemory(request);
   ZeroMemory(result);
   
   request.action = TRADE_ACTION_SLTP;
   request.position = ticket;
   request.sl = newSL;
   request.tp = newTP;
   
   OrderSend(request, result);
}

//+------------------------------------------------------------------+
//| Check Trading Session                                            |
//+------------------------------------------------------------------+
bool IsInTradingSession()
{
   datetime currentTime = TimeCurrent();
   MqlDateTime dt;
   TimeToStruct(currentTime, dt);
   
   return (dt.hour >= SessionStartHour && dt.hour <= SessionEndHour);
}

//+------------------------------------------------------------------+
//| Check Spread                                                     |
//+------------------------------------------------------------------+
bool IsSpreadAcceptable()
{
   int spread = (int)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
   return (spread <= MaxSpread);
}

//+------------------------------------------------------------------+
//| Check for New Bar                                                |
//+------------------------------------------------------------------+
bool IsNewBar()
{
   static datetime lastBarTime = 0;
   datetime currentBarTime = iTime(_Symbol, LTF_Period, 0);
   
   if(currentBarTime != lastBarTime)
   {
      lastBarTime = currentBarTime;
      return true;
   }
   return false;
}

//+------------------------------------------------------------------+
//| Copy Indicator Values                                            |
//+------------------------------------------------------------------+
bool CopyIndicators()
{
   if(CopyBuffer(ema200Handle, 0, 0, 2, ema200) < 0 ||
      CopyBuffer(ema50Handle, 0, 0, 2, ema50) < 0 ||
      CopyBuffer(atrHandle, 0, 0, 2, atr) < 0)
   {
      Print("Failed to copy indicator buffers. Error: ", GetLastError());
      return false;
   }
   return true;
}
//+------------------------------------------------------------------+
