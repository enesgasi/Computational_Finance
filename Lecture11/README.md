# Lecture 11 - Portföy Dengeleme (Rebalancing) Stratejisi

## İçerik
Bu ders, birden fazla kripto para varlığı içeren bir portföyün otomatik dengelenmesi (rebalancing) stratejisini öğretir. BTC, BNB, ETH ve XRP'den oluşan bir portföy optimize edilir.

## Dosyalar
- `untitled2.m` - Portföy rebalancing MATLAB scripti (60 satır)
- `BTC_USDT_year.m` - Bitcoin yıllık fiyat verileri
- `BNB_USDT_year.m` - Binance Coin yıllık fiyat verileri
- `ETH_USDT_year.m` - Ethereum yıllık fiyat verileri
- `XRP_USDT_year.m` - Ripple yıllık fiyat verileri
- `untitled2.asv` - Auto-save backup dosyası

## Script Detayları

### untitled2.m - Multi-Asset Portfolio Rebalancing

#### 1. Veri Yükleme ve Normalizasyon
```matlab
BTC_USDT_year
price1 = data1./data1(1);  % İlk güne göre normalize

BNB_USDT_year
price2 = data1./data1(1);

ETH_USDT_year
price3 = data1./data1(1);

XRP_USDT_year
price4 = data1./data1(1);
```
- Her varlığın fiyatı ilk günün fiyatına bölünür
- **Normalize fiyat**: Tüm varlıklar aynı başlangıç noktasından (1.0) başlar
- Bu sayede performans karşılaştırması kolay olur

#### 2. Fiyat Görselleştirmesi
```matlab
plot(price1)
hold on 
plot(price2)
hold on
plot(price3)
hold on
plot(price4)

legend('BTC', 'BNB', 'ETH', 'XRP', location='best')
```
- 4 varlığın yıllık performansı tek grafikte
- Hangisi daha iyi performans göstermiş görsel olarak anlaşılır

#### 3. Başlangıç Parametreleri
```matlab
margin = 0.10;                % Dengeleme eşiği: %10
price = [price1, price2, price3, price4];
amount(1:4) = 100;           % Her varlıkta 100 birim
t_f = 1/1000;                % İşlem ücreti: %0.1
```

**Portfolio Allocation:**
- Başlangıçta her varlıkta 100 birim (eşit ağırlık)
- Toplam portföy değeri = 400 birim

#### 4. Rebalancing Stratejisi
```matlab
for i = 1:365  % Her gün için
    
    % Her varlığın güncel değerini hesapla
    for k = 1:4
        value(k) = price(i, k) * amount(k);
    end    
    avg_value = mean(value);  % Ortalama değer

    % Eğer herhangi bir varlık ortalamadan %10+ sapma gösteriyorsa
    if max(value) > (avg_value)*(1+margin) || min(value) < (avg_value)*(1+margin)
        
        for k=1:4
            if value(k) > avg_value
                % Fazla olan varlığı sat
                difference = value(k) - avg_value;
                amount(k) = amount(k) - ((1 + t_f) * difference / price(i, k));
            else
                % Eksik olan varlığı al
                difference = avg_value - value(k);
                amount(k) = amount(k) + ((1 - t_f) * difference / price(i, k));
            end
        end    
    end    
end
```

### Rebalancing Mantığı

**Adım 1: Değer Hesaplama**
$$Value_k(t) = Price_k(t) \times Amount_k(t)$$

**Adım 2: Ortalama Değer**
$$\overline{Value}(t) = \frac{1}{4} \sum_{k=1}^{4} Value_k(t)$$

**Adım 3: Sapma Kontrolü**
$$\text{If } \max(Value_k) > \overline{Value} \times (1 + margin) \text{ or } \min(Value_k) < \overline{Value} \times (1 - margin)$$

**Adım 4: Rebalancing**
- **Fazla değerde:** $Amount_k = Amount_k - \frac{(1+f) \times \Delta}{Price_k}$ (SAT)
- **Eksik değerde:** $Amount_k = Amount_k + \frac{(1-f) \times \Delta}{Price_k}$ (AL)

Burada:
- $\Delta$ = Değer farkı
- $f = 0.001$ = İşlem ücreti

#### 5. Performans Hesaplama
```matlab
(sum(value) - length(value)*100) / length(value)
```
- Toplam portföy getirisi hesaplanır
- Başlangıç: 4 × 100 = 400 birim
- Final: sum(value)
- Ortalama varlık başına getiri

```matlab
(100*sum(price(i,:)) - length(value)*100) / length(value)
```
- Buy & Hold stratejisi getirisi (karşılaştırma için)

## Rebalancing Stratejisi Avantajları

### 1. Risk Yönetimi
- Tek bir varlığa aşırı maruz kalma önlenir
- Portföy diversifikasyonu korunur
- Volatilite azalır

### 2. "Buy Low, Sell High" Otomasyonu
- Düşen varlıkları otomatik alır (ucuzken)
- Yükselen varlıkları otomatik satar (pahalıyken)
- Trend takip yerine mean-reversion stratejisi

### 3. Disiplinli Yaklaşım
- Duygusal kararlar önlenir
- Sistematik yaklaşım
- Backtesting ile test edilebilir

## Strateji Parametreleri

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **margin** | 0.10 (10%) | Rebalancing tetikleyici eşik |
| **t_f** | 0.001 (0.1%) | İşlem ücreti |
| **Varlık Sayısı** | 4 | BTC, BNB, ETH, XRP |
| **Başlangıç Alloction** | Eşit (25% her biri) | Equal-weight |
| **Rebalancing Frekansı** | Günlük kontrol | Condition-triggered |

## Rebalancing Türleri

### 1. **Threshold Rebalancing** (Bu derste kullanılan)
- Sapma %10'u geçince rebalance et
- Avantaj: İşlem maliyeti düşük
- Dezavantaj: Trend kaçırma riski

### 2. **Periodic Rebalancing**
- Her ay/çeyrek düzenli rebalance
- Avantaj: Basit, öngörülebilir
- Dezavantaj: Gereksiz işlemler yapabilir

### 3. **Constant Mix Strategy**
- Sürekli sabit oran koru
- Avantaj: Maksimum diversifikasyon
- Dezavantaj: Yüksek işlem maliyeti

## Kullanılan MATLAB Fonksiyonları
- `close all` - Tüm figürleri kapat
- `clear all` - Workspace'i temizle
- `clf` - Current figure'ı temizle
- `plot()` - Grafik çizimi
- `hold on` - Grafikleri bindirme
- `legend()` - Grafik açıklaması
- `mean()` - Ortalama hesaplama
- `max()`, `min()` - Maksimum ve minimum değer
- `sum()` - Toplam
- `length()` - Dizin uzunluğu

## Öğrenilen Konular

1. **Portfolio Theory**: Modern portföy teorisi pratiği
2. **Asset Allocation**: Varlık dağılımı stratejileri
3. **Rebalancing**: Portföy dengeleme mekanizmaları
4. **Risk Management**: Çeşitlendirme ile risk azaltma
5. **Mean Reversion**: Ortalamaya dönüş stratejisi
6. **Transaction Costs**: İşlem maliyetlerinin etkisi
7. **Performance Measurement**: Portföy performans ölçümü
8. **Backtesting**: Tarihsel veri ile test

## Karşılaştırma: Rebalancing vs Buy & Hold

| Strateji | Avantajlar | Dezavantajlar |
|----------|-----------|---------------|
| **Rebalancing** | Risk kontrolü, volatilite azaltma, disiplin | İşlem maliyeti, güçlü trend'i kaçırabilir |
| **Buy & Hold** | Düşük maliyet, basit, trend'ten yararlanma | Yüksek risk, diversifikasyon kaybı |

## Performans Metrikleri (Manuel Hesaplama)

Script'te şu metrikler hesaplanabilir:
- ✅ **Total Return**: Toplam getiri
- ❌ **Sharpe Ratio**: Risk-adjusted return (manuel eklenebilir)
- ❌ **Max Drawdown**: Maksimum kayıp (manuel eklenebilir)
- ❌ **Volatility**: Standart sapma (manuel eklenebilir)
- ❌ **Number of Rebalances**: İşlem sayısı (sayaç eklenebilir)

## Gerçek Dünya Uygulaması

### Başarı Faktörleri:
- ✅ Düşük işlem ücretleri (exchange seçimi önemli)
- ✅ Likidite yüksek varlıklar
- ✅ Uzun vadeli yatırım (kısa vadede işlem maliyeti baskın)
- ✅ Volatilite yüksek piyasalar (rebalancing daha etkili)

### Dikkat Edilecekler:
- ⚠️ İşlem maliyetleri getiriyi önemli ölçüde azaltabilir
- ⚠️ Güçlü trend olan piyasalarda underperform edebilir
- ⚠️ Tax implications (vergiye tabi alım-satımlar)
- ⚠️ Slippage ve liquidity sorunları

## Optimizasyon Fırsatları

Script şu şekillerde geliştirilebilir:

1. **Dinamik Margin**: Volatiliteye göre ayarlanabilir eşik
2. **Volatility-Based Weights**: Düşük volatiliteli varlıklara daha fazla ağırlık
3. **Risk Parity**: Eşit risk katkısı stratejisi
4. **Correlation Matrix**: Korelasyonları hesaba katan optimizasyon
5. **Transaction Cost Optimization**: Maliyet-fayda analizi

## Kod İyileştirme Önerileri

```matlab
% İşlem sayısını say
rebalance_count = 0;
if max(value) > ... 
    rebalance_count = rebalance_count + 1;
end

% Portföy değerini kaydet
portfolio_value(i) = sum(value);

% Drawdown hesapla
cummax = max(portfolio_value(1:i));
drawdown(i) = (portfolio_value(i) - cummax) / cummax;
```

## Teknik Detaylar
- **Dil**: MATLAB/Octave
- **Varlıklar**: BTC, BNB, ETH, XRP
- **Zaman Dilimi**: 1 yıl (365 gün)
- **Başlangıç Sermaye**: 400 birim (her varlıkta 100)
- **Rebalancing Trigger**: ±10% sapma
- **İşlem Ücreti**: %0.1

Bu ders, öğrencilere çok varlıklı portföy yönetimi ve sistematik rebalancing stratejileri geliştirme becerisi kazandırmayı amaçlamaktadır.
