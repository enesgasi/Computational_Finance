# Lecture 8 - Regresyon ile Hisse Senedi Fiyat Tahmini ve Alım-Satım Stratejisi

## İçerik
Bu ders, makine öğrenmesi regresyon teknikleri kullanılarak hisse senedi fiyat tahmini ve algoritmik ticaret stratejisi geliştirmeyi öğretir.

## Dosyalar
- `lecture8.py` - Google hisse senedi analiz scripti (109 satır)
- `GOOG.csv` - Google (Alphabet) hisse senedi tarihsel fiyat verileri

## Script Detayları

### lecture8.py
Bu script, Google hisse senedi verileri üzerinde regresyon analizi yaparak gelecek fiyat hareketlerini tahmin eder ve bir ticaret stratejisi oluşturur.

#### 1. Veri Hazırlama ve Özellik Mühendisliği
```python
df['Open-Close'] = df['Open'] - df['Close']
df['High-Low'] = df['High'] - df['Low']
df['Target'] = df['Close'].shift(-1) - df['Close']
```
- **Open-Close**: Günlük açılış ve kapanış fiyatı farkı
- **High-Low**: Günlük en yüksek ve en düşük fiyat aralığı
- **Target**: Tahmin edilecek değişken (yarının kapanış fiyatı - bugünün kapanış fiyatı)

#### 2. Veri Görselleştirme
```python
pd.plotting.scatter_matrix(
    df_feat[['Open-Close', 'High-Low', 'Target']],
    grid=True,
    diagonal='kde'
)
```
Özellikler arası ilişkileri ve dağılımları gösterir (scatter matrix).

#### 3. Model Eğitimi - Ordinary Least Squares (OLS)
```python
ols = linear_model.LinearRegression()
ols.fit(X_train, Y_train)
```
- %80 veri eğitim, %20 test için ayrılır
- Lineer regresyon modeli eğitilir
- Katsayılar ve intercept hesaplanır

#### 4. Model Değerlendirmesi
```python
train_mse = mean_squared_error(Y_train, train_predict)
train_r2 = r2_score(Y_train, train_predict)
test_mse = mean_squared_error(Y_test, test_predict)
test_r2 = r2_score(Y_test, test_predict)
```
- **MSE (Mean Squared Error)**: Ortalama kare hata
- **R² Score**: Modelin açıklama gücü (1'e yakın daha iyi)

#### 5. Alım-Satım Stratejisi
```python
df_feat['Predicted_Signal'] = np.where(df_feat['Predicted_Return'] > 0, 1, -1)
df_feat['Strategy_Returns'] = df_feat['GOOG_Returns'] * df_feat['Predicted_Signal'].shift(1)
```
- **Sinyal Üretimi**: 
  - Tahmin pozitif ise → LONG (1) - Hisse al
  - Tahmin negatif ise → SHORT (-1) - Hisse sat
- **Strateji Getirisi**: Dünkü sinyale göre bugünün getirisini al
- Log getiri hesaplaması kullanılır

#### 6. Performans Karşılaştırması
```python
cum_goog_return = df_feat.iloc[split_value:]['GOOG_Returns'].cumsum() * 100
cum_strategy_return = df_feat.iloc[split_value:]['Strategy_Returns'].cumsum() * 100
```
- Test dönemi için kümülatif getiriler hesaplanır
- **Buy & Hold** stratejisi ile **ML tabanlı strateji** karşılaştırılır
- Grafik çizilerek görsel karşılaştırma yapılır

#### 7. Lasso Regresyon (Bonus)
```python
lasso = linear_model.Lasso(alpha=0.001)
lasso.fit(X_train, Y_train)
```
- Özellik seçimi için Lasso regresyon denenmiş
- L1 regularizasyon ile bazı katsayıları sıfıra çeker
- Alpha parametresi düzenleme kuvvetini kontrol eder

## Kullanılan Kütüphaneler
- **pandas**: Veri manipülasyonu
- **numpy**: Sayısal hesaplamalar
- **matplotlib**: Veri görselleştirme
- **sklearn**: Makine öğrenmesi modelleri
  - `LinearRegression`: OLS modeli
  - `Lasso`: L1 regularizasyon ile regresyon
  - `train_test_split`: Veri bölme
  - `mean_squared_error`, `r2_score`: Metrikler

## Öğrenilen Konular
1. **Teknik Analiz İndikatörleri**: Fiyat açıklık, yüksek-düşük aralığı
2. **Regresyon Analizi**: OLS ve Lasso regresyon
3. **Özellik Mühendisliği**: Finansal verilerden özellik çıkarma
4. **Model Değerlendirme**: MSE, R² metrikleri
5. **Algoritmik Ticaret**: Sinyal üretme ve strateji testi
6. **Backtesting**: Geçmiş verilerle strateji performans testi
7. **Getiri Hesaplama**: Logaritmik getiriler
8. **Strateji Karşılaştırması**: Buy & Hold vs ML stratejisi

## Dikkat Edilmesi Gerekenler
- **Lookahead Bias**: `.shift(-1)` ile gelecek verisi kullanılır, gerçek uygulamada dikkatli olunmalı
- **Overfitting**: Modelin eğitim verisine aşırı uyum sağlaması riski
- **İşlem Maliyetleri**: Gerçek dünyada komisyon ve slippage hesaba katılmalı
- **Market Conditions**: Model piyasa koşulları değiştiğinde başarısız olabilir

## Kod Hatası
Script'te bir typo var:
```python
test_r2 = r2_score(Y_Test, test_predict)  # Y_Test → Y_test olmalı
```

## Teknik Detaylar
- **Dil**: Python 3
- **Veri Seti**: Google (GOOG) hisse senedi
- **Model**: Lineer Regresyon (OLS ve Lasso)
- **Strateji**: Long-Short
- **Metrik**: Kümülatif getiri (%)
