<?php
require("bin_class.php");
//require("key_secret.php");
$key='';
$secret='';
$bnb=new Binance\binali($key, $secret, ['useServerTime'=>True]);
$bnb->useServerTime();

$ticker=$bnb->bookprices();
$buyprice=$ticker['ETHUSDT']['bidPrice'];
$sellprice=$ticker['ETHUSDT']['askPrice'];
echo "Buy Price: $buyprice\n";
echo "Sell Price: $sellprice\n";
$eth_ticker=$ticker['ETHUSDT'];
print_r($eth_ticker);

$day_info=$bnb->prevDay();
print_r($day_info[5]);
$percent=$day_info[5]['priceChangePercent'];
echo "24h Change Percent: $percent%\n";
echo("price percent change=$percent%\n");

for ($i=0;$i<count($day_info);$i++) {
    $percent=$day_info[$i]['priceChangePercent'];
    if ($percent > 20) 
    {
        $symbol=$day_info[$i]['symbol'];
        echo ("<br>symbol=$symbol --percent== $percent%\n");

    }
}