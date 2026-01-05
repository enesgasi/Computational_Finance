<?php

/*
$a=5;
$b=4;
$c=$a+$b;
echo("The total=$c");
*/
require("bin_class.php");
$key = '';
$secret = '';
$bnb = new Binance\binali($key,$secret, ['useServerTime'=>True]);
$bnb->useServerTime();
/*
$ticker =$bnb->bookPrices();
$b_price =$ticker['BTCUSDT']['bid'];
$w_price =$ticker['WBTCUSDT']['bid'];
echo("BTC price=".$b_price);
echo("<br>");
echo("WBTC price=".$w_price);
*/
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
    $price_ratio = $b_price/$w_price;
    $price_ratio = 0.99;
    if ($price_ratio>(1+2*$t_f) and $balance1>0){
        echo('<br> Sell BTC and Buy WBTC');
        //$bnb->sell("BTCUSDT",1, $b_price);
        //bnb->buy("WBTC", $quantity, $w_price);
        //balance2=(balance1*price_ratio(i))*(1-2*t_f);
        //balance1 = 0;
    }

    if ($price_ratio<(1-2*$t_f) and $balance2>0){
        echo('<br> Sell WBTC and Buy BTC');
        //balance2 = (balance1*price_ratio(i)) *(1-2*t_f)
    }
    sleep(15);
}


?>