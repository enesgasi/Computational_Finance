# Lecture 9 - Zaman Serisi Analizi: ARMA, ARIMA ve SARIMA Modelleri

## İçerik
Bu ders, hisse senedi fiyat tahmininde kullanılan klasik zaman serisi modelleri olan ARMA, ARIMA ve SARIMA modellerini öğretir.

## Dosyalar
- `lecture9.py` - IBM hisse senedi üzerinde ARMA ve SARIMAX analizi (58 satır)
- `amazon.py` - Amazon hisse senedi üzerinde ARMA, ARIMA ve SARIMA karşılaştırması (75 satır)
- `IBM.csv` - IBM hisse senedi tarihsel fiyat verileri

## Script Detayları

### lecture9.py - IBM Hisse Senedi Analizi

#### 1. Veri Yükleme ve Hazırlama
```python
quotes = pd.read_csv('IBM.csv')
data = quotes[['Date', 'Close']]
data.index = pd.to_datetime(data['Date'], format='mixed')
```
- IBM hisse senedi kapanış fiyatları yüklenir
- Tarih index olarak ayarlanır

#### 2. Veri Görselleştirme
```python
plt.plot(data.index, data['Close'])
plt.xlabel('Date')
plt.ylabel('Price')
```
- Fiyat zaman serisi grafiği çizilir
- Seaborn stil uygulanır

#### 3. Train/Test Split
```python
train = data[data.index < pd.to_datetime('2023-04-10')]
test = data[data.index > pd.to_datetime('2023-04-10')]
```
- 2023-04-10 tarihine kadar eğitim
- Sonrası test verisi

#### 4. ARMA Modeli (AutoRegressive Moving Average)
```python
ArmaModel = SARIMAX(X, order=(1,0,1))
ArmaModel = ArmaModel.fit()
```
- **ARMA(1,0,1)**: AR(1) + MA(1) modeli
- **order=(p,d,q)**:
  - p=1: Autoregressive terimi (geçmiş değerlere bağımlılık)
  - d=0: Differencing yok (seri durağan)
  - q=1: Moving Average terimi (geçmiş hatalara bağımlılık)

#### 5. Tahmin ve Güven Aralığı
```python
y_pred = ArmaModel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha=0.05)
y_pred_df['Predictions'] = ArmaModel.predict(...)
```
- Test dönemi için tahmin yapılır
- %95 güven aralığı hesaplanır (alpha=0.05)

#### 6. Model Değerlendirmesi
```python
arma_rmse = np.sqrt(mean_squared_error(test['Close'], y_pred_df['Predictions']))
```
- **RMSE (Root Mean Squared Error)**: Tahmin hatası ölçütü
- Düşük RMSE daha iyi model performansı gösterir

#### 7. SARIMAX Modeli (Bonus)
```python
SarimaxModel = SARIMAX(X, order=(5,3,2), seasonal_order=(2,2,3,6))
```
- **SARIMA**: Mevsimsel ARIMA
- **order=(5,3,2)**: AR(5), I(3), MA(2)
- **seasonal_order=(2,2,3,6)**: Mevsimsel AR(2), I(2), MA(3), Periyot=6

---

### amazon.py - Amazon Hisse Senedi Karşılaştırmalı Analiz

#### 1. Veri Çekme (yfinance ile)
```python
ticker = 'AMZN'
amazon = yf.Ticker(ticker)
history = amazon.history(period='500d')
data = history['Close']
```
- yfinance kütüphanesi ile otomatik veri indirme
- Son 500 günlük veri
- Günlük frekans ayarlanır ve eksik değerler doldurulur

#### 2. Train/Test Split
```python
train = data[:-30]  # Son 30 gün hariç
test = data[-30:]   # Son 30 gün
```

#### 3. ARMA Modeli (AutoReg ile)
```python
arma_model = AutoReg(train, lags=5).fit()
arma_forecast = arma_model.predict(start=len(train), end=len(train)+len(test)-1)
```
- **AutoReg(lags=5)**: Son 5 günün verisiyle tahmin
- ARMA benzeri model

#### 4. ARIMA Modeli
```python
arima_model = ARIMA(train, order=(5,1,2)).fit()
```
- **ARIMA(5,1,2)**:
  - **AR(5)**: Son 5 gözleme bağımlılık
  - **I(1)**: 1. derece differencing (trend giderme)
  - **MA(2)**: Son 2 hataya bağımlılık
- Trend içeren seriler için uygun

#### 5. SARIMA Modeli
```python
sarima_model = SARIMAX(train, order=(5,1,2), seasonal_order=(1,1,1,7)).fit()
```
- **seasonal_order=(1,1,1,7)**:
  - Mevsimsel AR(1)
  - Mevsimsel I(1)
  - Mevsimsel MA(1)
  - **Periyot=7**: Haftalık mevsimsellik

#### 6. Tüm Modellerin Karşılaştırmalı Görselleştirmesi
```python
plt.plot(data.index, data, label="Actual Price")
plt.plot(test.index, arma_forecast, label="ARMA Forecast")
plt.plot(test.index, arima_forecast, label="ARIMA Forecast")
plt.plot(test.index, sarima_forecast, label="SARIMA Forecast")
```
- Gerçek fiyat vs 3 model tahmini
- Hangi modelin daha iyi performans gösterdiği görsel olarak değerlendirilir

#### 7. Gelecek Tahminleri (30 Gün İleride)
```python
future_arima = arima_model.predict(len(data), len(data)+future_days-1)
future_sarima = sarima_model.predict(len(data), len(data)+future_days-1)
```
- Test döneminden sonra 30 gün daha ileriye tahmin
- Gerçek forecasting senaryosu

## Kullanılan Kütüphaneler
- **pandas**: Veri manipülasyonu
- **numpy**: Sayısal hesaplamalar
- **matplotlib**: Görselleştirme
- **seaborn**: İleri seviye görselleştirme
- **statsmodels**:
  - `SARIMAX`: ARMA/ARIMA/SARIMA modelleri
  - `ARIMA`: ARIMA modeli
  - `AutoReg`: Autoregression modeli
- **yfinance**: Yahoo Finance'den hisse senedi verisi çekme
- **sklearn.metrics**: Model değerlendirme metrikleri

## Zaman Serisi Modelleri Karşılaştırması

| Model | Açıklama | Kullanım Durumu | Parametreler |
|-------|----------|----------------|--------------|
| **ARMA** | Autoregressive + Moving Average | Durağan seriler | (p, 0, q) |
| **ARIMA** | ARMA + Differencing | Trend içeren seriler | (p, d, q) |
| **SARIMA** | ARIMA + Mevsimsellik | Mevsimsel patern içeren seriler | (p,d,q)(P,D,Q,s) |

### Parametre Açıklamaları:
- **p**: Autoregressive (AR) terimi sayısı
- **d**: Differencing derecesi
- **q**: Moving Average (MA) terimi sayısı
- **P,D,Q**: Mevsimsel AR, I, MA
- **s**: Mevsimsel periyot (örn: 7=haftalık, 12=aylık)

## Öğrenilen Konular
1. **Zaman Serisi Analizi**: Finansal verilerin zamansal yapısı
2. **Durağanlık (Stationarity)**: Serinin istatistiksel özelliklerinin zamana göre değişmemesi
3. **Differencing**: Trend giderme tekniği
4. **Otokorelasyon**: Zaman serisinin kendisi ile gecikmeli korelasyonu
5. **Model Seçimi**: ARMA vs ARIMA vs SARIMA
6. **Forecast vs Prediction**: İleriye yönelik tahmin
7. **Güven Aralıkları**: Tahmin belirsizliği
8. **Model Değerlendirme**: RMSE metriği

## Dikkat Edilmesi Gerekenler
1. **Durağanlık Testi**: ARIMA öncesi ADF testi yapılmalı
2. **Parametre Seçimi**: ACF/PACF grafikleri ile optimal p,q seçimi
3. **Mevsimsellik Tespiti**: Seasonal decomposition yapılmalı
4. **Overfitting**: Çok fazla parametre kullanmak modeli kötüleştirebilir
5. **Finansal Veriler**: Genelde durağan değildir, differencing gerekir

## Pratik Uygulamalar
- Hisse senedi fiyat tahmini
- Volatilite tahmini
- Risk yönetimi
- Portföy optimizasyonu
- Algoritmik trading stratejileri

## Teknik Detaylar
- **Dil**: Python 3
- **Veri Kaynağı**: CSV dosyaları ve Yahoo Finance API
- **Modeller**: ARMA(1,0,1), ARIMA(5,1,2), SARIMA(5,1,2)(1,1,1,7)
- **Metrik**: RMSE
- **Test Periyodu**: 30 gün
