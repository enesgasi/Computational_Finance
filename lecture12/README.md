# Lecture 12 - Mean Reversion Trading: Z-Score Stratejisi

## İçerik
Bu ders, pair trading (çift trading) ve mean reversion (ortalamaya dönüş) stratejisini öğretir. ETH ve XRP fiyat oranının istatistiksel analizine dayalı otomatik trading sistemi geliştirilir.

## Dosyalar
- `lec12.m` - Z-score analizi ve giriş-çıkış sinyalleri (MATLAB, 100 satır)
- `mean_reversion.php` - Gerçek zamanlı mean reversion trading bot (PHP, 115 satır)
- `main.py` - Boş Python dosyası (muhtemelen ileride kullanılacak)
- `bin_class.php` - Binance API wrapper
- `ETH_USDT_2023.m` - Ethereum 2023 fiyat verileri
- `XRP_USDT_2023.m` - Ripple 2023 fiyat verileri

## Script Detayları

### lec12.m - Statistical Arbitrage Analizi

#### 1. Veri Yükleme
```matlab
XRP_USDT_2023;
Price1 = data1;   % XRP fiyatı

ETH_USDT_2023;
Price2 = data1;   % ETH fiyatı
```

#### 2. Normalizasyon
```matlab
Price1_n = Price1 ./ Price1(1);  % İlk güne göre normalize
Price2_n = Price2 ./ Price2(1);
```
- Her iki varlık da 1.0'dan başlar
- Performans karşılaştırması kolaylaşır

#### 3. Fiyat Oranı ve Z-Score Hesaplama
```matlab
ratio = Price1 ./ Price2;      % XRP/ETH oranı
mu = mean(ratio);              % Ortalama
sigma = std(ratio);            % Standart sapma
z = (ratio - mu) ./ sigma;     % Z-score
```

**Z-Score Formülü:**
$$Z(t) = \frac{Ratio(t) - \mu}{\sigma}$$

**Z-Score Yorumu:**
- $Z > 0$: Oran ortalamanın üstünde (XRP pahalı)
- $Z < 0$: Oran ortalamanın altında (XRP ucuz)
- $|Z| > 2$: İstatistiksel olarak anormal (arbitraj fırsatı)

#### 4. Görselleştirme (3 Alt Grafik)
```matlab
% 1) Normalize Fiyatlar
subplot(3,1,1)
plot(Price2_n, 'b'); hold on
plot(Price1_n, 'g')
title('Normalized Price Comparison (ETH vs XRP)')

% 2) Fiyat Oranı
subplot(3,1,2)
plot(ratio, 'k')
title('XRP / ETH Price Ratio')

% 3) Z-Score
subplot(3,1,3)
plot(z, 'y'); hold on
yline(1,  'r--')    % Üst eşik
yline(-1, 'r--')    # Alt eşik
yline(0,  'k-')     % Ortalama
title('Z-Score of XRP / ETH Ratio')
```

#### 5. Trading Sinyalleri
```matlab
entry_th = 1;      % Pozisyon açma eşiği
exit_th = 0.5;     % Pozisyon kapatma eşiği

in_position = 0;
entry = [];
exit = [];

for t = 1:length(z)
    % ENTRY: Z-score > 1 veya < -1
    if in_position == 0 && abs(z(t)) > entry_th
        entry = [entry; t];
        in_position = 1;
    end
    
    % EXIT: Z-score ortalamaya döndü (< 0.5)
    if in_position == 1 && abs(z(t)) < exit_th
        exit = [exit; t];
        in_position = 0;
    end
end
```

**Trading Logic:**
- **Entry Condition**: $|Z| > 1$ (ortalamadan 1 std. sapma uzaklaştı)
- **Exit Condition**: $|Z| < 0.5$ (ortalamaya yaklaştı)

**Pozisyon Yönü:**
- $Z > 1$: XRP pahalı → XRP short, ETH long
- $Z < -1$: XRP ucuz → XRP long, ETH short

#### 6. Sinyal Görselleştirmesi
```matlab
figure
plot(z,'b','LineWidth',1.2)
hold on

% Threshold çizgileri
yline(1,'r--');      % Entry pozitif
yline(-1,'r--');     % Entry negatif
yline(0.5,'g--');    % Exit pozitif
yline(-0.5,'g--');   % Exit negatif

% Giriş ve çıkış noktaları
plot(entry, z(entry), 'ro', 'MarkerSize',8, 'LineWidth',2)  % Kırmızı daire
plot(exit,  z(exit),  '^', 'MarkerSize',8, 'LineWidth',2)   % Üçgen
```

---

### mean_reversion.php - Gerçek Zamanlı Trading Bot

#### 1. API Bağlantısı ve Veri Çekme
```php
require("bin_class.php");
$bnb = new Binance\binali($key, $secret, ['useServerTime'=>True]);

// Son 365 günlük günlük mum verileri
$data1 = $bnb->candlesticks('ETHUSDT','1d',365);
$data2 = $bnb->candlesticks('XRPUSDT','1d',365);
```

#### 2. Tarihsel Fiyat Oranı Hesaplama
```php
for($i=0; $i<count($keys1); $i++){
    $close1 = $data1[$keys1[$i]]['close'];  // ETH kapanış
    $close2 = $data2[$keys2[$i]]['close'];  // XRP kapanış
    
    $price1[$i] = $close1;
    $price2[$i] = $close2;
    $ratio[$i] = $close1/$close2;  // ETH/XRP oranı
}
```

#### 3. İstatistiksel Parametreler
```php
$mean1 = array_sum($ratio)/count($ratio);  // Ortalama

function standard_deviation($aValues, $bSample = false) {
    $fMean = array_sum($aValues) / count($aValues);
    $fVariance = 0.0;
    foreach ($aValues as $i) {
        $fVariance += pow($i - $fMean, 2);
    }
    $fVariance /= ($bSample ? count($aValues) - 1 : count($aValues));
    return (float) sqrt($fVariance);
}

$std1 = standard_deviation($ratio);
```

#### 4. Gerçek Zamanlı Z-Score Monitoring
```php
while(1){
    $binance_ticker = $bnb->bookPrices();
    $eth_price = $binance_ticker['ETHUSDT']['bid'];
    $xrp_price = $binance_ticker['XRPUSDT']['bid'];
    
    // Anlık Z-score hesapla
    $zscore = ($eth_price/$xrp_price - $mean1) / $std1;
    
    echo("<br> ZSCORE<br>");
    echo($zscore);
    
    // Trading sinyalleri
    if (abs($zscore) > 1){
        echo("<br> Enter<br>");  // Pozisyon aç
    }
    if (abs($zscore) < 0.5){
        echo("<br> Exit <br>");  // Pozisyon kapat
    }
    
    sleep(5);  // 5 saniye bekle
}
```

**Bot Mantığı:**
1. Tarihsel verilerden ortalama ve std hesapla
2. Her 5 saniyede bir anlık fiyatları çek
3. Anlık Z-score hesapla
4. Eşik değerlerini kontrol et
5. Entry/Exit sinyalleri üret

#### 5. Veri Export (Yorum Satırında)
```php
// CSV formatında export
$file = fopen('series.csv','w');
fputcsv($file, $price);

// MATLAB formatında export
$file3 = fopen('BTC_USDT_day.m','w');
fwrite($file3, "data1=[");
for($i=0; $i<count($keys); $i++){
    fwrite($file3, "$close\n");
}
fwrite($file3, "];");
```

## Mean Reversion Stratejisi

### Temel Prensipler

1. **Cointegration (Eşbütünleşme)**
   - İki varlık uzun dönemde birlikte hareket eder
   - Kısa dönemde sapmalar olabilir
   - Sapmalar geçicidir, ortalamaya döner

2. **Statistical Arbitrage**
   - İstatistiksel anormalliklerden kar
   - Risk nötr pozisyonlar (long + short)
   - Düşük risk, orta getiri

3. **Z-Score Tabanlı Sinyal**
   - Objektif, matematiksel yaklaşım
   - Overfit riski düşük
   - Backtesting kolay

### Matematiksel Model

**Spread (Fark):**
$$S(t) = \log(P_1(t)) - \beta \log(P_2(t))$$

Bu derste basitleştirilmiş:
$$S(t) = \frac{P_1(t)}{P_2(t)}$$

**Z-Score:**
$$Z(t) = \frac{S(t) - \mu_S}{\sigma_S}$$

**Trading Rules:**
- $Z > +1$: Short spread (P1 sat, P2 al)
- $Z < -1$: Long spread (P1 al, P2 sat)
- $|Z| < 0.5$: Pozisyon kapat

## Kullanılan Teknolojiler

### MATLAB:
- `subplot()` - Çoklu grafik düzeni
- `yline()` - Yatay çizgi
- `std()` - Standart sapma
- `mean()` - Ortalama
- `abs()` - Mutlak değer

### PHP:
- `array_sum()` - Dizi toplamı
- `count()` - Eleman sayısı
- `pow()` - Üs alma
- `sqrt()` - Karekök
- `sleep()` - Bekleme
- `while(1)` - Sonsuz döngü

## Öğrenilen Konular

1. **Pair Trading**: Çift varlık trading stratejisi
2. **Mean Reversion**: Ortalamaya dönüş teorisi
3. **Z-Score Analysis**: İstatistiksel sapma analizi
4. **Cointegration**: Eşbütünleşme kavramı
5. **Statistical Arbitrage**: İstatistiksel arbitraj
6. **Risk-Neutral Strategy**: Risk nötr pozisyon alma
7. **Threshold Optimization**: Eşik değer optimizasyonu
8. **Real-time Monitoring**: Gerçek zamanlı izleme
9. **Signal Generation**: Otomatik sinyal üretimi

## Strateji Parametreleri

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Entry Threshold** | ±1σ | Pozisyon açma eşiği |
| **Exit Threshold** | ±0.5σ | Pozisyon kapatma eşiği |
| **Lookback Period** | 365 gün | İstatistik hesaplama dönemi |
| **Update Frequency** | 5 saniye | Fiyat güncelleme sıklığı |
| **Asset Pair** | ETH/XRP | Trading çifti |

## Avantajlar ve Dezavantajlar

### Avantajlar:
- ✅ Market direction neutral (piyasa yönü önemsiz)
- ✅ Düşük risk (long + short)
- ✅ İstatistiksel temele dayalı
- ✅ Otomatize edilebilir
- ✅ Backtesting kolay

### Dezavantajlar:
- ⚠️ Cointegration bozulabilir
- ⚠️ Regime change (piyasa rejim değişikliği)
- ⚠️ İşlem maliyetleri kritik
- ⚠️ Execution risk (slippage)
- ⚠️ Margin requirements (teminat gereksinimleri)

## Risk Yönetimi

### Önemli Riskler:
1. **Divergence Risk**: Spread sürekli açılabilir
2. **Liquidity Risk**: Pozisyon kapatma zorluğu
3. **Model Risk**: İstatistiksel model başarısız olabilir
4. **Execution Risk**: Fiyat kayması

### Risk Azaltma:
- Stop-loss kullanımı
- Pozisyon büyüklüğü limiti
- Cointegration testleri (Engle-Granger, Johansen)
- Rolling window (dinamik parametre güncellemesi)

## İyileştirme Önerileri

1. **Cointegration Test**: ADF testi ile pair seçimi
2. **Dynamic Thresholds**: Volatilite bazlı eşikler
3. **Position Sizing**: Kelly criterion
4. **Stop Loss**: Maksimum kayıp limiti
5. **Half-Life Calculation**: Ortalamaya dönüş süresi
6. **Correlation Check**: Sürekli korelasyon takibi

## Örnek İyileştirilmiş Kod

```matlab
% Half-life calculation (ortalamaya dönüş süresi)
beta = polyfit(ratio(1:end-1), ratio(2:end) - ratio(1:end-1), 1);
half_life = -log(2) / beta(1);

% Stop-loss
max_loss = 0.05;  % %5 stop-loss
if loss > max_loss
    disp('Stop loss triggered!');
    exit_position();
end
```

## Teknik Detaylar

### MATLAB Script:
- **Varlıklar**: ETH, XRP
- **Veri**: 2023 yılı günlük
- **Grafikler**: 3 subplot + 1 sinyal grafiği
- **Sinyal**: Entry (kırmızı), Exit (mavi üçgen)

### PHP Bot:
- **API**: Binance REST API
- **Timeframe**: 1 günlük (1d)
- **Lookback**: 365 gün
- **Update**: 5 saniye
- **Output**: Konsol (echo)

## Performans Metrikleri (Manuel Hesaplama Gerekir)

Script'e eklenebilir:
- Win Rate
- Average Profit per Trade
- Sharpe Ratio
- Maximum Drawdown
- Number of Trades
- Average Holding Period

Bu ders, öğrencilere profesyonel düzeyde statistical arbitrage ve pair trading stratejileri geliştirme becerisi kazandırmayı amaçlamaktadır.
