# Lecture 10 - Arbitraj Trading: BTC vs WBTC Fiyat Paritesi

## İçerik
Bu ders, kripto para piyasalarında arbitraj fırsatlarını tespit edip otomatik trading yapma konusunu işler. BTC (Bitcoin) ve WBTC (Wrapped Bitcoin) arasındaki fiyat farklılıklarından kar elde etme stratejisi gösterilir.

## Dosyalar
- `lec10.php` - Gerçek zamanlı arbitraj bot scripti (PHP)
- `lec10.m` - Tarihsel veri üzerinde arbitraj simülasyonu (MATLAB)
- `bin_class.php` - Binance API wrapper sınıfı
- `BTC_USDT_hour.m` - BTC/USDT saatlik fiyat verileri
- `WBTC_USDT_hour.m` - WBTC/USDT saatlik fiyat verileri
- `WBTC_USDT_day.m` - WBTC/USDT günlük fiyat verileri

## Script Detayları

### lec10.php - Gerçek Zamanlı Arbitraj Bot

#### 1. Binance API Bağlantısı
```php
require("bin_class.php");
$bnb = new Binance\binali($key, $secret, ['useServerTime'=>True]);
```
- Binance API'sine bağlanır
- Sunucu zamanı senkronizasyonu aktif

#### 2. Başlangıç Parametreleri
```php
$balance1 = 1;    // BTC bakiyesi (başlangıç: 1 BTC)
$balance2 = 0;    // WBTC bakiyesi (başlangıç: 0)
$t_f = 1/1000;    // İşlem ücreti (0.1%)
```

#### 3. Sonsuz Döngü ile Fiyat İzleme
```php
while(1){
    $ticker = $bnb->bookPrices();
    $b_price = $ticker['BTCUSDT']['bid'];  // BTC fiyatı
    $w_price = $ticker['WBTCUSDT']['bid']; // WBTC fiyatı
    $price_ratio = $b_price/$w_price;
    ...
    sleep(15);  // 15 saniye bekle
}
```
- Her 15 saniyede bir fiyatlar güncellenir
- Bid (alış) fiyatları kullanılır

#### 4. Arbitraj Stratejisi
```php
// BTC pahalıysa → BTC sat, WBTC al
if ($price_ratio > (1 + 2*$t_f) and $balance1 > 0){
    echo('Sell BTC and Buy WBTC');
    // $bnb->sell("BTCUSDT", 1, $b_price);
    // $bnb->buy("WBTCUSDT", $quantity, $w_price);
}

// WBTC pahalıysa → WBTC sat, BTC al
if ($price_ratio < (1 - 2*$t_f) and $balance2 > 0){
    echo('Sell WBTC and Buy BTC');
}
```

**Arbitraj Mantığı:**
- Normal koşulda BTC/WBTC oranı ≈ 1 olmalı
- Eğer oran > 1.002 ise BTC pahalı → BTC sat, WBTC al
- Eğer oran < 0.998 ise WBTC pahalı → WBTC sat, BTC al
- İşlem ücreti (%0.1) her iki yönde de hesaba katılır

**Not:** Gerçek alım-satım kodları yorum satırında (test için)

---

### lec10.m - MATLAB Arbitraj Simülasyonu

#### 1. Veri Yükleme (Saatlik)
```matlab
BTC_USDT_hour      % Script dosyası, price1 değişkenini yükler
price1 = data1;     % BTC fiyatı
WBTC_USDT_hour     
price2 = data1;     % WBTC fiyatı
```

#### 2. Fiyat Görselleştirmesi
```matlab
figure(1)
plot(price1, 'b');  % Mavi: BTC
hold on;
plot(price2,'r');   % Kırmızı: WBTC
legend('BTC_USDT','WBTC_USDT');
```

#### 3. Fiyat Oranı Analizi
```matlab
price_ratio = price1./price2;
figure(2)
plot(price_ratio)
```
- BTC/WBTC oranının zaman içindeki değişimi
- Arbitraj fırsatlarını gösterir

#### 4. Arbitraj Simülasyonu
```matlab
balance1 = 1;      % Başlangıç: 1 BTC
balance2 = 0;      % Başlangıç: 0 WBTC
t_f = 1/1000;      % İşlem ücreti: %0.1

for i=1:length(price_ratio)
    % BTC pahalıysa
    if(price_ratio(i) > (1+2*t_f) & balance1 > 0)
        display('Sell BTC and Buy WBTC')
        balance2 = (balance1 * price_ratio(i)) * (1-2*t_f);
        balance1 = 0;
    end
    
    % WBTC pahalıysa
    if(price_ratio(i) < (1-2*t_f) & balance2 > 0)
        display('Sell WBTC and Buy BTC')
        balance1 = (balance2 / price_ratio(i)) * (1-2*t_f);
        balance2 = 0;
    end
end

final_balance = balance1 + balance2
```

#### 5. Günlük Veri Simülasyonu (İkinci Bölüm)
```matlab
BTC_USDT_day
price1 = data1(51:1000);  % İlk 50 gün atlanır
WBTC_USDT_day
price2 = data1;
```
- Günlük verilerle aynı strateji test edilir
- Daha uzun dönem performansı değerlendirilir

## Arbitraj Stratejisi Detayları

### Matematiksel Model

**Fiyat Oranı:**
$$r(t) = \frac{P_{BTC}(t)}{P_{WBTC}(t)}$$

**Alım-Satım Koşulları:**
- **BTC Sat, WBTC Al:** $r(t) > 1 + 2f$
- **WBTC Sat, BTC Al:** $r(t) < 1 - 2f$

Burada $f = 0.001$ (işlem ücreti)

**Kar Hesaplaması (BTC → WBTC → BTC):**
$$Balance_{final} = Balance_{initial} \times r(t) \times (1-f) \times \frac{1}{r(t+\Delta t)} \times (1-f)$$

### İşlem Ücreti Etkisi
- Her işlemde %0.1 ücret kesilir
- İki yönlü işlem → toplam %0.2 maliyet
- Arbitraj fırsatı ancak fiyat farkı > %0.2 ise karlı

## Kullanılan Kütüphaneler

### PHP:
- `bin_class.php` - Binance API wrapper
- Binance REST API

### MATLAB:
- `plot()` - Grafik çizimi
- `hold on` - Grafikleri üst üste bindirme
- `legend()` - Grafik açıklamaları
- `display()` - Konsol çıktısı

## Öğrenilen Konular

1. **Arbitraj Trading**: Farklı varlıklar arası fiyat farklılıklarından kar
2. **Market Inefficiency**: Piyasa verimsizliklerini tespit etme
3. **Algorithmic Trading**: Otomatik alım-satım botları
4. **Transaction Costs**: İşlem maliyetlerinin stratejiye etkisi
5. **Pair Trading**: Korelasyonlu varlıklar arası trading
6. **Real-time Monitoring**: Gerçek zamanlı piyasa takibi
7. **Backtesting**: Tarihsel verilerle strateji testi
8. **Risk Management**: Bakiye kontrolü ve pozisyon yönetimi

## BTC vs WBTC Nedir?

- **BTC (Bitcoin)**: Orijinal Bitcoin blockchain'inde çalışan kripto para
- **WBTC (Wrapped Bitcoin)**: Ethereum blockchain'inde ERC-20 token olarak BTC
- **1 WBTC = 1 BTC** (teorik olarak)
- **Farklı blockchain'ler** → Arz-talep farklılıkları → Arbitraj fırsatı

## Arbitraj Türleri

1. **Statistical Arbitrage**: İstatistiksel modellere dayalı
2. **Triangular Arbitrage**: Üç varlık arası
3. **Cross-Exchange Arbitrage**: Farklı borsalar arası
4. **Pair Trading**: Bu derste kullanılan yöntem

## Risk Faktörleri

1. **Execution Risk**: Emir gerçekleşmeden fiyat değişebilir
2. **Slippage**: Gerçek işlem fiyatı beklenenden farklı olabilir
3. **Latency**: Network gecikmesi fırsatı kaçırabilir
4. **Liquidity Risk**: Yeterli alıcı/satıcı olmayabilir
5. **Exchange Risk**: Borsa teknik sorun yaşayabilir

## Optimizasyon Stratejileri

1. **Threshold Optimization**: İşlem eşiklerini optimize etme
2. **Fee Structure**: İşlem ücretlerini minimize etme
3. **Position Sizing**: Optimal işlem miktarı belirleme
4. **Risk-Reward Ratio**: Risk-getiri dengesini ayarlama

## Gerçek Dünya Uygulaması

### Başarı Faktörleri:
- ✅ Düşük latency (hızlı internet bağlantısı)
- ✅ API rate limit yönetimi
- ✅ Güvenilir sunucu (24/7 çalışma)
- ✅ Yedek sermaye (unexpected costs)
- ✅ Stop-loss mekanizması

### Zorluklar:
- ⚠️ Yüksek rekabet (HFT firmalarıyla)
- ⚠️ Giderek kapanan arbitraj fırsatları
- ⚠️ Teknik aksaklık riskleri
- ⚠️ Sermaye gereksinimleri

## Teknik Detaylar

### PHP Script:
- **Çalışma Modu**: Real-time
- **Update Frequency**: 15 saniye
- **API**: Binance REST API
- **Trading Pair**: BTCUSDT, WBTCUSDT

### MATLAB Script:
- **Çalışma Modu**: Backtesting
- **Veri**: Saatlik ve günlük OHLCV
- **Zaman Aralığı**: 1000+ veri noktası
- **Görselleştirme**: 2 figür (fiyat + oran)

## Performans Metrikleri
- **Final Balance**: Stratejinin toplam getirisi
- **Number of Trades**: İşlem sayısı
- **Win Rate**: Kazanan işlem oranı (manuel hesaplama gerekir)
- **Max Drawdown**: Maksimum düşüş (manuel hesaplama gerekir)

Bu ders, öğrencilere gerçek dünya kripto para arbitraj stratejileri geliştirme ve test etme becerisi kazandırmayı amaçlamaktadır.
