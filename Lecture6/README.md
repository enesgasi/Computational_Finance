# Lecture 6 - Binance API ile Kripto Para İşlemleri

## İçerik
Bu ders, Binance kripto para borsası API'si ile programatik etkileşim konusunu işlemektedir.

## Dosyalar
- `bin_class.php` - Binance API için PHP wrapper sınıfı (1707 satır)

## Script Detayları

### bin_class.php
Bu dosya, Binance kripto para borsası ile etkileşim için kapsamlı bir PHP sınıfı içerir.

#### Ana Özellikler:
1. **API Bağlantı Yapılandırması**
   - REST API endpoint'leri (api.binance.com)
   - WebSocket stream bağlantıları
   - API key ve secret yönetimi
   - Proxy desteği

2. **Temel İşlem Fonksiyonları**
   - `buy()` - Alış emri oluşturma
   - `sell()` - Satış emri oluşturma
   - `buyTest()` - Test alış emri (gerçek işlem yapmaz)
   - `sellTest()` - Test satış emri (gerçek işlem yapmaz)
   - `marketBuy()` - Piyasa fiyatından alış

3. **Sipariş Tipleri**
   - LIMIT - Limit emir
   - MARKET - Piyasa emri
   - STOP_LOSS - Zarar durdur
   - STOP_LOSS_LIMIT - Limitli zarar durdur
   - TAKE_PROFIT - Kâr al
   - TAKE_PROFIT_LIMIT - Limitli kâr al
   - LIMIT_MAKER - Maker limit emir

4. **Veri Yönetimi**
   - Depth cache (Derinlik önbelleği)
   - Chart data (Grafik verileri)
   - Bakiye takibi
   - BTC değer hesaplaması

5. **Yapılandırma**
   - Kullanıcı home dizininden config dosyası okuma
   - Proxy yapılandırması
   - Sunucu zamanı senkronizasyonu

#### Kullanım Örneği:
```php
$api = new Binance\binali($api_key, $api_secret);

// Limit alış emri
$quantity = 1;
$price = 0.0005;
$order = $api->buy("BNBBTC", $quantity, $price);

// Satış emri
$order = $api->sell("BNBBTC", $quantity, $price);
```

## Öğrenilen Konular
- Kripto para borsası API entegrasyonu
- REST API ve WebSocket kullanımı
- Emir tipleri ve alım-satım stratejileri
- Güvenli API key yönetimi
- Gerçek zamanlı veri akışı (streaming)
- Finansal işlem güvenliği

## Teknik Detaylar
- **Dil**: PHP
- **API**: Binance REST API & WebSocket
- **Kütüphane**: php-binance-api wrapper
- **Protokol**: HTTPS, WSS (WebSocket Secure)
- **Satır Sayısı**: 1707 satır

Bu ders, öğrencilere programatik olarak kripto para borsalarında işlem yapma, veri çekme ve gerçek zamanlı piyasa verilerini izleme becerisi kazandırmayı amaçlamaktadır.
