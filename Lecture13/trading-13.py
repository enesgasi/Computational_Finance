import requests
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
import mail_configuration

api_url = "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/cex/alpha/all/token/list"

sender = mail_configuration.sender
receiver = mail_configuration.receiver
password = mail_configuration.password

try:
    response = requests.get(api_url, timeout=10)
    info1 = response.json()
    
    for i in range(min(5, len(info1['data']))):
        symbol = info1["data"][i]['symbol']
        percent = float(info1['data'][i]['percentChange24h'])
        high = float(info1['data'][i]['priceHigh24h'])
        low = float(info1['data'][i]['priceLow24h'])
        
        print(f"Symbol: {symbol}, Percent: {percent}%")
        
        if percent > 80:
            message = f"ALERT: {symbol} +{percent}%\nHigh: {high}\nLow: {low}"
            msg = MIMEText(message)
            msg['Subject'] = f"Trading Alert: {symbol}"
            msg['From'] = sender
            msg['To'] = ', '.join(receiver) if isinstance(receiver, list) else receiver
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
                print("✅ Email sent")
except Exception as e:
    print(f"Error: {e}")