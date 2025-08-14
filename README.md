# 🔥 Long Candle Detector - MQL5

Sistem deteksi candle panjang otomatis untuk MetaTrader 5 dengan sinyal entry real-time.

## 📋 Fitur Utama

- **Deteksi Real-time**: Monitor candle panjang secara otomatis
- **Sinyal Entry**: Entry point yang tepat di tengah candle panjang
- **Visual Alert**: Arrow dan garis di chart untuk memudahkan analisis
- **Risk Management**: Perhitungan lot size otomatis berdasarkan risk
- **Multi Timeframe**: Support untuk berbagai timeframe (1M, 5M, 15M, 1H)
- **Alert System**: Notifikasi popup, email, dan push notification

## 🚀 Cara Install

### 1. Copy File ke MetaTrader 5

1. Buka MetaTrader 5
2. Tekan `Ctrl+N` untuk membuka Navigator
3. Klik kanan pada folder **Experts** → **Open Folder**
4. Copy file `LongCandleDetector.mq5` ke folder tersebut
5. Copy file `LongCandleIndicator.mq5` ke folder **Indicators**

### 2. Compile Script

1. Di MetaTrader 5, buka **MetaEditor** (`F4`)
2. Buka file `LongCandleDetector.mq5`
3. Tekan `F7` untuk compile
4. Lakukan hal yang sama untuk `LongCandleIndicator.mq5`

### 3. Aktifkan Expert Advisor

1. Di chart, klik kanan → **Expert Advisors** → **Allow live trading**
2. Drag `LongCandleDetector` dari Navigator ke chart
3. Atur parameter sesuai kebutuhan
4. Klik **OK**

## ⚙️ Parameter Settings

### Expert Advisor Parameters

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `LookbackPeriods` | 20 | Jumlah candle untuk perhitungan rata-rata |
| `BodyMultiplier` | 2.0 | Multiplier untuk body panjang (2x rata-rata) |
| `RangeMultiplier` | 1.5 | Multiplier untuk range panjang (1.5x rata-rata) |
| `VolumeMultiplier` | 1.5 | Multiplier untuk volume kuat |
| `EnableAlerts` | true | Aktifkan alert popup |
| `EnableNotifications` | true | Aktifkan notifikasi |
| `EnableEmail` | false | Kirim email alert |
| `EnablePush` | false | Push notification |
| `AlertCooldown` | 60 | Cooldown alert (detik) |

### Indicator Parameters

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `LookbackPeriods` | 20 | Jumlah candle untuk rata-rata |
| `BodyMultiplier` | 2.0 | Multiplier body panjang |
| `RangeMultiplier` | 1.5 | Multiplier range panjang |
| `VolumeMultiplier` | 1.5 | Multiplier volume |
| `EnableAlerts` | true | Aktifkan alert |
| `ShowStrength` | true | Tampilkan strength line |
| `AutoEntry` | false | Auto generate entry signal |
| `RiskPercent` | 2.0 | Risk per trade (%) |

## 📊 Cara Kerja

### 1. Deteksi Candle Panjang

Sistem mendeteksi candle panjang berdasarkan:
- **Body Size**: 2x lebih besar dari rata-rata body candle sebelumnya
- **Range Size**: 1.5x lebih besar dari rata-rata range candle sebelumnya
- **Volume**: 1.5x lebih besar dari rata-rata volume candle sebelumnya

### 2. Entry Signal

Ketika candle panjang terdeteksi:
- **Entry Price**: Close price candle panjang
- **Stop Loss**: Low - (body size × 0.5) untuk bullish, High + (body size × 0.5) untuk bearish
- **Take Profit**: Close + (body size × 1.5) untuk bullish, Close - (body size × 1.5) untuk bearish

### 3. Risk Management

Lot size dihitung otomatis berdasarkan:
```
Risk Amount = Account Balance × (Risk Percent / 100)
Stop Loss Distance = |Entry Price - Stop Loss|
Lot Size = Risk Amount / (Stop Loss Distance × 100000)
```

## 🎯 Strategi Trading

### Entry Rules

1. **Tunggu Candle Panjang**: Sistem akan alert ketika candle panjang terdeteksi
2. **Entry di Close**: Masuk di close price candle panjang
3. **Konfirmasi Volume**: Pastikan volume tinggi untuk validasi sinyal
4. **Risk Management**: Gunakan stop loss dan take profit yang disarankan

### Exit Rules

1. **Stop Loss**: Exit jika harga menyentuh stop loss
2. **Take Profit**: Exit jika harga mencapai take profit
3. **Manual Exit**: Exit manual jika ada perubahan kondisi market

## 📈 Visual Indicators

### Expert Advisor
- **Garis Entry**: Garis horizontal di entry price
- **Garis Stop Loss**: Garis merah putus-putus
- **Garis Take Profit**: Garis hijau putus-putus
- **Text Label**: Label arah sinyal

### Custom Indicator
- **Arrow Hijau**: Candle panjang bullish
- **Arrow Merah**: Candle panjang bearish
- **Strength Line**: Garis kekuatan candle (kuning)
- **Entry Lines**: Garis entry, SL, dan TP otomatis

## ⚠️ Disclaimer

- Sistem ini untuk analisis teknis semata
- Hasil trading tidak dijamin profit
- Selalu gunakan risk management yang proper
- Test di demo account terlebih dahulu
- Trading forex/crypto memiliki risiko tinggi

## 🔧 Troubleshooting

### Error "Not enough data"
- Pastikan ada minimal 20 candle di chart
- Coba timeframe yang lebih besar

### Alert tidak muncul
- Cek setting `EnableAlerts` = true
- Cek cooldown alert
- Pastikan volume dan size candle memenuhi kriteria

### Garis tidak muncul di chart
- Pastikan "Allow live trading" aktif
- Cek setting "Show objects" di chart properties
- Restart Expert Advisor

## 📞 Support

Jika ada masalah atau pertanyaan:
1. Cek log di MetaTrader 5 (View → Log)
2. Pastikan semua parameter sudah benar
3. Test di demo account terlebih dahulu

## 🎉 Tips Penggunaan

1. **Timeframe Optimal**: Gunakan 1M atau 5M untuk scalping
2. **Market Hours**: Lebih efektif saat market aktif (London/NY session)
3. **News Events**: Hindari trading saat news penting
4. **Multiple Timeframes**: Kombinasikan dengan analisis timeframe lebih besar
5. **Backtesting**: Test strategi di historical data terlebih dahulu

---

**Happy Trading! 🚀**