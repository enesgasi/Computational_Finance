# Lecture 15 - Triangular Arbitrage (Üçgen Arbitraj)

## İçerik
Bu ders, kripto para piyasalarında üçgen arbitraj stratejisini öğretir. BTC/EUR, EUR/USDT ve BTC/USDT fiyat paritelerindeki verimsizliklerden kar elde etme yöntemi gösterilir.

## Dosyalar
- `lecture15.py` - Arbitraj fırsatlarını tespit eden analiz scripti (33 satır)
- `lecture15_2.py` - Kümülatif arbitraj profit simülasyonu (28 satır)
- `mahmut.py` - Basitleştirilmiş arbitraj hesaplayıcı (19 satır)
- `BTCEUR_price.csv` - Bitcoin/Euro fiyat verileri
- `EURUSDT_price.csv` - Euro/USDT fiyat verileri
- `BTCUSDT_price.csv` - Bitcoin/USDT fiyat verileri

## Triangular Arbitrage Nedir?

### Temel Konsept
Üçgen arbitraj, üç farklı trading pair arasındaki fiyat tutarsızlıklarından kar elde etme stratejisidir.

### Arbitraj Döngüsü:
1. **BTC → EUR**: BTC sat, EUR al
2. **EUR → USDT**: EUR sat, USDT al
3. **USDT → BTC**: USDT sat, BTC al

**Kar Koşulu:**
$$\frac{P_{BTC/EUR} \times P_{EUR/USDT}}{P_{BTC/USDT}} > 1$$

## Script Detayları

### lecture15.py - Arbitraj Fırsat Analizi

#### 1. Veri Yükleme
```python
btceur = pd.read_csv("BTCEUR_price.csv", header=None)
eurusdt = pd.read_csv("EURUSDT_price.csv", header=None)
btcusdt = pd.read_csv("BTCUSDT_price.csv", header=None)

# Transpose (veriler yatay formatta)
btceur = btceur.T
eurusdt = eurusdt.T
btcusdt = btcusdt.T
```

#### 2. DataFrame Oluşturma
```python
btceur.columns = ["btceur"]
eurusdt.columns = ["eurusdt"]
btcusdt.columns = ["btcusdt"]

df = pd.concat([btceur, eurusdt, btcusdt], axis=1)
```

#### 3. Arbitraj Hesaplama
```python
df["btc_start"] = 1.0  # 1 BTC ile başla

# Üçgen döngüsü:
df["eur"] = df["btc_start"] * df["btceur"]        # BTC → EUR
df["usdt"] = df["eur"] * df["eurusdt"]           # EUR → USDT
df["btc_end"] = df["usdt"] / df["btcusdt"]       # USDT → BTC

# Kar yüzdesi
df["profit_pct"] = (df["btc_end"] - 1) * 100
```

**Matematiksel Formül:**
$$BTC_{end} = \frac{BTC_{start} \times P_{BTC/EUR} \times P_{EUR/USDT}}{P_{BTC/USDT}}$$

$$Profit(\%) = (BTC_{end} - BTC_{start}) \times 100$$

#### 4. Fırsat Tespiti
```python
arb = df[df["profit_pct"] >= 0.04]  # %0.04+ kar fırsatları

print("Total arbitrage opportunities:", len(arb))
print(arb[["btc_end", "profit_pct"]])
```

**Threshold**: %0.04 (işlem ücretlerini karşılamak için minimum)

---

### lecture15_2.py - Kümülatif Arbitraj Simülasyonu

#### 1. Dinamik Capital Management
```python
btc_balance = 1.0        # Başlangıç: 1 BTC
threshold = 1.0004       # Minimum %0.04 kar
trade_count = 0

for _, row in df.iterrows():
    # Arbitraj oranı hesapla
    btc_end = (btc_balance * row["btceur"] * row["eurusdt"]) / row["btcusdt"]
    
    # Karlıysa işlem yap
    if btc_end >= btc_balance * threshold:
        btc_balance = btc_end  # Bakiyeyi güncelle
        trade_count += 1
```

#### 2. Sonuç Analizi
```python
cumulative_profit_pct = (btc_balance - 1) * 100

print(f"Executed trades: {trade_count}")
print(f"Final BTC balance: {btc_balance:.6f}")
print(f"Cumulative profit (%): {cumulative_profit_pct:.3f}")
```

**Önemli Fark:**
- `lecture15.py`: Sadece fırsatları tespit eder
- `lecture15_2.py`: Her işlemden sonra sermayeyi günceller (compounding effect)

---

### mahmut.py - Basitleştirilmiş Versiyon

#### Daha Basit Yaklaşım
```python
capital = 1  # 1 BTC
margin = 1.0004

for i in range(1000):
    x = btceur.iloc[0,i]   # BTC/EUR
    y = btcusdt.iloc[0,i]  # BTC/USDT
    z = eurusdt.iloc[0,i]  # EUR/USDT
    
    ratio = (x * z) / y  # Arbitraj oranı
    
    if ratio > margin:
        print(f"Arbitrage opportunity at index {i}:")
        capital = float(capital) * ratio
        print(f"New capital: {capital} BTC")

percent = 100 * capital - 100
print("profit percentage:", percent)
```

**Farklılıklar:**
- Daha basit kod yapısı
- Pandas DataFrame kullanmıyor
- Aynı mantık, daha az satır

## Üçgen Arbitraj Matematiği

### Arbitraj Oranı Formülü
$$R = \frac{P_{BTC/EUR} \times P_{EUR/USDT}}{P_{BTC/USDT}}$$

### Kar Hesaplama
$$Profit = Capital \times (R - 1)$$

### Kümülatif Kar (Compounding)
$$Capital_{final} = Capital_{initial} \times \prod_{t=1}^{n} R_t$$

Burada $R_t > threshold$ olan tüm zamanlar için.

### Örnek Hesaplama

**Fiyatlar:**
- BTC/EUR = 50,000
- EUR/USDT = 1.10
- BTC/USDT = 54,000

**Arbitraj Oranı:**
$$R = \frac{50,000 \times 1.10}{54,000} = \frac{55,000}{54,000} = 1.0185$$

**Kar:** %1.85 (İşlem ücretleri öncesi)

**İşlem Akışı:**
1. 1 BTC sat → 50,000 EUR al
2. 50,000 EUR sat → 55,000 USDT al
3. 55,000 USDT sat → 1.0185 BTC al
4. **Net Kar**: 0.0185 BTC (%1.85)

## Kullanılan Kütüphaneler

### Python:
- **pandas**: Veri manipülasyonu
  - `read_csv()`: CSV okuma
  - `transpose()` / `.T`: Satır-sütun dönüşümü
  - `concat()`: DataFrame birleştirme
  - `iterrows()`: Satır satır döngü

## Öğrenilen Konular

1. **Triangular Arbitrage**: Üçgen arbitraj mekanizması
2. **Cross-Rate Inefficiency**: Çapraz kur verimsizlikleri
3. **Market Making**: Piyasa yapıcılık fırsatları
4. **Transaction Cost Analysis**: İşlem maliyeti etkisi
5. **Compounding Effect**: Birleşik faiz etkisi
6. **Real-time Detection**: Gerçek zamanlı fırsat tespiti
7. **Data Alignment**: Farklı veri kaynaklarını senkronize etme
8. **Threshold Optimization**: Eşik değer belirleme

## Arbitraj Türleri Karşılaştırması

| Tür | Pairler | Karmaşıklık | Risk | Getiri |
|-----|---------|-------------|------|--------|
| **Simple Arbitrage** | 2 (A-B) | Düşük | Düşük | Düşük |
| **Triangular Arbitrage** | 3 (A-B-C-A) | Orta | Orta | Orta |
| **Quadrangular** | 4+ | Yüksek | Yüksek | Yüksek |
| **Cross-Exchange** | Farklı borsalar | Orta | Yüksek | Yüksek |

## Başarı Faktörleri

### Gerekli Şartlar:
- ✅ **Low Latency**: Düşük gecikme (< 100ms)
- ✅ **High Liquidity**: Yüksek likidite
- ✅ **Low Fees**: Düşük işlem ücretleri (< 0.1%)
- ✅ **Fast Execution**: Hızlı emir iletimi
- ✅ **Automated System**: Otomatik işlem sistemi

### Zorluklar:
- ❌ **Competition**: Yüksek rekabet (HFT firmalar)
- ❌ **Slippage**: Fiyat kayması
- ❌ **Latency**: Network gecikmesi
- ❌ **Execution Risk**: Emir gerçekleşmeme
- ❌ **Capital Requirements**: Yüksek sermaye ihtiyacı

## Risk Yönetimi

### 1. Execution Risk (Emir Gerçekleşme Riski)
```python
# Emir sırası kritik
try:
    order1 = sell_btc_for_eur()
    order2 = sell_eur_for_usdt()
    order3 = buy_btc_with_usdt()
except:
    # Rollback or hedge
    handle_failed_arbitrage()
```

### 2. Slippage Risk
```python
# Expected vs Actual price
expected_profit = calculate_theoretical_profit()
actual_profit = execute_trades()
slippage = expected_profit - actual_profit

if slippage > max_acceptable_slippage:
    cancel_arbitrage()
```

### 3. Partial Fill Risk
```python
# Kısmi emir gerçekleşme
if order1.filled < order1.amount:
    # Kalan pozisyon risk altında
    hedge_position()
```

## İşlem Maliyeti Analizi

### Fee Structure:
```python
maker_fee = 0.0001   # %0.01 (maker)
taker_fee = 0.001    # %0.1 (taker)

# 3 işlem = 3 × taker fee
total_fee = 3 * taker_fee  # %0.3

# Minimum kar eşiği
min_profit = total_fee * 1.5  # %0.45 (güvenlik payı)
```

### Net Kar Hesaplama:
$$Net\ Profit = Gross\ Profit - (3 \times Fee)$$

### Break-even Analysis:
$$R_{breakeven} = 1 + (3 \times fee)$$

Örneğin, %0.1 fee için:
$$R_{breakeven} = 1 + (3 \times 0.001) = 1.003$$

Bu derste **threshold = 1.0004** kullanılmış (%0.04), bu mantıklı bir seçim.

## Performans Optimizasyonu

### 1. Veri Yapısı Optimizasyonu
```python
# NumPy daha hızlı
import numpy as np

prices = np.array([btceur, eurusdt, btcusdt])
ratio = (prices[0] * prices[1]) / prices[2]
arb_opportunities = ratio > threshold
```

### 2. Vectorization
```python
# Loop yerine vectorized operations
df["ratio"] = (df["btceur"] * df["eurusdt"]) / df["btcusdt"]
df["profit"] = df["ratio"] - 1
opportunities = df[df["profit"] > 0.0004]
```

### 3. Parallel Processing
```python
from multiprocessing import Pool

def check_arbitrage(price_snapshot):
    # Her timestamp için kontrol et
    return calculate_profit(price_snapshot)

with Pool(4) as p:
    results = p.map(check_arbitrage, price_data)
```

## Gerçek Zamanlı Uygulama

### WebSocket ile Canlı Veri
```python
import websocket

def on_message(ws, message):
    data = json.loads(message)
    
    # Update prices
    btceur_price = data['btceur']
    eurusdt_price = data['eurusdt']
    btcusdt_price = data['btcusdt']
    
    # Check arbitrage
    ratio = (btceur_price * eurusdt_price) / btcusdt_price
    
    if ratio > 1.0004:
        execute_arbitrage()

# Connect to Binance WebSocket
ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/...")
ws.run_forever()
```

## Gelişmiş Stratejiler

### 1. Multi-Hop Arbitrage
```python
# 4+ pair arbitrage
paths = [
    ["BTC", "EUR", "USDT", "BTC"],
    ["BTC", "ETH", "USDT", "BTC"],
    ["BTC", "BNB", "USDT", "EUR", "BTC"]
]

for path in paths:
    profit = calculate_path_profit(path)
    if profit > threshold:
        execute_path(path)
```

### 2. Cross-Exchange Arbitrage
```python
# Farklı borsalar arası
binance_price = get_binance_price("BTCUSDT")
coinbase_price = get_coinbase_price("BTCUSDT")

if abs(binance_price - coinbase_price) / coinbase_price > 0.005:
    # %0.5+ fark varsa arbitraj fırsatı
    execute_cross_exchange_arb()
```

## İstatistiksel Analiz

### Fırsat Sıklığı
```python
total_samples = len(df)
arbitrage_count = len(arb)
frequency = arbitrage_count / total_samples

print(f"Arbitrage frequency: {frequency*100:.2f}%")
print(f"Average time between opportunities: {1/frequency:.1f} samples")
```

### Kar Dağılımı
```python
import matplotlib.pyplot as plt

plt.hist(df["profit_pct"], bins=50)
plt.axvline(x=0.04, color='r', linestyle='--', label='Threshold')
plt.xlabel("Profit %")
plt.ylabel("Frequency")
plt.title("Arbitrage Profit Distribution")
plt.legend()
plt.show()
```

## Gerçek Dünya Örneği

### Başarılı Arbitrage:
- **2017-2018**: Korea Premium (Kimchi Premium)
  - Kore borsalarında BTC %30+ pahalıydı
  - Büyük arbitraj fırsatları
  
### Başarısız Arbitrage:
- **Network Congestion**: 2017 Ethereum ağ tıkanıklığı
  - Gas fees çok yüksek
  - Arbitraj karlı görünse de execution maliyetli

## Yasal ve Etik Konular

### Yasal:
- ✅ Arbitraj yasal (çoğu yetki alanında)
- ⚠️ KYC/AML gereksinimleri
- ⚠️ Vergiye tabi işlemler

### Etik:
- ✅ Piyasa verimliliğine katkı
- ⚠️ Likidite çekme riski
- ⚠️ Front-running tartışması

## Teknik Detaylar

### lecture15.py:
- **Approach**: Static analysis
- **Output**: Tüm fırsatların listesi
- **Kullanım**: Tarihsel analiz

### lecture15_2.py:
- **Approach**: Dynamic simulation
- **Output**: Kümülatif kar
- **Kullanım**: Backtest

### mahmut.py:
- **Approach**: Simple loop
- **Output**: Final profit
- **Kullanım**: Hızlı test

## Sonuç ve Öneriler

### Öğrenciler İçin:
1. **Teori**: Önce matematiksel modeli anla
2. **Backtest**: Tarihsel verilerle test et
3. **Paper Trading**: Gerçek parayla test etme
4. **Risk Management**: Her zaman risk kontrolü
5. **Continuous Learning**: Piyasalar sürekli değişiyor

### Gerçek Uygulama İçin:
- Profesyonel altyapı gerekir
- Yüksek sermaye (likidite için)
- Düşük latency bağlantı
- Otomatik execution sistemi
- 7/24 monitoring

Bu ders, öğrencilere arbitraj fikirlerini anlamaları ve basit stratejiler geliştirebilmeleri için temel bilgi sağlar. Gerçek dünya uygulaması çok daha karmaşıktır ve profesyonel düzeyde altyapı gerektirir.
