//+------------------------------------------------------------------+
//|                                           LongCandleDetector.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "Detector Candle Panjang dengan Sinyal Entry Real-time"

// Input parameters
input int      LookbackPeriods = 20;        // Jumlah candle untuk rata-rata
input double   BodyMultiplier = 2.0;        // Multiplier untuk body panjang
input double   RangeMultiplier = 1.5;       // Multiplier untuk range panjang
input double   VolumeMultiplier = 1.5;      // Multiplier untuk volume kuat
input bool     EnableAlerts = true;         // Aktifkan alert
input bool     EnableNotifications = true;  // Aktifkan notifikasi
input bool     EnableEmail = false;         // Kirim email
input bool     EnablePush = false;          // Push notification
input int      AlertCooldown = 60;          // Cooldown alert (detik)

// Global variables
datetime lastAlertTime = 0;
bool isNewCandle = false;
int lastCandleTime = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   Print("🔥 LONG CANDLE DETECTOR - Initialized");
   Print("📊 Symbol: ", Symbol());
   Print("⏰ Timeframe: ", EnumToString(Period()));
   Print("📈 Lookback Periods: ", LookbackPeriods);
   Print("=" * 50);
   
   // Set timer untuk check setiap detik
   EventSetTimer(1);
   
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   EventKillTimer();
   Print("🛑 LONG CANDLE DETECTOR - Deinitialized");
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   // Cek apakah ada candle baru
   if(TimeCurrent() != lastCandleTime)
   {
      lastCandleTime = (int)TimeCurrent();
      isNewCandle = true;
      
      // Deteksi candle panjang setelah candle baru terbentuk
      if(isNewCandle)
      {
         DetectLongCandle();
         isNewCandle = false;
      }
   }
}

//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
{
   // Check setiap detik untuk monitoring real-time
   if(isNewCandle)
   {
      DetectLongCandle();
   }
}

//+------------------------------------------------------------------+
//| Deteksi candle panjang                                          |
//+------------------------------------------------------------------+
void DetectLongCandle()
{
   // Ambil data candle terbaru
   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   
   int copied = CopyRates(Symbol(), Period(), 0, LookbackPeriods + 5, rates);
   
   if(copied < LookbackPeriods + 1)
   {
      Print("❌ Tidak cukup data untuk analisis");
      return;
   }
   
   // Hitung rata-rata body dan range
   double avgBody = 0, avgRange = 0, avgVolume = 0;
   
   for(int i = 1; i <= LookbackPeriods; i++)
   {
      avgBody += MathAbs(rates[i].close - rates[i].open);
      avgRange += (rates[i].high - rates[i].low);
      avgVolume += rates[i].tick_volume;
   }
   
   avgBody /= LookbackPeriods;
   avgRange /= LookbackPeriods;
   avgVolume /= LookbackPeriods;
   
   // Analisis candle terbaru (index 0)
   MqlRates currentCandle = rates[0];
   double currentBody = MathAbs(currentCandle.close - currentCandle.open);
   double currentRange = currentCandle.high - currentCandle.low;
   double currentVolume = currentCandle.tick_volume;
   
   // Deteksi candle panjang
   bool isLongBody = currentBody > (avgBody * BodyMultiplier);
   bool isLongRange = currentRange > (avgRange * RangeMultiplier);
   bool isHighVolume = currentVolume > (avgVolume * VolumeMultiplier);
   
   // Candle panjang = body panjang ATAU range panjang
   bool isLongCandle = isLongBody || isLongRange;
   
   // Cek apakah candle sudah selesai (untuk timeframe > 1 menit)
   bool candleComplete = false;
   if(Period() == PERIOD_M1)
      candleComplete = true; // 1 menit candle sudah selesai
   else if(Period() == PERIOD_M5)
      candleComplete = (TimeCurrent() % 300) >= 240; // 4 menit terakhir dari 5 menit
   else if(Period() == PERIOD_M15)
      candleComplete = (TimeCurrent() % 900) >= 780; // 13 menit terakhir dari 15 menit
   else if(Period() == PERIOD_H1)
      candleComplete = (TimeCurrent() % 3600) >= 3300; // 55 menit terakhir dari 1 jam
   
   // Jika candle panjang terdeteksi dan candle sudah hampir selesai
   if(isLongCandle && isHighVolume && candleComplete)
   {
      // Cek cooldown alert
      if(TimeCurrent() - lastAlertTime > AlertCooldown)
      {
         GenerateEntrySignal(currentCandle, avgBody, avgRange, avgVolume);
         lastAlertTime = TimeCurrent();
      }
   }
}

//+------------------------------------------------------------------+
//| Generate entry signal                                            |
//+------------------------------------------------------------------+
void GenerateEntrySignal(MqlRates &candle, double avgBody, double avgRange, double avgVolume)
{
   // Tentukan arah candle
   string direction = "";
   double entryPrice = 0, stopLoss = 0, takeProfit = 0;
   double bodySize = MathAbs(candle.close - candle.open);
   double rangeSize = candle.high - candle.low;
   
   if(candle.close > candle.open)
   {
      direction = "BULLISH";
      entryPrice = candle.close; // Entry di close candle
      stopLoss = candle.low - (bodySize * 0.5);
      takeProfit = candle.close + (bodySize * 1.5);
   }
   else
   {
      direction = "BEARISH";
      entryPrice = candle.close; // Entry di close candle
      stopLoss = candle.high + (bodySize * 0.5);
      takeProfit = candle.close - (bodySize * 1.5);
   }
   
   // Hitung strength ratio
   double strengthRatio = (candle.tick_volume * rangeSize) / (avgVolume * avgRange);
   
   // Format pesan alert
   string alertMessage = "";
   alertMessage += "🚨 SINYAL ENTRY DETECTED! 🚨\n";
   alertMessage += "⏰ Waktu: " + TimeToString(TimeCurrent(), TIME_MINUTES) + "\n";
   alertMessage += "📈 Arah: " + direction + "\n";
   alertMessage += "💰 Entry Price: " + DoubleToString(entryPrice, Digits()) + "\n";
   alertMessage += "🛑 Stop Loss: " + DoubleToString(stopLoss, Digits()) + "\n";
   alertMessage += "🎯 Take Profit: " + DoubleToString(takeProfit, Digits()) + "\n";
   alertMessage += "📊 Body Size: " + DoubleToString(bodySize, Digits()) + "\n";
   alertMessage += "📏 Range Size: " + DoubleToString(rangeSize, Digits()) + "\n";
   alertMessage += "💪 Strength Ratio: " + DoubleToString(strengthRatio, 2) + "x\n";
   alertMessage += "📈 Volume: " + DoubleToString(candle.tick_volume, 0) + "\n";
   alertMessage += "=" * 50;
   
   // Tampilkan alert
   if(EnableAlerts)
   {
      Alert(alertMessage);
   }
   
   // Tampilkan di log
   Print(alertMessage);
   
   // Kirim notifikasi
   if(EnableNotifications)
   {
      string notificationTitle = "Long Candle Signal - " + Symbol();
      string notificationBody = direction + " Signal at " + DoubleToString(entryPrice, Digits());
      
      if(EnableEmail)
      {
         SendMail(notificationTitle, alertMessage);
      }
      
      if(EnablePush)
      {
         SendNotification(notificationBody);
      }
   }
   
   // Tampilkan info di chart
   ShowSignalOnChart(entryPrice, stopLoss, takeProfit, direction);
}

//+------------------------------------------------------------------+
//| Tampilkan sinyal di chart                                        |
//+------------------------------------------------------------------+
void ShowSignalOnChart(double entryPrice, double stopLoss, double takeProfit, string direction)
{
   string signalName = "Signal_" + TimeToString(TimeCurrent());
   
   // Hapus objek lama jika ada
   ObjectDelete(0, signalName + "_Entry");
   ObjectDelete(0, signalName + "_SL");
   ObjectDelete(0, signalName + "_TP");
   ObjectDelete(0, signalName + "_Text");
   
   // Warna berdasarkan arah
   color signalColor = (direction == "BULLISH") ? clrLime : clrRed;
   
   // Garis entry
   ObjectCreate(0, signalName + "_Entry", OBJ_HLINE, 0, 0, entryPrice);
   ObjectSetInteger(0, signalName + "_Entry", OBJPROP_COLOR, signalColor);
   ObjectSetInteger(0, signalName + "_Entry", OBJPROP_WIDTH, 2);
   ObjectSetInteger(0, signalName + "_Entry", OBJPROP_STYLE, STYLE_SOLID);
   
   // Garis stop loss
   ObjectCreate(0, signalName + "_SL", OBJ_HLINE, 0, 0, stopLoss);
   ObjectSetInteger(0, signalName + "_SL", OBJPROP_COLOR, clrRed);
   ObjectSetInteger(0, signalName + "_SL", OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, signalName + "_SL", OBJPROP_STYLE, STYLE_DOT);
   
   // Garis take profit
   ObjectCreate(0, signalName + "_TP", OBJ_HLINE, 0, 0, takeProfit);
   ObjectSetInteger(0, signalName + "_TP", OBJPROP_COLOR, clrLime);
   ObjectSetInteger(0, signalName + "_TP", OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, signalName + "_TP", OBJPROP_STYLE, STYLE_DOT);
   
   // Text label
   ObjectCreate(0, signalName + "_Text", OBJ_TEXT, 0, TimeCurrent(), entryPrice);
   ObjectSetString(0, signalName + "_Text", OBJPROP_TEXT, direction + " SIGNAL");
   ObjectSetInteger(0, signalName + "_Text", OBJPROP_COLOR, signalColor);
   ObjectSetInteger(0, signalName + "_Text", OBJPROP_FONTSIZE, 10);
   ObjectSetInteger(0, signalName + "_Text", OBJPROP_ANCHOR, ANCHOR_LEFT);
   
   // Auto-hapus setelah 1 jam
   EventSetTimer(3600);
}

//+------------------------------------------------------------------+
//| Custom function untuk string repeat                              |
//+------------------------------------------------------------------+
string operator*(string str, int count)
{
   string result = "";
   for(int i = 0; i < count; i++)
   {
      result += str;
   }
   return result;
}

//+------------------------------------------------------------------+
//| Custom function untuk string repeat dengan char                  |
//+------------------------------------------------------------------+
string operator*(string str, char ch)
{
   return str + CharToString(ch);
}