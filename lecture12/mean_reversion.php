<?php
require("bin_class.php");
//require("key_secret.php");
$key='';
$secret='';
$bnb=new Binance\binali($key, $secret, ['useServerTime'=>True]);
$bnb->useServerTime();
$data1=$bnb->candlesticks('ETHUSDT','1d',365);
$data2=$bnb->candlesticks('XRPUSDT','1d',365);
//echo("ETH Price <br>");
//print_r($data1);
//echo("<br> XRP Price");
//print_r($data2);



//print_r($data);
$keys1=array_keys($data1);
$keys2=array_keys($data2);
//print_r($keys1);


for($i=0; $i<count($keys1); $i++){
    $close1=$data1[$keys1[$i]]['close'];
    $close2=$data2[$keys2[$i]]['close'];
    //echo($close);
    //echo"<br>";
    $price1[$i]=$close1;
    $price2[$i]=$close2;

    $ratio[$i]=$close1/$close2;
}

$mean1=array_sum($ratio)/count($ratio);


function standard_deviation($aValues, $bSample = false)
{
    $fMean = array_sum($aValues) / count($aValues);
    $fVariance = 0.0;
    foreach ($aValues as $i)
    {
        $fVariance += pow($i - $fMean, 2);
    }
    $fVariance /= ( $bSample ? count($aValues) - 1 : count($aValues) );
    return (float) sqrt($fVariance);
}

$std1=standard_deviation($ratio);

echo("<br>ETH Price <br>");
print_r($price1);
echo("<br> XRP Price<br>");
print_r($price2);
echo("<br> Ratio<br>");
print_r($ratio);
echo("<br> mean Ratio<br>");
echo($mean1);
echo("<br> STD Ratio<br>");
echo($std1);


while(1){
    $binance_ticker=$bnb->bookPrices();
    $eth_price=$binance_ticker['ETHUSDT']['bid'];
    $xrp_price=$binance_ticker['XRPUSDT']['bid'];
    $zscore= ($eth_price/$xrp_price-$mean1)/$std1;
    echo("<br> ZSCORE<br>");
    echo($zscore);
    if (abs($zscore)>1){
        echo("<br> Enter<br>");
    }
    if (abs($zscore)<0.5){
        echo("<br> Exit <br>");
    }
    sleep(5);
}

//echo("<br> ZSCORE<br>");
//echo($zscore);






//print_r($price);
/*
$file=fopen('series.csv','w');
fputcsv($file,$price);
fclose($file);

$file2=fopen('series.txt','w');
for($i=0; $i<count($keys); $i++){
    $close=$data[$keys[$i]]['close'];
    fwrite($file2,"$close");
    fwrite($file2,"\n");
}
fclose($file2);


$file3=fopen('BTC_USDT_day.m','w');
fwrite($file3,"data1=[");
for($i=0; $i<count($keys); $i++){
    $close=$data[$keys[$i]]['close'];
    fwrite($file3,"$close");
    fwrite($file3,"\n");
}
fwrite($file3,"];");

fclose($file3);
*/


?>