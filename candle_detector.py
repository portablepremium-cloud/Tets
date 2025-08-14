import yfinance as yf
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

class LongCandleDetector:
    def __init__(self, symbol="BTC-USD", timeframe="1m", lookback_periods=20):
        """
        Detector untuk candle panjang dengan sinyal entry real-time
        
        Parameters:
        - symbol: Pair trading (default: BTC-USD)
        - timeframe: Interval candle (1m, 5m, 15m, 1h, 1d)
        - lookback_periods: Jumlah candle untuk perhitungan rata-rata
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.lookback_periods = lookback_periods
        self.data = None
        self.last_alert_time = None
        
    def fetch_data(self):
        """Ambil data real-time dari Yahoo Finance"""
        try:
            # Ambil data dengan interval yang lebih kecil untuk deteksi real-time
            ticker = yf.Ticker(self.symbol)
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)  # 24 jam terakhir
            
            self.data = ticker.history(
                start=start_time,
                end=end_time,
                interval=self.timeframe
            )
            
            if self.data.empty:
                print(f"❌ Tidak ada data untuk {self.symbol}")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error mengambil data: {e}")
            return False
    
    def calculate_candle_metrics(self):
        """Hitung metrik untuk setiap candle"""
        if self.data is None or self.data.empty:
            return None
            
        df = self.data.copy()
        
        # Hitung body dan shadow candle
        df['body'] = abs(df['Close'] - df['Open'])
        df['upper_shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
        df['lower_shadow'] = df[['Open', 'Close']].min(axis=1) - df['Low']
        df['total_range'] = df['High'] - df['Low']
        
        # Hitung rata-rata body candle dalam periode lookback
        df['avg_body'] = df['body'].rolling(window=self.lookback_periods).mean()
        df['avg_range'] = df['total_range'].rolling(window=self.lookback_periods).mean()
        
        # Deteksi candle panjang
        df['is_long_body'] = df['body'] > (df['avg_body'] * 2.0)  # Body 2x lebih besar dari rata-rata
        df['is_long_range'] = df['total_range'] > (df['avg_range'] * 1.5)  # Range 1.5x lebih besar
        
        # Candle panjang = body panjang ATAU range panjang
        df['is_long_candle'] = df['is_long_body'] | df['is_long_range']
        
        # Hitung kekuatan candle (volume * range)
        df['candle_strength'] = df['Volume'] * df['total_range']
        df['avg_strength'] = df['candle_strength'].rolling(window=self.lookback_periods).mean()
        df['is_strong_candle'] = df['candle_strength'] > (df['avg_strength'] * 1.5)
        
        return df
    
    def detect_entry_signals(self, df):
        """Deteksi sinyal entry berdasarkan candle panjang"""
        signals = []
        
        if df is None or df.empty:
            return signals
            
        # Cari candle panjang yang baru terbentuk
        for i in range(1, len(df)):
            current_candle = df.iloc[i]
            prev_candle = df.iloc[i-1]
            
            # Deteksi candle panjang yang sedang terbentuk
            if current_candle['is_long_candle'] and current_candle['is_strong_candle']:
                
                # Tentukan arah candle
                if current_candle['Close'] > current_candle['Open']:
                    direction = "BULLISH"
                    entry_price = current_candle['Close']  # Entry di close candle
                    stop_loss = current_candle['Low'] - (current_candle['body'] * 0.5)
                    take_profit = current_candle['Close'] + (current_candle['body'] * 1.5)
                else:
                    direction = "BEARISH"
                    entry_price = current_candle['Close']  # Entry di close candle
                    stop_loss = current_candle['High'] + (current_candle['body'] * 0.5)
                    take_profit = current_candle['Close'] - (current_candle['body'] * 1.5)
                
                signal = {
                    'timestamp': current_candle.name,
                    'direction': direction,
                    'entry_price': round(entry_price, 2),
                    'stop_loss': round(stop_loss, 2),
                    'take_profit': round(take_profit, 2),
                    'body_size': round(current_candle['body'], 2),
                    'range_size': round(current_candle['total_range'], 2),
                    'volume': current_candle['Volume'],
                    'strength_ratio': round(current_candle['candle_strength'] / current_candle['avg_strength'], 2)
                }
                
                signals.append(signal)
        
        return signals
    
    def print_signal_alert(self, signal):
        """Tampilkan alert sinyal entry"""
        timestamp = signal['timestamp'].strftime('%H:%M:%S')
        
        print(f"\n🚨 SINYAL ENTRY DETECTED! 🚨")
        print(f"⏰ Waktu: {timestamp}")
        print(f"📈 Arah: {signal['direction']}")
        print(f"💰 Entry Price: ${signal['entry_price']:,.2f}")
        print(f"🛑 Stop Loss: ${signal['stop_loss']:,.2f}")
        print(f"🎯 Take Profit: ${signal['take_profit']:,.2f}")
        print(f"📊 Body Size: ${signal['body_size']:,.2f}")
        print(f"📏 Range Size: ${signal['range_size']:,.2f}")
        print(f"💪 Strength Ratio: {signal['strength_ratio']}x")
        print("=" * 50)
    
    def monitor_realtime(self, check_interval=30):
        """Monitor real-time untuk deteksi candle panjang"""
        print(f"🔍 Memulai monitoring {self.symbol} real-time...")
        print(f"⏱️  Interval check: {check_interval} detik")
        print("=" * 50)
        
        while True:
            try:
                # Ambil data terbaru
                if self.fetch_data():
                    df = self.calculate_candle_metrics()
                    signals = self.detect_entry_signals(df)
                    
                    # Tampilkan sinyal baru
                    for signal in signals:
                        # Cek apakah ini sinyal baru (belum di-alert)
                        if (self.last_alert_time is None or 
                            signal['timestamp'] > self.last_alert_time):
                            
                            self.print_signal_alert(signal)
                            self.last_alert_time = signal['timestamp']
                
                # Tampilkan status monitoring
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"⏰ {current_time} - Monitoring aktif... (Ctrl+C untuk stop)")
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring dihentikan oleh user")
                break
            except Exception as e:
                print(f"❌ Error dalam monitoring: {e}")
                time.sleep(check_interval)
    
    def analyze_historical(self):
        """Analisis data historis untuk pattern candle panjang"""
        if not self.fetch_data():
            return
            
        df = self.calculate_candle_metrics()
        
        if df is None or df.empty:
            print("❌ Tidak ada data untuk dianalisis")
            return
        
        # Statistik candle panjang
        long_candles = df[df['is_long_candle']]
        total_candles = len(df)
        long_candle_count = len(long_candles)
        
        print(f"\n📊 ANALISIS CANDLE PANJANG - {self.symbol}")
        print(f"📅 Periode: {df.index[0].strftime('%Y-%m-%d %H:%M')} - {df.index[-1].strftime('%Y-%m-%d %H:%M')}")
        print(f"📈 Total Candle: {total_candles}")
        print(f"🔥 Candle Panjang: {long_candle_count} ({long_candle_count/total_candles*100:.1f}%)")
        
        if not long_candles.empty:
            print(f"\n📋 STATISTIK CANDLE PANJANG:")
            print(f"   Rata-rata Body Size: ${long_candles['body'].mean():,.2f}")
            print(f"   Rata-rata Range Size: ${long_candles['total_range'].mean():,.2f}")
            print(f"   Rata-rata Volume: {long_candles['Volume'].mean():,.0f}")
            
            # Arah candle panjang
            bullish_long = long_candles[long_candles['Close'] > long_candles['Open']]
            bearish_long = long_candles[long_candles['Close'] < long_candles['Open']]
            
            print(f"\n📈 BULLISH Long Candles: {len(bullish_long)} ({len(bullish_long)/long_candle_count*100:.1f}%)")
            print(f"📉 BEARISH Long Candles: {len(bearish_long)} ({len(bearish_long)/long_candle_count*100:.1f}%)")
        
        return df

def main():
    """Main function untuk menjalankan detector"""
    print("🔥 LONG CANDLE DETECTOR - Bitcoin Trading 🔥")
    print("=" * 50)
    
    # Inisialisasi detector
    detector = LongCandleDetector(
        symbol="BTC-USD",
        timeframe="1m",  # 1 menit untuk deteksi real-time
        lookback_periods=20
    )
    
    while True:
        print("\n📋 MENU:")
        print("1. 📊 Analisis Data Historis")
        print("2. 🔍 Monitor Real-time")
        print("3. ⚙️  Ubah Settings")
        print("4. 🚪 Keluar")
        
        choice = input("\nPilih menu (1-4): ").strip()
        
        if choice == "1":
            print("\n📊 Menjalankan analisis historis...")
            detector.analyze_historical()
            
        elif choice == "2":
            print("\n🔍 Memulai monitoring real-time...")
            interval = input("Interval check (detik, default 30): ").strip()
            try:
                interval = int(interval) if interval else 30
                detector.monitor_realtime(check_interval=interval)
            except ValueError:
                print("❌ Interval tidak valid, menggunakan default 30 detik")
                detector.monitor_realtime()
                
        elif choice == "3":
            print("\n⚙️  Settings:")
            symbol = input(f"Symbol (default {detector.symbol}): ").strip()
            if symbol:
                detector.symbol = symbol
                
            timeframe = input(f"Timeframe (1m/5m/15m/1h, default {detector.timeframe}): ").strip()
            if timeframe in ['1m', '5m', '15m', '1h']:
                detector.timeframe = timeframe
                
            lookback = input(f"Lookback periods (default {detector.lookback_periods}): ").strip()
            try:
                if lookback:
                    detector.lookback_periods = int(lookback)
            except ValueError:
                print("❌ Lookback tidak valid")
                
            print(f"✅ Settings updated: {detector.symbol}, {detector.timeframe}, {detector.lookback_periods}")
            
        elif choice == "4":
            print("👋 Terima kasih telah menggunakan Long Candle Detector!")
            break
            
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()