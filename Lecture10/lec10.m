clc; clear all; close all;
BTC_USDT_hour
price1 = data1; 
WBTC_USDT_hour
price2 = data1; 

figure(1)
plot(price1, 'b');
hold on;
plot(price2,'r');
legend('BTC_USDT','WBTC_USDT');
xlabel('Time (hours)');
ylabel('Price');
price_ratio = price1./price2;

figure(2)
plot(price_ratio)

balance1 = 1
balance2 = 0 

t_f =1/1000; 

for i=1:length(price_ratio)
    if(price_ratio(i)>(1+2*t_f) & balance1 > 0)
    i
    display('Sell BTC and Buy WBTC')
    balance2 =(balance1*price_ratio(i))*(1-2*t_f);
    balance1 = 0;
    end
    if(price_ratio(i)<(1-2*t_f) & balance2 > 0)
    i
    display('Sell BTC and Buy WBTC')
    balance1 =(balance2/price_ratio(i))*(1-2*t_f);
    balance2 = 0;
    end
end

final_balance = balance1+ balance2



clc; clear all; close all;
BTC_USDT_day
price1 = data1(51:1000); 
WBTC_USDT_day
price2 = data1; 

figure(1)
plot(price1, 'b');
hold on;
plot(price2,'r');
legend('BTC_USDT','WBTC_USDT');
xlabel('Time (day)');
ylabel('Price');
price_ratio = price1./price2;

figure(2)
plot(price_ratio)

balance1 = 1
balance2 = 0 

t_f =1/1000; 

for i=1:length(price_ratio)
    if(price_ratio(i)>(1+2*t_f) & balance1 > 0)
    i
    display('Sell BTC and Buy WBTC')
    balance2 =(balance1*price_ratio(i))*(1-2*t_f);
    balance1 = 0;
    end
    if(price_ratio(i)<(1-2*t_f) & balance2 > 0)
    i
    display('Sell WBTC and Buy BTC')
    balance1 =(balance2/price_ratio(i))*(1-2*t_f);
    balance2 = 0;
    end
end

final_balance = balance1+ balance2