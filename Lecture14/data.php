<?php

// $a = 5;
// $b = 4;
// $c = $a + $b;

// echo("The total is equal to $c");

require("bin_class.php");
$key = '';
$secret = '';
$bnb = new Binance\binali($key, $secret, ['useServerTime' => True]);
$bnb -> useServerTime(); // timestamp is unique identifier.
$data = $bnb->candlesticks('BTCUSDT', '1d',1000);
// print_r($data[1758657600000+60*60*1000]['close']);
$keys=array_keys($data);
// print_r($keys);
for($i = 0; $i<count($keys); $i++){
    // echo($data[$keys[$i]]['close']);
    // echo("<br>");
    $price[$i] = $data[$keys[$i]]['close'];
}

print_r($price);
$file=fopen('BTC_USDT_day.csv','w');
fputcsv($file, $price);
fclose($file);


// $file2=fopen('SOL_series.txt','w');
// for($i = 0; $i<count($keys); $i++){
//     $price[$i] = $data[$keys[$i]]['close'];
//     fwrite($file2, $price[$i]);
//     fwrite($file2, "\n");
// }
// fclose($file2)


?>