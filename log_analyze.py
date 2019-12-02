#usr/bin/env python
import glob
import re
from collections import Counter
from argparse import ArgumentParser
from dateutil.parser import parse

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-s','--since',type = str , default = "0001/01/01",help ='Aggregate from this date. YYYY/MM/DD')
    argparser.add_argument('-u','--until',type = str , default = "9999/12/31",help = 'Aggregate up to this date. YYYY/MM/DD')
    return argparser.parse_args()
    
def date_to_datetime(date_str):
    return parse(date_str,fuzzy = True,yearfirst = True)

def ip_access_counter(since_date,until_date):
    print("=============ログファイルを読み込みます=============")
    ip_count=Counter()
    for log_file in glob.glob('./access_log/*.log'):
        with open(log_file) as f:
            for log in f:
                log_day = re.findall(r'\[([\w:/]+\s[+\-]\d{4})\]',log)
                log_day = date_to_datetime(log_day[0])
                ip_in_log = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',log)
                since = date_to_datetime(since_date + ' 00:00:00 +0900')
                until = date_to_datetime(until_date + ' 23:59:59 +0900')
                if since <= log_day <= until:
                    ip_count += Counter(ip_in_log)
                else:
                    pass
                del log
            print("ログファイル　"+ str(log_file) +"を読み込みました")
            f.close()   
    print("\n")
    print("=============IPアドレスとアクセス回数を表示します(アクセス回数が多い順)=============")
    print("\n")
    print("アクセス回数集計日時:")
    print(since)
    print("～")
    print(until)
    print("\n")
    ip_count = ip_count.most_common()
    for address , count in ip_count:
        print("IPアドレス "+ str(address) + " のアクセス回数は " + str(count) + "回 です")
        
def time_access_counter(since_date,until_date):
    print("=============ログファイルを読み込みます=============")
    time_count = Counter()
    for log_file in glob.glob('./access_log/*.log'):
        with open(log_file) as f:
            for log in f:
                time_in_log = re.findall(r'\[([\w:/]+\s[+\-]\d{4})\]',log)
                log_day = date_to_datetime(time_in_log[0])
                since = date_to_datetime(since_date + ' 00:00:00 +0900')
                until = date_to_datetime(until_date + ' 23:59:59 +0900')
                if since <= log_day  <= until:
                    time_count += Counter(time_in_log)
                else:
                    pass
                del log
            print("ログファイル　"+ str(log_file) +"を読み込みました")
            f.close() 
    print("\n")
    print("=============時間ごとのアクセス回数を表示します(時間順)=============")
    print("\n")
    print("アクセス回数集計日時:")
    print(since)
    print("～")
    print(until)
    print("\n")
    time_list = list(time_count.items())
    time_list_for_out =[]
    for time in range(len(time_list)):
        time_and_times = []
        time_and_times.append(date_to_datetime(time_list[time][0]))
        time_and_times.append(time_list[time][1])
        time_list_for_out.append(time_and_times)
        
    time_list_for_out = sorted(time_list_for_out,key=lambda y: y[0])
    for time , count in time_list_for_out:
        print("時間； "+ str(time) + " のアクセス回数は " + str(count) + "回 です")
    
if __name__ == '__main__':
    args = get_option()
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