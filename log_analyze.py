#usr/bin/env python
import glob
import re
from collections import Counter
from argparse import ArgumentParser
from dateutil.parser import parse


#オプション引数の指定
def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-s','--since',type = str , default = "0001/01/01",help = 'Aggregate from this date. YYYY/MM/DD')#集計開始日
    argparser.add_argument('-u','--until',type = str , default = "9999/12/31",help = 'Aggregate up to this date. YYYY/MM/DD')#集計終了日
    return argparser.parse_args()
    
#str型の日時を与えるとdatetime型に変換して返す関数
def date_to_datetime(date_str):
    return parse(date_str,fuzzy = True,yearfirst = True)

#リモートホスト毎のアクセス回数を表示する関数
def ip_access_counter(since_date,until_date):
    print("=============access_logフォルダ内のログファイルを読み込みます=============")
    ip_count = Counter()
    #globを使ってaccess_logフォルダ内の全てのログファイルを読み込む(1つずつ)
    for log_file in glob.glob('./access_log/*.log'):
        with open(log_file) as f:
            #読み込んだファイルから１行ずつ読み込む(メモリ対策)
            for log in f:
                try:
                    log_day = re.findall(r'\[([\w:/]+\s[+\-]\d{4})\]',log) #アクセス日時を正規表現で抽出
                    log_day = date_to_datetime(log_day[0]) #アクセス日時をdatetime型に変換
                    ip_in_log = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',log) #リモートホストのIPアドレスを正規表現で抽出
                    since = date_to_datetime(since_date + ' 00:00:00 +0900') #集計開始日(datetime型)
                    until = date_to_datetime(until_date + ' 23:59:59 +0900') #集計終了日(datetime型)
                    if since <= log_day <= until: #アクセス日時が集計期間中なら
                        ip_count += Counter(ip_in_log) #Counterでipアドレスをカウント
                    else:
                        pass
                except IndexError:# 改行で１データが分割されてしまっていて、IndexErrorが発生した場合
                    pass #何もせず、次の行へ行く
                del log #カウント処理が終わった行のメモリ解放
            print("ログファイル　"+ str(log_file) +"を読み込みました") #logファイルを読み込めているか確認するために表示
            f.close()   #ログファイル分のメモリ解放
    
    #以下、結果出力部分
    print("\n")
    print("=============IPアドレスとアクセス回数を表示します(アクセス回数が多い順)=============")
    print("\n")
    print("アクセス回数集計日時:")
    print(since)
    print("～")
    print(until)
    print("\n")
    ip_count = ip_count.most_common() #アクセス回数が多い順にソート
    for address , count in ip_count: #出力
        print("IPアドレス "+ str(address) + " のアクセス回数は " + str(count) + "回 です")

#時間毎のアクセス回数を表示する関数
def time_access_counter(since_date,until_date):
    print("=============access_logフォルダ内のログファイルを読み込みます=============")
    time_count = Counter()
    #globを使ってaccess_logフォルダ内の全てのログファイルを読み込む(1つずつ)
    for log_file in glob.glob('./access_log/*.log'):
        with open(log_file) as f:
            #読み込んだファイルから１行ずつ読み込む(メモリ対策)
            for log in f:
                try:
                    time_in_log = re.findall(r'\[([\w:/]+\s[+\-]\d{4})\]',log) #アクセス日時を正規表現で抽出
                    log_day = date_to_datetime(time_in_log[0]) #アクセス日時をdatetime型に変換
                    since = date_to_datetime(since_date + ' 00:00:00 +0900') #集計開始日(datetime型)
                    until = date_to_datetime(until_date + ' 23:59:59 +0900') #集計終了日(datetime型)
                    if since <= log_day  <= until: #アクセス日時が集計期間中なら
                        time_count += Counter(time_in_log) #Counterでアクセス時間(str型)をカウント
                    else:
                        pass
                except IndexError: #改行で１データが分割されてしまっていて、IndexErrorが発生した場合
                    pass #何もせず、次の行へ行く
                del log #カウント処理が終わった行のメモリ解放
            print("ログファイル　"+ str(log_file) +"を読み込みました") #logファイルを読み込めているか確認するために表示
            f.close()  #ログファイル分のメモリ解放
            
    #結果出力部分
    print("\n")
    print("=============時間ごとのアクセス回数を表示します(時間順)=============")
    print("\n")
    print("アクセス回数集計日時:")
    print(since)
    print("～")
    print(until)
    print("\n")
    #時間順に表示させるため、Counterのタプルを[[datetime,アクセス回数],[...],[...]]のリストに変換する
    time_list = list(time_count.items())
    time_list_for_out =[]
    for time in range(len(time_list)):
        time_and_times = []
        time_and_times.append(date_to_datetime(time_list[time][0]))
        time_and_times.append(time_list[time][1])
        time_list_for_out.append(time_and_times)
        
    time_list_for_out = sorted(time_list_for_out,key=lambda y: y[0]) #sorted関数にDatetimeを渡して時間が古い順にソートする
    for time , count in time_list_for_out: #出力
        print("時間； "+ str(time) + " のアクセス回数は " + str(count) + "回 です")
    
if __name__ == '__main__':
    args = get_option() #オプションを取得
    print("集計対象期間:" + str(args.since) +"～" + str(args.until))
    print("何を行いますか？")
    print("[1]:アクセス回数計算（リモートホスト毎）\n[2]:アクセス回数計算（時間毎)")
    choose_action = input('1 or 2 :')
    if choose_action == str(1):
        ip_access_counter(args.since,args.until)
    elif choose_action == str(2):
        time_access_counter(args.since,args.until)
    else:
        print("エラー：不明な入力です。")
