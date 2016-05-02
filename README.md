# StockPrediction

決定木を使って株価の変動を予測します。株価データをダウンロードする「scraper」と予測を行う「prediction」に分かれています。

## Scraper

Yahoo! ファイナンスから株価データをダウンロードします。ダウンロードする銘柄は `targets.txt` で設定します。
`targets.txt` はタブ区切りテキストファイルです。1列目に銘柄コード、2列目に株価データを保存するファイル名を指定します。
`RunScraper.py` を実行すると Scraper が動きます。

## Prediction

Scraper が生成した株価データを用いて、株価の変動を予測します。利用する株価データは `targets.txt` で設定します。
1銘柄につき、短期(5日)、長期(25日) の変動予測を10回行います。10回予測した平均値を 0 以上 1 以下の値で算出します。
平均値が 0 の場合は株価は上昇しない(下がるか横ばい)という予測結果になります。平均値が 1 の場合は株価は上昇するという予測結果になります。
`RunPredict.py` を実行すると Prediction が動きます。


## 成績

検証中です。


## 参考

* http://qiita.com/ynakayama/items/6a472e5ebbe9365186bd
