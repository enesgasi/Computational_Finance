<?php

$balance1 = 1;
$balance2 = 0;

$t_f =1/1000; 

while(1){
    $ticker =$bnb->bookPrices();
    $b_price =$ticker['BTCUSDT']['bid'];
    $w_price =$ticker['WBTCUSDT']['bid'];
    echo("BTC price=".$b_price);
    echo("<br>");
    echo("WBTC price=".$w_price);

    $price_ratio = --(1)
  

    if --(2) {
        echo('<br> Sell BTC and Buy WBTC');
        //$bnb->sell("BTCUSDT",1, $b_price);
        //bnb->buy("WBTC", $quantity, $w_price);
        //balance2=(balance1*price_ratio(i))*(1-2*t_f);
        //balance1 = 0;
    }

    if --(3) {
        echo('<br> Sell WBTC and Buy BTC');
        //balance2 = (balance1*price_ratio(i)) *(1-2*t_f)
    }
    sleep(15);
}

/*
Cevaplar
(1): $b_price/$w_price;
(2): ($price_ratio>(1+2*$t_f) and $balance1>0);
(3): ($price_ratio<(1-2*$t_f) and $balance2>0);
*/

?>