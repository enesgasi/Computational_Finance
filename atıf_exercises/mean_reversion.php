<?php

$mean1=array_sum($ratio)/count($ratio);
$std1=standard_deviation($ratio);

while(1){
    $binance_ticker=$bnb->bookPrices();
    $eth_price=$binance_ticker['ETHUSDT']['bid'];
    $xrp_price=$binance_ticker['XRPUSDT']['bid'];
    $zscore= ___________(1)
    echo("<br> ZSCORE<br>");
    echo($zscore);
    if ___________(2) {
        echo("<br> Enter<br>");
    }
    if ___________(3) {
        echo("<br> Exit <br>");
    }
    sleep(5);
}

/*
Cevaplar:
(1): ($eth_price/$xrp_price-$mean1)/$std1;
(2): (abs($zscore)>1)
(3): (abs($zscore)<0.5)
*/

?>