//+------------------------------------------------------------------+
//|                                        LongCandleIndicator.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "Indikator Deteksi Candle Panjang dengan Visual Alert"
#property indicator_chart_window
#property indicator_buffers 3
#property indicator_plots   3

//--- plot LongCandle
#property indicator_label1  "Long Candle"
#property indicator_type1   DRAW_ARROW
#property indicator_color1  clrLime
#property indicator_style1  STYLE_SOLID
#property indicator_width1  3

//--- plot LongCandleBearish
#property indicator_label2  "Long Candle Bearish"
#property indicator_type2   DRAW_ARROW
#property indicator_color2  clrRed
#property indicator_style2  STYLE_SOLID
#property indicator_width2  3

//--- plot Strength
#property indicator_label3  "Candle Strength"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrYellow
#property indicator_style3  STYLE_SOLID
#property indicator_width3  1

// Input parameters
input int      LookbackPeriods = 20;        // Jumlah candle untuk rata-rata
input double   BodyMultiplier = 2.0;        // Multiplier untuk body panjang
input double   RangeMultiplier = 1.5;       // Multiplier untuk range panjang
input double   VolumeMultiplier = 1.5;      // Multiplier untuk volume kuat
input bool     EnableAlerts = true;         // Aktifkan alert
input bool     ShowStrength = true;         // Tampilkan strength line
input bool     AutoEntry = false;           // Auto entry signal
input double   RiskPercent = 2.0;           // Risk per trade (%)

// Indicator buffers
double LongCandleBuffer[];
double LongCandleBearishBuffer[];
double StrengthBuffer[];

// Global variables
datetime lastAlertTime = 0;
int lastCalculatedBar = 0;

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
   // Set indicator buffers
   SetIndexBuffer(0, LongCandleBuffer, INDICATOR_DATA);
   SetIndexBuffer(1, LongCandleBearishBuffer, INDICATOR_DATA);
   SetIndexBuffer(2, StrengthBuffer, INDICATOR_DATA);
   
   // Set arrow codes
   PlotIndexSetInteger(0, PLOT_ARROW, 233); // Up arrow
   PlotIndexSetInteger(1, PLOT_ARROW, 234); // Down arrow
   
   // Set indicator name
   IndicatorSetString(INDICATOR_SHORTNAME, "Long Candle Detector");
   
   // Set accuracy
   IndicatorSetInteger(INDICATOR_DIGITS, Digits());
   
   Print("🔥 LONG CANDLE INDICATOR - Initialized");
   Print("📊 Symbol: ", Symbol());
   Print("⏰ Timeframe: ", EnumToString(Period()));
   Print("📈 Lookback Periods: ", LookbackPeriods);
   Print("=" * 50);
   
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   // Cek apakah ada data yang cukup
   if(rates_total < LookbackPeriods + 1)
      return(0);
   
   // Tentukan bar yang perlu dihitung
   int start = prev_calculated;
   if(start == 0)
   {
      start = LookbackPeriods;
      // Reset buffers
      ArrayInitialize(LongCandleBuffer, EMPTY_VALUE);
      ArrayInitialize(LongCandleBearishBuffer, EMPTY_VALUE);
      ArrayInitialize(StrengthBuffer, EMPTY_VALUE);
   }
   
   // Hitung untuk setiap bar
   for(int i = start; i < rates_total; i++)
   {
      // Hitung rata-rata body, range, dan volume
      double avgBody = 0, avgRange = 0, avgVolume = 0;
      
      for(int j = 1; j <= LookbackPeriods; j++)
      {
         int idx = i - j;
         if(idx >= 0)
         {
            avgBody += MathAbs(close[idx] - open[idx]);
            avgRange += (high[idx] - low[idx]);
            avgVolume += tick_volume[idx];
         }
      }
      
      avgBody /= LookbackPeriods;
      avgRange /= LookbackPeriods;
      avgVolume /= LookbackPeriods;
      
      // Analisis candle saat ini
      double currentBody = MathAbs(close[i] - open[i]);
      double currentRange = high[i] - low[i];
      double currentVolume = tick_volume[i];
      
      // Deteksi candle panjang
      bool isLongBody = currentBody > (avgBody * BodyMultiplier);
      bool isLongRange = currentRange > (avgRange * RangeMultiplier);
      bool isHighVolume = currentVolume > (avgVolume * VolumeMultiplier);
      
      // Candle panjang = body panjang ATAU range panjang
      bool isLongCandle = isLongBody || isLongRange;
      
      // Hitung strength ratio
      double strengthRatio = (currentVolume * currentRange) / (avgVolume * avgRange);
      
      // Set strength buffer
      if(ShowStrength)
         StrengthBuffer[i] = strengthRatio;
      
      // Deteksi arah candle
      bool isBullish = close[i] > open[i];
      
      // Set arrow buffer
      if(isLongCandle && isHighVolume)
      {
         if(isBullish)
         {
            LongCandleBuffer[i] = low[i] - (currentRange * 0.1); // Arrow di bawah candle
            LongCandleBearishBuffer[i] = EMPTY_VALUE;
         }
         else
         {
            LongCandleBearishBuffer[i] = high[i] + (currentRange * 0.1); // Arrow di atas candle
            LongCandleBuffer[i] = EMPTY_VALUE;
         }
         
         // Generate alert untuk candle terbaru
         if(i == rates_total - 1 && EnableAlerts)
         {
            GenerateAlert(time[i], open[i], high[i], low[i], close[i], 
                         currentBody, currentRange, currentVolume, 
                         avgBody, avgRange, avgVolume, isBullish);
         }
         
         // Auto entry signal
         if(AutoEntry && i == rates_total - 1)
         {
            GenerateEntrySignal(time[i], open[i], high[i], low[i], close[i], 
                              currentBody, currentRange, currentVolume, isBullish);
         }
      }
      else
      {
         LongCandleBuffer[i] = EMPTY_VALUE;
         LongCandleBearishBuffer[i] = EMPTY_VALUE;
      }
   }
   
   lastCalculatedBar = rates_total;
   return(rates_total);
}

//+------------------------------------------------------------------+
//| Generate alert                                                   |
//+------------------------------------------------------------------+
void GenerateAlert(datetime time, double open, double high, double low, double close,
                  double body, double range, double volume,
                  double avgBody, double avgRange, double avgVolume, bool isBullish)
{
   // Cek cooldown alert
   if(time - lastAlertTime < 60) // 1 menit cooldown
      return;
   
   string direction = isBullish ? "BULLISH" : "BEARISH";
   double strengthRatio = (volume * range) / (avgVolume * avgRange);
   
   // Format pesan alert
   string alertMessage = "";
   alertMessage += "🚨 LONG CANDLE DETECTED! 🚨\n";
   alertMessage += "⏰ Waktu: " + TimeToString(time, TIME_MINUTES) + "\n";
   alertMessage += "📈 Arah: " + direction + "\n";
   alertMessage += "💰 Open: " + DoubleToString(open, Digits()) + "\n";
   alertMessage += "💰 Close: " + DoubleToString(close, Digits()) + "\n";
   alertMessage += "📊 Body Size: " + DoubleToString(body, Digits()) + "\n";
   alertMessage += "📏 Range Size: " + DoubleToString(range, Digits()) + "\n";
   alertMessage += "💪 Strength Ratio: " + DoubleToString(strengthRatio, 2) + "x\n";
   alertMessage += "📈 Volume: " + DoubleToString(volume, 0) + "\n";
   alertMessage += "=" * 50;
   
   // Tampilkan alert
   Alert(alertMessage);
   Print(alertMessage);
   
   lastAlertTime = time;
}

//+------------------------------------------------------------------+
//| Generate entry signal                                            |
//+------------------------------------------------------------------+
void GenerateEntrySignal(datetime time, double open, double high, double low, double close,
                        double body, double range, double volume, bool isBullish)
{
   string direction = isBullish ? "BULLISH" : "BEARISH";
   double entryPrice = close; // Entry di close candle
   double stopLoss, takeProfit;
   
   if(isBullish)
   {
      stopLoss = low - (body * 0.5);
      takeProfit = close + (body * 1.5);
   }
   else
   {
      stopLoss = high + (body * 0.5);
      takeProfit = close - (body * 1.5);
   }
   
   // Hitung lot size berdasarkan risk
   double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount = accountBalance * (RiskPercent / 100.0);
   double stopLossDistance = MathAbs(entryPrice - stopLoss);
   double lotSize = NormalizeDouble(riskAmount / (stopLossDistance * 100000), 2); // Untuk forex
   
   // Format entry signal
   string entryMessage = "";
   entryMessage += "🎯 ENTRY SIGNAL GENERATED! 🎯\n";
   entryMessage += "⏰ Waktu: " + TimeToString(time, TIME_MINUTES) + "\n";
   entryMessage += "📈 Arah: " + direction + "\n";
   entryMessage += "💰 Entry Price: " + DoubleToString(entryPrice, Digits()) + "\n";
   entryMessage += "🛑 Stop Loss: " + DoubleToString(stopLoss, Digits()) + "\n";
   entryMessage += "🎯 Take Profit: " + DoubleToString(takeProfit, Digits()) + "\n";
   entryMessage += "📊 Lot Size: " + DoubleToString(lotSize, 2) + "\n";
   entryMessage += "💵 Risk Amount: $" + DoubleToString(riskAmount, 2) + "\n";
   entryMessage += "=" * 50;
   
   // Tampilkan entry signal
   Alert(entryMessage);
   Print(entryMessage);
   
   // Tampilkan garis di chart
   ShowEntryLines(entryPrice, stopLoss, takeProfit, direction, time);
}

//+------------------------------------------------------------------+
//| Tampilkan garis entry di chart                                   |
//+------------------------------------------------------------------+
void ShowEntryLines(double entryPrice, double stopLoss, double takeProfit, 
                   string direction, datetime time)
{
   string baseName = "Entry_" + TimeToString(time);
   
   // Hapus objek lama
   ObjectDelete(0, baseName + "_Entry");
   ObjectDelete(0, baseName + "_SL");
   ObjectDelete(0, baseName + "_TP");
   ObjectDelete(0, baseName + "_Text");
   
   // Warna berdasarkan arah
   color signalColor = (direction == "BULLISH") ? clrLime : clrRed;
   
   // Garis entry
   ObjectCreate(0, baseName + "_Entry", OBJ_HLINE, 0, 0, entryPrice);
   ObjectSetInteger(0, baseName + "_Entry", OBJPROP_COLOR, signalColor);
   ObjectSetInteger(0, baseName + "_Entry", OBJPROP_WIDTH, 2);
   ObjectSetInteger(0, baseName + "_Entry", OBJPROP_STYLE, STYLE_SOLID);
   
   // Garis stop loss
   ObjectCreate(0, baseName + "_SL", OBJ_HLINE, 0, 0, stopLoss);
   ObjectSetInteger(0, baseName + "_SL", OBJPROP_COLOR, clrRed);
   ObjectSetInteger(0, baseName + "_SL", OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, baseName + "_SL", OBJPROP_STYLE, STYLE_DOT);
   
   // Garis take profit
   ObjectCreate(0, baseName + "_TP", OBJ_HLINE, 0, 0, takeProfit);
   ObjectSetInteger(0, baseName + "_TP", OBJPROP_COLOR, clrLime);
   ObjectSetInteger(0, baseName + "_TP", OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, baseName + "_TP", OBJPROP_STYLE, STYLE_DOT);
   
   // Text label
   ObjectCreate(0, baseName + "_Text", OBJ_TEXT, 0, time, entryPrice);
   ObjectSetString(0, baseName + "_Text", OBJPROP_TEXT, direction + " ENTRY");
   ObjectSetInteger(0, baseName + "_Text", OBJPROP_COLOR, signalColor);
   ObjectSetInteger(0, baseName + "_Text", OBJPROP_FONTSIZE, 10);
   ObjectSetInteger(0, baseName + "_Text", OBJPROP_ANCHOR, ANCHOR_LEFT);
}