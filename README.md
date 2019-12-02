# fixpoint　プログラミング試験用プログラム
fixpointのプログラミング試験用のプログラムです。

## 使用した言語、外部ライブラリ
プログラミング言語:Python 3.7  
外部ライブラリ:dateutil

## ファイル構成

access_log:集計対象のアクセスログファイルを格納するフォルダです。  
log_analyze.py:アクセス回数を集計して表示するプログラムです。

## 何ができるのか
Apacheのログファイル(.log)を読み込み、  
・リモートホスト(IPアドレス)ごとのアクセス回数　もしくは  
・時間(秒単位）ごとのアクセス回数  
を計算し、表示します。

## 使い方
### ① git リポジトリをクローンする
以下のコマンドを実行し、リポジトリをクローンします。 

```
$ git clone https://github.com/KSthjpngyg/fixpoint_kadai
```

### ②Apacheのアクセスログファイル(～.log)をaccess_logフォルダ直下に置く
集計対象の全アクセスログファイルをリポジトリ内の access_log フォルダ直下に置いてください。  
access_log フォルダ内にある全てのログファイル(～.log)が集計対象になります。

### ③log_analyze.pyを実行
fixpont_kadai フォルダ内の log_analyze.py を実行してください。  

```shell
$ home>cd fixpont_kadai
$ home/fixpoint_kadai>python log_analyze.py

```

log_analyze.pyに以下のオプション値を渡すことで、集計期間を指定できます。

|オプション|意味|入力形式| 
----|----|---- 
|-s , --since|集計開始日|YYYY/MM/DD| 
|-u , --until|集計終了日|YYYY/MM/DD| 

期間を指定して集計する場合は以下のように記述してください。  
(例:2019/12/02 00:00:00 ~ 2019/12/05 23:59:59 を対象にする場合）

```shell
$ home/fixpoint_kadai>python log_analyze.py --since 2019/12/02 --until 2019/12/05
```

### ④リモートホスト毎に集計するか、時間毎に集計するか選択する
log_analyze.pyを実行すると、集計対象期間を表示し、  
リモートホスト(IPアドレス)ごとにアクセス数を集計するか、  
時間(秒単位）ごとにアクセス数を集計するかを聞きます。  
1を入力するとリモートホスト(IPアドレス）ごとのアクセス数を集計し表示します。  
2を入力すると時間(秒単位)ごとのアクセス数を集計し表示します。
