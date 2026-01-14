margin = 0.10;
price = [price1, price2, price3, price4];

%amount1 = 100;
%amount2 = 100;
amount(1:4) = 100;
t_f = 1/1000;

for i = 1:365  % Her gün için
    
    % Her varlığın güncel değerini hesapla
    for k = 1:4
        value(k) = price(i, k) * amount(k);
    end    
    avg_value = mean(value);  % Ortalama değer

    % Eğer herhangi bir varlık ortalamadan %10+ sapma gösteriyorsa
    ___________(1)        
        for k=1:4
            if value(k) > avg_value
                % Fazla olan varlığı sat
                __________(2)
                __________(3)
            else
                % Eksik olan varlığı al

                __________(4)
                __________(5)
            end
        end    
    end    
end

/*
Cevaplar:
(1): if max(value) > avg_value * (1 + margin) || min(value) < avg_value * (1 - margin)
(2): difference = value(k) - avg_value;
(3): amount(k) = amount(k) - ((1 + t_f * difference/price(i,k))
(4): diffeence = avg_value -value(k)
(5): amount(k) = amount(k) - ((1 - t_f * difference/price(i,k))
*/

