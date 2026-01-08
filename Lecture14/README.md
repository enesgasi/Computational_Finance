# Lecture 14 - Periodic Rebalancing Application

## Ödev Sorusu (MIS4321)

**Görev:** BTC/USDT, ADA/USDT ve SOL/USDT için son 1000 günlük veriyi Binance'den indirin. 3000 USDT sermaye ile her varlığa eşit ağırlıklı (1000 USDT) yatırım yapın. Periyodik rebalancing stratejilerinin karını hesaplayın:

- **Daily** (Günlük) rebalancing
- **Weekly** (Haftalık) rebalancing  
- **Monthly** (Aylık) rebalancing

**İşlem ücreti:** %0.1

---

## İçerik
Bu ders, farklı rebalancing frekanslarının (günlük, haftalık, aylık) portföy performansına etkisini analiz eder. BTC, ADA ve SOL içeren 3 varlıklı portföyde Buy & Hold ile karşılaştırmalı test yapılır.

## Dosyalar
- `atıf.py` - Rebalancing karşılaştırmalı backtest scripti (Python, 93 satır) ✅
- `mahmut.py` - Tamamlanmamış rebalancing denemesi (Python, yarım) ⚠️
- `data.php` - Binance'den veri çekme ve CSV export scripti (PHP)
- `bin_class.php` - Binance API wrapper
- `BTCUSDT_price.csv` - Bitcoin fiyat verileri
- `ADAUSDT_price.csv` - Cardano fiyat verileri
- `SOLUSDT_price.csv` - Solana fiyat verileri

## Script Detayları

### atıf.py - Profesyonel Rebalancing Backtest

#### 1. Parametre Tanımları
```python
INITIAL_CAPITAL = 3000      # Başlangıç sermayesi: $3000
FEE_RATE = 0.001           # İşlem ücreti: %0.1
ASSETS = ['BTC', 'ADA', 'SOL']  # Varlıklar
```

#### 2. Veri Yükleme ve Hazırlama
```python
def load_price_csv(path, asset):
    df = pd.read_csv(path, header=None)
    prices = df.iloc[0].astype(float)  # İlk satır = fiyat serisi
    prices = prices.reset_index(drop=True)
    return pd.DataFrame({asset: prices})

btc = load_price_csv("BTCUSDT_price.csv", "BTC")
ada = load_price_csv("ADAUSDT_price.csv", "ADA")
sol = load_price_csv("SOLUSDT_price.csv", "SOL")
```

**Özel Veri Formatı:**
- CSV dosyasında tek satır
- Her sütun bir fiyat noktası
- Transpose gerekli (satır → sütun)

#### 3. Veri Hizalama (Alignment)
```python
min_len = min(len(btc), len(ada), len(sol))

df = pd.concat([
    btc.tail(min_len),
    ada.tail(min_len),
    sol.tail(min_len)
], axis=1).reset_index(drop=True)

df = df.tail(1000)  # Son 1000 veri noktası
```
- Farklı uzunluktaki serileri eşitle
- Pandas DataFrame'e dönüştür
- Son 1000 günü al (test için)

#### 4. Buy & Hold Stratejisi
```python
def buy_and_hold(prices):
    # Başlangıçta eşit ağırlıklı al ve tut
    holdings = {a: (INITIAL_CAPITAL / 3) / prices[a].iloc[0] 
                for a in ASSETS}
    
    # Final değer
    return sum(holdings[a] * prices[a].iloc[-1] for a in ASSETS)
```

**Mantık:**
- $3000 ÷ 3 = $1000 her varlığa
- İlk fiyattan miktar hesapla
- Hiç satma, sonuna kadar tut
- Final değeri hesapla

#### 5. Rebalancing Stratejisi
```python
def rebalance_backtest(prices, freq):
    # Başlangıç holding
    holdings = {a: (INITIAL_CAPITAL / 3) / prices[a].iloc[0] 
                for a in ASSETS}
    total_fee = 0

    for t in range(1, len(prices)):
        # Her 'freq' günde bir rebalance et
        if t % freq == 0:
            # Mevcut toplam değer
            value = sum(holdings[a] * prices[a].iloc[t] for a in ASSETS)
            target = value / 3  # Eşit ağırlık hedefi
            
            traded = 0
            for a in ASSETS:
                curr = holdings[a] * prices[a].iloc[t]
                diff = target - curr
                traded += abs(diff)  # Toplam işlem hacmi
                holdings[a] = target / prices[a].iloc[t]
            
            # İşlem ücreti hesapla
            fee = traded * FEE_RATE
            total_fee += fee
            
            # Ücreti her varlıktan düş
            for a in ASSETS:
                holdings[a] -= (fee / 3) / prices[a].iloc[t]

    # Final değer
    final_value = sum(holdings[a] * prices[a].iloc[-1] for a in ASSETS)
    return final_value, total_fee
```

**Rebalancing Mekanizması:**
1. Her `freq` günde bir:
   - Mevcut portföy değerini hesapla
   - Her varlık için hedef = Toplam / 3 (eşit ağırlık)
   - Fazla olanı sat, eksik olanı al
2. İşlem hacmini hesapla
3. İşlem ücreti kes
4. Yeni holding'leri güncelle

#### 6. Karşılaştırmalı Test
```python
bh = buy_and_hold(df)
daily, daily_fee = rebalance_backtest(df, 1)      # Günlük
weekly, weekly_fee = rebalance_backtest(df, 7)    # Haftalık
monthly, monthly_fee = rebalance_backtest(df, 30) # Aylık

results = pd.DataFrame({
    "Strategy": ["Buy & Hold", "Daily", "Weekly", "Monthly"],
    "Final Value (USDT)": [bh, daily, weekly, monthly],
    "Total Fees (USDT)": [0, daily_fee, weekly_fee, monthly_fee]
})

results["Rebalancing Profit vs Buy&Hold"] = results["Final Value (USDT)"] - bh
```

**Output Örneği:**
```
Strategy      Final Value  Total Fees  Profit vs B&H
Buy & Hold    4500         0           0
Daily         4200         250        -300
Weekly        4600         35         +100
Monthly       4550         12         +50
```

---

### mahmut.py - Basit Haftalık Rebalancing Scripti

Bu script, basit ve minimal bir yaklaşımla haftalık rebalancing stratejisini uygular. Ödev sorusunun gereksinimlerini karşılar.

#### 1. Veri Yükleme ve Hazırlama
```python
price_btc = pd.read_csv("BTCUSDT_price.csv", header=None)
price_ada = pd.read_csv("ADAUSDT_price.csv", header=None)
price_sol = pd.read_csv("SOLUSDT_price.csv", header=None)

price_btc = price_btc.T
price_ada = price_ada.T
price_sol = price_sol.T

price_btc = price_btc.iloc[:, 0]
price_ada = price_ada.iloc[:, 0]
price_sol = price_sol.iloc[:, 0]
```

#### 2. Veri Hizalama
```python
min_len = min(len(price_btc), len(price_ada), len(price_sol))
price_btc = price_btc[:min_len]
price_ada = price_ada[:min_len]
price_sol = price_sol[:min_len]
```

#### 3. Normalizasyon ve Görselleştirme
```python
price_btc_norm = price_btc / price_btc.iloc[0]
price_ada_norm = price_ada / price_ada.iloc[0]
price_sol_norm = price_sol / price_sol.iloc[0]

plt.figure(figsize=(12, 6))
plt.plot(price_btc_norm, label='BTCUSDT')
plt.plot(price_ada_norm, label='ADAUSDT')
plt.plot(price_sol_norm, label='SOLUSDT')
plt.legend()
plt.show()
```

#### 4. Başlangıç Parametreleri
```python
prices = np.column_stack((price_btc.values, price_ada.values, price_sol.values))

# Her varlığa 1000$ yatırım
initial_value = 1000
amounts = np.array([
    initial_value / prices[0, 0],  # BTC amount
    initial_value / prices[0, 1],  # ADA amount
    initial_value / prices[0, 2]   # SOL amount
])

com_rate = 0.001  # İşlem ücreti %0.1
m, n = prices.shape
```

**Önemli:** Normalize edilmiş fiyatlar sadece görselleştirme için kullanılır. Rebalancing hesaplamalarında orijinal fiyatlar (`prices`) kullanılır.

#### 5. Haftalık Rebalancing Döngüsü
```python
for i in range(m):
    values = prices[i] * amounts 
    average = np.mean(values)
    
    if i % 7 == 0:  # Her 7 günde bir
        if np.max(values) > average * (1 + com_rate) or \
           np.min(values) < average * (1 - com_rate):
            
            for k in range(n):
                if values[k] > average:
                    difference = values[k] - average 
                    amounts[k] = amounts[k] - (difference * (1 + com_rate)) / prices[i, k]
                else:
                    difference = average - values[k]
                    amounts[k] = amounts[k] + (difference * (1 - com_rate)) / prices[i, k]
```

**Rebalancing Mantığı:**
- Her 7 günde bir kontrol et
- Eğer herhangi bir varlık ortalamadan ±%0.1'den fazla sapıyorsa rebalance et
- Fazla olan varlığı sat (ortalamanın üstünde)
- Eksik olan varlığı al (ortalamanın altında)
- İşlem ücretini hesaba kat

#### 6. Sonuç Hesaplama
```python
final_values = prices[-1] * amounts
final_total = np.sum(final_values)
initial_total = 3 * initial_value

profit_pct = ((final_total - initial_total) / initial_total) * 100

print("Final value:", final_total)
print("Profit percentage:", profit_pct)
```

**Çıktı Formatı:**
```
Final value: 3450.75
Profit percentage: 15.02
```

### mahmut.py vs atıf.py Karşılaştırması

| Özellik | mahmut.py | atıf.py |
|---------|-----------|---------|
| **Yaklaşım** | Basit threshold | Çoklu frekans karşılaştırması |
| **Rebalancing** | Haftalık + threshold | Daily/Weekly/Monthly seçenekleri |
| **Kod Uzunluğu** | ~80 satır | ~93 satır |
| **Threshold** | %0.1 sapma | Frekansa göre otomatik |
| **Karşılaştırma** | Yok | Buy & Hold ile karşılaştırılır |
| **Çıktı** | Final value + fees | DataFrame (4 strateji) |
| **Grafik** | Fiyat grafiği | Yok |
| **Kullanım** | Basit test | Profesyonel analiz |

### Hangi Script Ne Zaman Kullanılır?

**mahmut.py kullanın:**
- ✅ Hızlı test için
- ✅ Tek strateji denemek için
- ✅ Görsel analiz istiyorsanız
- ✅ Basit implementasyon yeterli

**atıf.py kullanın:**
- ✅ Çoklu strateji karşılaştırması için
- ✅ Buy & Hold ile performans karşılaştırması
- ✅ Farklı rebalancing frekanslarını test etmek için
- ✅ Detaylı raporlama gerekiyorsa

---

### data.php - Veri Çekme Scripti

#### 1. Binance'den Veri Çekme
```php
require("bin_class.php");
$bnb = new Binance\binali($key, $secret, ['useServerTime' => True]);

$data = $bnb->candlesticks('BTCUSDT', '1d', 1000);  // 1000 günlük mum verisi
```

#### 2. Kapanış Fiyatlarını Çıkar
```php
$keys = array_keys($data);
for($i = 0; $i < count($keys); $i++){
    $price[$i] = $data[$keys[$i]]['close'];
}
```

#### 3. CSV'ye Kaydet
```php
$file = fopen('BTC_USDT_day.csv','w');
fputcsv($file, $price);  // Tek satır, virgülle ayrılmış
fclose($file);
```

**CSV Formatı:**
```
45000.50,45123.20,44890.33,...
```
- Tek satır
- Her değer virgülle ayrılmış
- Python'da özel parsing gerekir

## Rebalancing Frekansı Karşılaştırması

### 1. Daily (Günlük) Rebalancing
**Avantajlar:**
- ✅ En sık dengeleme
- ✅ Hedef ağırlıklardan minimum sapma
- ✅ Risk kontrolü maksimum

**Dezavantajlar:**
- ❌ En yüksek işlem maliyeti
- ❌ Aşırı trading (overtrading)
- ❌ Tax implications (vergiye tabi işlemler)
- ❌ Execution risk

### 2. Weekly (Haftalık) Rebalancing
**Avantajlar:**
- ✅ Dengeli maliyet-fayda
- ✅ Makul işlem sıklığı
- ✅ Trend'leri kaçırmaz

**Dezavantajlar:**
- ⚠️ Orta seviye maliyet
- ⚠️ Volatil piyasalarda geç kalabilir

### 3. Monthly (Aylık) Rebalancing
**Avantajlar:**
- ✅ En düşük işlem maliyeti
- ✅ Trend'lerden faydalanır
- ✅ Basit, kolay yönetim

**Dezavantajlar:**
- ❌ Hedef ağırlıklardan büyük sapmalar
- ❌ Risk kontrolü zayıf
- ❌ Hızlı piyasalarda yetersiz

### 4. Buy & Hold
**Avantajlar:**
- ✅ Sıfır işlem maliyeti
- ✅ Kazanan varlıktan maksimum fayda
- ✅ Basit

**Dezavantajlar:**
- ❌ Risk yönetimi yok
- ❌ Tek varlığa aşırı maruz kalma
- ❌ Diversifikasyon kaybı

## Performans Analizi

### Hangi Strateji Ne Zaman İyi?

| Piyasa Koşulu | En İyi Strateji | Sebep |
|---------------|----------------|--------|
| **Yüksek Volatilite** | Weekly/Monthly | Düşük maliyet, trend'den fayda |
| **Düşük Volatilite** | Daily | Sapma az, maliyet önemsiz |
| **Bull Market** | Buy & Hold | Tüm varlıklar yükseliyor |
| **Bear Market** | Daily/Weekly | Risk kontrolü kritik |
| **Sideways Market** | Weekly | Rebalancing en etkili |

## Kullanılan Kütüphaneler

### Python:
- **pandas**: DataFrame operasyonları
  - `read_csv()`: CSV okuma
  - `concat()`: Veri birleştirme
  - `tail()`: Son n satır
- **numpy**: Sayısal hesaplamalar
- **matplotlib**: Görselleştirme (mahmut.py'de)

### PHP:
- **Binance API**: Veri çekme
- `fopen()`, `fputcsv()`: Dosya işlemleri
- `array_keys()`: Dizi anahtarları

## Öğrenilen Konular

1. **Rebalancing Frequency**: Dengeleme sıklığı optimizasyonu
2. **Transaction Cost Analysis**: İşlem maliyeti analizi
3. **Performance Attribution**: Performans kaynaklarını belirleme
4. **Buy & Hold vs Active**: Pasif vs aktif strateji karşılaştırması
5. **Data Alignment**: Farklı uzunluktaki serileri hizalama
6. **Backtesting Framework**: Geriye dönük test altyapısı
7. **CSV Data Handling**: Özel format veri işleme
8. **Portfolio Drift**: Portföy sapması analizi

## İşlem Maliyeti Analizi

### Maliyet Hesaplama:
$$\text{Total Fee} = \sum_{t \in \text{Rebalance Days}} \left( \sum_{i=1}^{3} |Target_i - Current_i| \right) \times f$$

Burada:
- $f = 0.001$ (işlem ücreti oranı)
- $Target_i$ = Hedef değer (Toplam/3)
- $Current_i$ = Mevcut değer

### Örnek:
- Portföy değeri: $4500
- Hedef: BTC=$1500, ADA=$1500, SOL=$1500
- Mevcut: BTC=$2000, ADA=$1200, SOL=$1300
- Traded: $500 + $300 + $200 = $1000
- Fee: $1000 × 0.001 = $1

## Risk Metrikleri (Manuel Eklenebilir)

```python
# Volatility
returns = df.pct_change()
volatility = returns.std() * np.sqrt(252)

# Sharpe Ratio
risk_free = 0.02  # %2 yıllık
sharpe = (returns.mean() * 252 - risk_free) / volatility

# Max Drawdown
cumulative = (1 + returns).cumprod()
running_max = cumulative.cummax()
drawdown = (cumulative - running_max) / running_max
max_dd = drawdown.min()
```

## Optimizasyon Fırsatları

### 1. Threshold-Based Rebalancing
```python
# Sapmaya göre rebalance et, zamana göre değil
threshold = 0.05  # %5 sapma
if max_deviation > threshold:
    rebalance()
```

### 2. Volatility-Adjusted Frequency
```python
# Volatilite yüksekse daha sık rebalance
if current_volatility > avg_volatility * 1.5:
    freq = 3  # 3 günde bir
else:
    freq = 7  # 7 günde bir
```

### 3. Asymmetric Rebalancing
```python
# Sadece büyük sapmalarda rebalance
if abs(deviation) > 0.10:  # %10
    rebalance()
```

## Gerçek Dünya Uygulaması

### Pratik Öneriler:
1. **Retail Investor**: Aylık rebalancing (düşük maliyet)
2. **Active Trader**: Haftalık rebalancing (dengeli)
3. **Institutional**: Günlük + threshold (profesyonel)
4. **Long-term HODLer**: Buy & Hold

### Dikkat Edilecekler:
- ⚠️ Vergi sonuçları (her alım-satım vergiye tabi)
- ⚠️ Slippage (büyük emirlerde fiyat kayması)
- ⚠️ Gas fees (DeFi'da yüksek olabilir)
- ⚠️ Exchange downtime riski

## Kod İyileştirmeleri

### atıf.py için Eklemeler:
```python
# Performans grafikleri
import matplotlib.pyplot as plt

def plot_equity_curve(prices, holdings, freq):
    equity = []
    for t in range(len(prices)):
        value = sum(holdings[a][t] * prices[a].iloc[t] for a in ASSETS)
        equity.append(value)
    
    plt.plot(equity, label=f"{freq}-day Rebalancing")
    plt.xlabel("Days")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.show()

# Drawdown analizi
def calculate_drawdown(equity_curve):
    running_max = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - running_max) / running_max
    return drawdown

# Win rate
def calculate_win_rate(returns):
    return (returns > 0).sum() / len(returns)
```

## Teknik Detaylar

### atıf.py (Çalışan Script):
- **Dil**: Python 3
- **Varlıklar**: BTC, ADA, SOL
- **Sermaye**: $3000
- **İşlem Ücreti**: %0.1
- **Test Dönemi**: Son 1000 gün
- **Stratejiler**: 4 (B&H, Daily, Weekly, Monthly)

### data.php:
- **API**: Binance REST
- **Timeframe**: 1 gün (1d)
- **Veri Sayısı**: 1000 mum
- **Format**: CSV (tek satır)

## Sonuç ve Öneriler

### Genel Bulgular:
1. **İşlem maliyeti kritik**: Çok sık rebalancing zararlı olabilir
2. **Piyasa koşullarına bağlı**: Tek bir "best" strateji yok
3. **Threshold-based daha iyi**: Zamana göre değil, sapmaya göre
4. **Backtesting şart**: Canlı işlem öncesi test edilmeli

### Öğrenciler İçin:
Bu ders, portföy yönetiminde **timing vs transaction cost trade-off**'unu anlamak için mükemmel bir örnektir. Farklı stratejileri karşılaştırarak optimal rebalancing politikası geliştirme becerisi kazandırır.
