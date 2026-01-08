# Lecture 13 - Momentum Trading: Fiyat Değişim Yüzdesi Stratejisi

## İçerik
Bu ders, momentum trading stratejisini öğretir. Binance borsasındaki tüm trading çiftlerinin 24 saatlik fiyat değişim yüzdelerini analiz ederek güçlü momentum gösteren varlıkları tespit etme yöntemi gösterilir.

## Dosyalar
- `mean_reversion_lecture_13.php` - Momentum tarama scripti (PHP, 32 satır)
- `trading-13.py` - Otomatik email alert sistemi (Python, 43 satır)
- `bin_class.php` - Binance API wrapper
- `init` - Başlatma dosyası (boş)

## Script Detayları

### mean_reversion_lecture_13.php - Momentum Scanner

**Not:** Dosya adı "mean_reversion" olsa da, aslında momentum stratejisi uygulanıyor.

#### 1. API Bağlantısı ve Başlangıç
```php
require("bin_class.php");
$key = '';
$secret = '';
$bnb = new Binance\binali($key, $secret, ['useServerTime'=>True]);
$bnb->useServerTime();
```
- Binance API'ye bağlanır
- Sunucu zamanı senkronizasyonu

#### 2. Anlık Fiyat Bilgisi (Bid-Ask Spread)
```php
$ticker = $bnb->bookprices();
$buyprice = $ticker['ETHUSDT']['bidPrice'];   // Alış fiyatı
$sellprice = $ticker['ETHUSDT']['askPrice'];  // Satış fiyatı

echo "Buy Price: $buyprice\n";
echo "Sell Price: $sellprice\n";

$eth_ticker = $ticker['ETHUSDT'];
print_r($eth_ticker);
```

**Bid-Ask Spread:**
- **Bid Price**: Piyasanın senden alacağı fiyat (sen satıyorsun)
- **Ask Price**: Piyasanın sana satacağı fiyat (sen alıyorsun)
- **Spread**: Ask - Bid (işlem maliyeti göstergesi)

#### 3. 24 Saatlik İstatistikler
```php
$day_info = $bnb->prevDay();
print_r($day_info[5]);

$percent = $day_info[5]['priceChangePercent'];
echo "24h Change Percent: $percent%\n";
```
- `prevDay()`: Son 24 saatin istatistikleri
- Fiyat değişim yüzdesi
- Volume, high, low, vs.

#### 4. Momentum Tarama - Tüm Çiftler
```php
for ($i=0; $i<count($day_info); $i++) {
    $percent = $day_info[$i]['priceChangePercent'];
    
    if ($percent > 20) {  // %20'den fazla yükselenler
        $symbol = $day_info[$i]['symbol'];
        echo ("<br>symbol=$symbol --percent== $percent%\n");
    }
}
```

**Strateji Mantığı:**
- Binance'teki **TÜM trading çiftlerini** tara
- Son 24 saatte **%20'den fazla yükselenleri** bul
- Bu varlıklar güçlü momentum gösteriyor
- **Momentum trading**: Yükseliş devam edebilir hipotezi

---

## trading-13.py - Otomatik Email Alert Sistemi

Bu Python scripti, Binance API'den alfa token verilerini çekerek güçlü momentum gösterenleri tespit eder ve email ile bildirim gönderir.

### 1. API Bağlantısı ve Konfigürasyon
```python
import requests
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
import mail_configuration

api_url = "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/cex/alpha/all/token/list"

sender = mail_configuration.sender
receiver = mail_configuration.receiver
password = mail_configuration.password
```

**Kullanılan Modüller:**
- `requests`: HTTP API çağrıları
- `smtplib`: Email gönderimi (SMTP protokolü)
- `ssl`: Güvenli bağlantı
- `MIMEText`: Email mesaj formatı
- `mail_configuration`: Email ayarları modülü

**Email Konfigürasyonu:**
- Yandex SMTP sunucusu kullanılıyor
- `mail_configuration` modülünden bilgiler çekiliyor
- Güvenlik için password ayrı dosyada

### 2. API'den Veri Çekme
```python
try:
    response = requests.get(api_url, timeout=10)
    info1 = response.json()
except Exception as e:
    print(f"Error: {e}")
```

**Hata Yönetimi:**
- `try-except` bloğu ile güvenli API çağrısı
- 10 saniye timeout süresi
- Hata durumunda script çökmez, hata mesajı yazdırır

**API Response Yapısı:**
```json
{
    "data": [
        {
            "symbol": "BTCUSDT",
            "percentChange24h": "5.23",
            "priceHigh24h": "45000.50",
            "priceLow24h": "43200.00",
            ...
        },
        ...
    ]
}
```

### 3. Token Analizi Döngüsü
```python
for i in range(min(5, len(info1['data']))):
    symbol = info1["data"][i]['symbol']
    percent = float(info1['data'][i]['percentChange24h'])
    high = float(info1['data'][i]['priceHigh24h'])
    low = float(info1['data'][i]['priceLow24h'])
    
    print(f"Symbol: {symbol}, Percent: {percent}%")
```

**Güvenli Döngü:**
- `min(5, len(info1['data']))` ile maksimum 5 token kontrol edilir
- Eğer 5'ten az token varsa hata vermez
- f-string ile modern Python formatlaması

**Çekilen Metrikler:**
- **symbol**: Token sembolü (örn: BTCUSDT)
- **percentChange24h**: 24 saatlik değişim yüzdesi
- **priceHigh24h**: Günün en yüksek fiyatı
- **priceLow24h**: Günün en düşük fiyatı

### 4. Alert Koşulu ve Email Gönderimi
```python
if percent > 80:  # %80'den fazla yükseliş
    # Email mesajı oluştur
    message = f"ALERT: {symbol} +{percent}%\nHigh: {high}\nLow: {low}"
    msg = MIMEText(message)
    msg['Subject'] = f"Trading Alert: {symbol}"
    msg['From'] = sender
    msg['To'] = ', '.join(receiver) if isinstance(receiver, list) else receiver
    
    # SSL ile güvenli bağlantı
    context = ssl.create_default_context()
    
    # Email gönder
    with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        print("✅ Email sent")
```

**Alert Mantığı:**
- Token %80'den fazla yükselmiş ise alarm
- f-string ile dinamik mesaj oluşturma
- Email başlığına token adı eklenir
- Liste veya tekil receiver desteği
- Başarılı gönderim sonrası onay mesajı
- Yandex SMTP (Port 465, SSL)

**Email Mesaj Formatı:**
```
ALERT: BTCUSDT +85.5%
High: 45000.50
Low: 43200.00
```

### Script Özellikleri

#### Script Özellikleri:
- ✅ Otomatik monitoring sistemi
- ✅ Anlık email bildirimi
- ✅ 7/24 çalışabilir
- ✅ Özelleştirilebilir threshold (%80)
- ✅ Hata yönetimi ile güvenli çalışma
- ✅ Timeout koruması (10 saniye)
- ✅ Liste veya tekil email desteği
- ✅ API'den 5 token kontrolü

#### Dikkat Edilmesi Gerekenler:

**1. API Timeout:**
```python
response = requests.get(api_url, timeout=10)
```
- 10 saniye içinde yanıt gelmezse timeout
- Network sorunlarında script kilitlenmez

**2. Güvenli Döngü:**
```python
for i in range(min(5, len(info1['data']))):
```
- API 5'ten az token döndürse bile hata vermez
- Index out of range hatası önlenir

**3. Dinamik Receiver:**
```python
msg['To'] = ', '.join(receiver) if isinstance(receiver, list) else receiver
```
- Receiver liste ise virgülle ayırır
- Tekil string ise direkt kullanır

**4. Hata Yakalama:**
```python
try:
    # Tüm işlemler
except Exception as e:
    print(f"Error: {e}")
```
- Herhangi bir hata durumunda script çökmez
- Hata mesajı ekrana yazdırılır

### mail_configuration.py - Email Yapılandırma Modülü

Bu modül, `trading-13.py` scripti için gerekli email ayarlarını içerir. Güvenlik açısından hassas bilgiler ayrı dosyada tutulur.

#### Dosya Yapısı:
```python
"""
Email Configuration Module
--------------------------
Bu dosya trading-13.py scripti için email ayarlarını içerir.
"""

# Email gönderen adresi (Yandex Mail)
sender = "your_email@yandex.com"

# Email alıcı adresleri (liste formatında)
receiver = ["recipient@example.com"]

# Yandex Mail uygulama şifresi
password = "your_app_password_here"

# SMTP Sunucu Ayarları
smtp_server = "smtp.yandex.com"
smtp_port = 465
```

#### Kurulum Adımları:

**1. Yandex Mail Hesabı Oluşturma**
- [mail.yandex.com](https://mail.yandex.com) adresinden ücretsiz hesap açın
- Hesabınızı doğrulayın

**2. Uygulama Şifresi Oluşturma**
- Yandex Mail'e giriş yapın
- Sağ üst köşe → **Ayarlar (Settings)**
- **Güvenlik (Security)** sekmesi
- **Uygulama şifreleri (App passwords)** bölümü
- "Mail" için yeni şifre oluşturun
- Oluşturulan şifreyi kopyalayın (bir daha gösterilmez!)

**3. Dosyayı Düzenleme**
```python
# Örnek gerçek kullanım:
sender = "trading_bot_2026@yandex.com"
receiver = ["mytrading@gmail.com", "alerts@yahoo.com"]
password = "abcdEFGH1234ijkl"  # Uygulama şifresi
```

#### Güvenlik Notları:

**❌ YAPILMAMASI GEREKENLER:**
```python
# Normal şifrenizi kullanmayın
password = "myYandexPassword123"  # YANLIŞ!

# Şifreyi kodun içine yazmayın
# trading-13.py içinde:
password = "hardcoded_password"  # YANLIŞ!

# Public repository'e yüklemeyin
git add mail_configuration.py  # TEHLİKELİ!
```

**✅ YAPILMASI GEREKENLER:**
```python
# Uygulama şifresi kullanın
password = "app_specific_password"  # DOĞRU

# .gitignore'a ekleyin
echo "mail_configuration.py" >> .gitignore

# Environment variable kullanın (alternatif)
import os
password = os.getenv('EMAIL_PASSWORD')
```

#### Alternatif: Environment Variables

Daha güvenli bir yaklaşım için environment variable kullanabilirsiniz:

**1. .env dosyası oluşturun:**
```bash
# .env
EMAIL_SENDER=trading_bot@yandex.com
EMAIL_RECEIVER=trader@gmail.com
EMAIL_PASSWORD=your_app_password
```

**2. Python-dotenv kullanın:**
```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()

sender = os.getenv('EMAIL_SENDER')
receiver = [os.getenv('EMAIL_RECEIVER')]
password = os.getenv('EMAIL_PASSWORD')
```

**3. .gitignore'a ekleyin:**
```bash
.env
mail_configuration.py
__pycache__/
```

#### Test Etme

Email ayarlarınızı test etmek için basit bir script:

```python
import smtplib
import ssl
from email.mime.text import MIMEText
import mail_configuration

def test_email_config():
    try:
        # Email oluştur
        msg = MIMEText("Bu bir test mesajıdır.")
        msg['Subject'] = "Email Config Test"
        msg['From'] = mail_configuration.sender
        msg['To'] = ', '.join(mail_configuration.receiver)
        
        # Gönder
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
            server.login(mail_configuration.sender, mail_configuration.password)
            server.sendmail(
                mail_configuration.sender,
                mail_configuration.receiver,
                msg.as_string()
            )
        
        print("✅ Email başarıyla gönderildi!")
        print(f"Gönderen: {mail_configuration.sender}")
        print(f"Alıcı: {mail_configuration.receiver}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Kimlik doğrulama hatası! Kullanıcı adı veya şifre yanlış.")
        print("💡 Uygulama şifresi kullandığınızdan emin olun.")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Hatası: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Genel Hata: {e}")
        return False

if __name__ == "__main__":
    test_email_config()
```

#### Çoklu Alıcı Yönetimi

```python
# Tek alıcı
receiver = ["trader@gmail.com"]

# Birden fazla alıcı
receiver = [
    "trader1@gmail.com",
    "trader2@yahoo.com",
    "alerts@hotmail.com"
]

# Alıcı grupları
receivers_urgent = ["ceo@company.com", "cto@company.com"]
receivers_info = ["team@company.com"]

# Script içinde kullanım:
if percent > 100:  # Kritik alarm
    receiver = receivers_urgent
elif percent > 50:  # Bilgilendirme
    receiver = receivers_info
```

#### Hata Ayıklama

**Sorun: "Authentication failed"**
```python
# Çözüm 1: Uygulama şifresi kullandığınızı kontrol edin
# Çözüm 2: 2FA (iki faktörlü doğrulama) aktif olmalı
# Çözüm 3: "Daha az güvenli uygulamalar" ayarını kontrol edin
```

**Sorun: "Connection timeout"**
```python
# Port numarasını kontrol edin: 465 (SSL) veya 587 (TLS)
smtp_server = "smtp.yandex.com"
smtp_port = 465  # SSL için

# Alternatif:
smtp_port = 587  # TLS için (STARTTLS)
```

**Sorun: "Recipient address rejected"**
```python
# Email formatını kontrol edin
receiver = ["valid_email@example.com"]  # DOĞRU
receiver = ["invalid-email"]  # YANLIŞ
```

#### Alternatif Email Sağlayıcıları

**Gmail:**
```python
smtp_server = "smtp.gmail.com"
smtp_port = 587
# NOT: Google "Daha az güvenli uygulamalar" desteğini kaldırdı
# OAuth2 veya Uygulama Şifresi gerekir
```

**Outlook/Hotmail:**
```python
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
```

**Yahoo:**
```python
smtp_server = "smtp.mail.yahoo.com"
smtp_port = 465
```

#### Best Practices

1. **Şifre Güvenliği**: Asla gerçek şifrenizi kullanmayın
2. **Version Control**: mail_configuration.py'yi git'e eklemeyin
3. **Backup**: Uygulama şifrenizi güvenli bir yerde saklayın
4. **Rate Limiting**: Çok fazla email göndermeyin (spam sayılabilir)
5. **Error Handling**: Her zaman try-except bloğu kullanın
6. **Logging**: Gönderilen emailleri kaydedin

#### İleri Seviye: Email Templates

```python
# mail_configuration.py içinde
email_template = """
🚨 TRADING ALERT 🚨

Token: {symbol}
24h Change: {percent}%
High: ${high}
Low: ${low}

Timestamp: {timestamp}

---
Bu otomatik bir mesajdır.
"""

# Kullanım:
from datetime import datetime

message = email_template.format(
    symbol="BTCUSDT",
    percent=85.5,
    high=45000,
    low=43000,
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)
```

---

## Momentum Trading Stratejisi

### Temel Prensipler

1. **Trend Following (Trend Takibi)**
   - "The trend is your friend"
   - Güçlü hareket eden varlıklara yatırım
   - Momentum devam edebilir

2. **Relative Strength**
   - En güçlü performans gösterenleri bul
   - Zayıf performans gösterenlerden kaçın
   - Karşılaştırmalı analiz

3. **Breakout Strategy**
   - Fiyat güçlü hareket edince pozisyon aç
   - Momentum zayıfladığında çık
   - Volume konfirmasyonu önemli

### Trading Sinyalleri

#### Entry (Giriş) Koşulları:
- ✅ 24h değişim > %20 (güçlü momentum)
- ✅ Yüksek volume (likidite)
- ✅ Trend devam ediyor
- ✅ Support seviyelerinden yukarıda

#### Exit (Çıkış) Koşulları:
- ❌ Momentum zayıfladı (< %5)
- ❌ Ters yönde hareket başladı
- ❌ Stop-loss tetiklendi
- ❌ Kar hedefine ulaşıldı

## API Fonksiyonları

### bookprices()
```php
$ticker = $bnb->bookprices();
```
**Döndürür:**
```php
[
    'ETHUSDT' => [
        'symbol' => 'ETHUSDT',
        'bidPrice' => '2450.50',   // Alış
        'bidQty' => '10.5',
        'askPrice' => '2451.20',   // Satış
        'askQty' => '8.2'
    ],
    ...
]
```

### prevDay()
```php
$day_info = $bnb->prevDay();
```
**Döndürür:**
```php
[
    [
        'symbol' => 'ETHUSDT',
        'priceChange' => '120.50',
        'priceChangePercent' => '5.15',
        'weightedAvgPrice' => '2400.25',
        'prevClosePrice' => '2330.00',
        'lastPrice' => '2450.50',
        'lastQty' => '0.5',
        'bidPrice' => '2450.00',
        'askPrice' => '2451.00',
        'openPrice' => '2330.00',
        'highPrice' => '2480.00',
        'lowPrice' => '2320.00',
        'volume' => '150000',
        'quoteVolume' => '360037500.00',
        'openTime' => 1704067200000,
        'closeTime' => 1704153600000,
        'firstId' => 123456789,
        'lastId' => 123567890,
        'count' => 111101
    ],
    ...
]
```

## Kullanım Senaryoları

### 1. Market Screener (Piyasa Tarayıcı)
```php
// En çok yükselenleri bul
foreach ($day_info as $coin) {
    if ($coin['priceChangePercent'] > 20) {
        // Trade signal
    }
}
```

### 2. Momentum Ranking
```php
// Tüm coinleri performansa göre sırala
usort($day_info, function($a, $b) {
    return $b['priceChangePercent'] - $a['priceChangePercent'];
});

// Top 10'u göster
for ($i=0; $i<10; $i++) {
    echo $day_info[$i]['symbol'] . ": " . 
         $day_info[$i]['priceChangePercent'] . "%\n";
}
```

### 3. Volatilite Analizi
```php
// Volatilite = (High - Low) / Open
foreach ($day_info as $coin) {
    $volatility = ($coin['highPrice'] - $coin['lowPrice']) / $coin['openPrice'];
    if ($volatility > 0.15) {  // %15+ volatilite
        echo "High volatility: " . $coin['symbol'] . "\n";
    }
}
```

## Öğrenilen Konular

1. **Momentum Trading**: Güçlü hareket eden varlıklara yatırım
2. **Market Scanning**: Piyasa tarama teknikleri
3. **Bid-Ask Spread**: Alış-satış farkı analizi
4. **24h Statistics**: Günlük performans metrikleri
5. **Relative Strength**: Göreceli güç analizi
6. **Trend Following**: Trend takip stratejisi
7. **Volume Analysis**: İşlem hacmi önemi
8. **Breakout Detection**: Kırılım tespiti

## Momentum vs Mean Reversion Karşılaştırması

| Özellik | Momentum | Mean Reversion |
|---------|----------|----------------|
| **Felsefe** | Trend devam eder | Fiyat ortalamaya döner |
| **Entry** | Güçlü hareket | Aşırı sapma |
| **Risk** | Trend dönüşü | Divergence |
| **Piyasa** | Trending markets | Range-bound markets |
| **Hold Period** | Orta-uzun | Kısa |
| **Win Rate** | Düşük (%40-50) | Yüksek (%60-70) |
| **Risk/Reward** | Yüksek | Düşük |

## Risk Yönetimi

### Momentum Trading Riskleri:
1. **Reversal Risk**: Ani trend dönüşü
2. **False Breakout**: Sahte kırılım
3. **Whipsaw**: Keskin dalgalanmalar
4. **FOMO Trading**: Korku ile geç giriş
5. **Bubble Risk**: Balon riski

### Risk Azaltma Teknikleri:
- **Stop Loss**: %5-10 aşağıda
- **Position Sizing**: Sermayenin %2-5'i
- **Diversification**: 5-10 farklı coin
- **Profit Taking**: Kademeli kar realizasyonu
- **Volume Confirmation**: Hacim doğrulaması

## İyileştirme Önerileri

### 1. Volume Filtresi
```php
if ($percent > 20 && $coin['volume'] > $min_volume) {
    // Trade signal
}
```

### 2. Multi-Timeframe Analysis
```php
// 1h, 4h, 1d momentum karşılaştır
$momentum_1h = calculate_momentum($bnb->candlesticks($symbol, '1h', 24));
$momentum_1d = calculate_momentum($bnb->candlesticks($symbol, '1d', 30));
```

### 3. Technical Indicators
```php
// RSI, MACD, Bollinger Bands ekle
if ($percent > 20 && $rsi > 70) {
    echo "Overbought - Caution!\n";
}
```

### 4. Risk Management
```php
// Position size calculation
$account_size = 10000;  // $10k
$risk_per_trade = 0.02;  // %2
$stop_loss = 0.05;  // %5

$position_size = ($account_size * $risk_per_trade) / $stop_loss;
```

## Örnek Genişletilmiş Strateji

```php
// Gelişmiş momentum tarama
foreach ($day_info as $coin) {
    $percent = $coin['priceChangePercent'];
    $volume = $coin['volume'];
    $high = $coin['highPrice'];
    $low = $coin['lowPrice'];
    $close = $coin['lastPrice'];
    
    // Volatilite
    $volatility = ($high - $low) / $low;
    
    // Volume spike detection
    $avg_volume = get_avg_volume($coin['symbol'], 30);
    $volume_ratio = $volume / $avg_volume;
    
    // Güçlü momentum + yüksek volume + uygun volatilite
    if ($percent > 15 && 
        $volume_ratio > 2 && 
        $volatility > 0.10 && 
        $volatility < 0.30) {
        
        echo "BUY SIGNAL: " . $coin['symbol'] . "\n";
        echo "  Price Change: $percent%\n";
        echo "  Volume Ratio: $volume_ratio x\n";
        echo "  Volatility: " . ($volatility*100) . "%\n";
        
        // Buraya emir gönderme kodu eklenebilir
        // $bnb->buy($coin['symbol'], $quantity, $price);
    }
}
```

## Performans Metrikleri

Manuel hesaplama gerekir:
- **Hit Rate**: Kazanan işlem oranı
- **Average Gain**: Ortalama kazanç
- **Average Loss**: Ortalama kayıp
- **Profit Factor**: Toplam kazanç / Toplam kayıp
- **Sharpe Ratio**: Risk-adjusted return
- **Max Drawdown**: Maksimum düşüş

## Piyasa Koşulları

### Momentum İyi Çalışır:
- ✅ Bull market (yükseliş trendi)
- ✅ Yüksek volatilite
- ✅ Güçlü trend var
- ✅ Yüksek likidite

### Momentum Kötü Çalışır:
- ❌ Bear market (düşüş trendi)
- ❌ Sideways market (yatay)
- ❌ Düşük volatilite
- ❌ Choppy market (dalgalı)

## Gerçek Dünya Örnekleri

### Başarılı Momentum Trades:
- Bitcoin 2020-2021 bull run
- Altcoin season momentum
- DeFi summer 2020
- NFT boom 2021

### Başarısız Momentum Trades:
- LUNA collapse 2022
- FTX token crash 2022
- Leverage cascade liquidations

## Teknik Detaylar

### PHP Script:
- **API**: Binance REST API
- **Endpoint**: `prevDay()`, `bookprices()`
- **Timeframe**: 24 saat
- **Threshold**: %20 fiyat değişimi
- **Output**: Konsol (echo)

### Veri Yapısı:
- Array of objects (JSON benzeri)
- Symbol, price, volume, change%
- Tüm Binance trading pairs

## Sonraki Adımlar

1. **Python Implementation**: Python ile aynı strateji
2. **Automated Trading**: Otomatik emir gönderme
3. **Backtesting**: Tarihsel performans testi
4. **Machine Learning**: ML ile momentum tahmini
5. **Multi-Exchange**: Birden fazla borsa desteği

Bu ders, öğrencilere momentum tabanlı trading stratejileri ve piyasa tarama teknikleri konusunda pratik beceriler kazandırmayı amaçlamaktadır.
