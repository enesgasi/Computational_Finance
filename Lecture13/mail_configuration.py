"""
Email Configuration Module
--------------------------
Bu dosya trading-13.py scripti için email ayarlarını içerir.

KULLANIM:
1. Yandex Mail hesabınızla giriş yapın (https://mail.yandex.com)
2. Ayarlar → Güvenlik → Uygulama şifreleri bölümünden yeni şifre oluşturun
3. Aşağıdaki bilgileri kendi bilgilerinizle güncelleyin
4. Bu dosyayı .gitignore'a ekleyin (güvenlik için)

NOT: Gerçek email ve şifrenizi asla GitHub'a yüklemeyin!
"""

# Email gönderen adresi (Yandex Mail)
sender = "your_email@yandex.com"

# Email alıcı adresleri (liste formatında)
# Tek alıcı: ["recipient@example.com"]
# Birden fazla alıcı: ["recipient1@example.com", "recipient2@example.com"]
receiver = ["recipient@example.com"]

# Yandex Mail uygulama şifresi
# NOT: Normal şifrenizi değil, "Uygulama Şifresi" kullanın
# Yandex → Ayarlar → Güvenlik → Uygulama şifreleri
password = "your_app_password_here"

# SMTP Sunucu Ayarları (Yandex için varsayılan)
smtp_server = "smtp.yandex.com"
smtp_port = 465

# Test için örnek ayarlar (kullanmadan önce gerçek bilgilerle değiştirin!)
# sender = "trading_bot@yandex.com"
# receiver = ["trader1@gmail.com", "trader2@yahoo.com"]
# password = "abcd1234efgh5678"
