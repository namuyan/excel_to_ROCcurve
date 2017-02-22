# excel_to_ROCcurve  
===================  
## Description  
エクセルファイルを入力すると容易にROCカーブのプロットデータを別のエクセルファイルに書き出すことができます。何か問題があればTwitterまでご連絡ください。


Overview

## Demo  
`python3 excel_to_ROCcurve.py -h`  
使い方はhelpをご覧ください。使用にはPython3である必要があります。

`python3 excel_to_ROCcurve.py -i inputfile.xlsx -x 0`  
*inputfile.xlsx.result.xls*が出力されます。  
グラフ作成は散布図をお勧めします。


## Requirement
Anaconda3を入れていれば問題ありません。  
必要なパッケージは**numpy, xlrd, xlwt**です。


## Install
右手は添えるだけ...


## Usage
オプションは**-i**の入力と、**-x**のシートインデックス入力のみです。  
インデックスは０から始まりますのでご注意ください。


## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[@namuyan_mine](https://twitter.com/namuyan_mine/)
