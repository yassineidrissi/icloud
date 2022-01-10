import os 
import logging
import pickle
import time
from termcolor import colored 
#from config import DispatchToTelegram, ExPositions, ExtractName, ExtractSoup, HandlePosition, Load_Pickle,  pickle_it, telegram_bot_sendtext
import pandas as pd
import config3
from test import CSV,FillDataFrame
#logging.basicConfig(filename="file1.log",level=logging.INFO,format="%(asctime)s:%(levelname)s:%(message)s")

#tradinghorse
url = "https://www.binance.com/en/futures-activity/leaderboard?type=myProfile&tradeType=PERPETUAL&encryptedUid=A532C4316C00206168F795EDFBB3E164"

saved_list = [] 

def main2(url,new_position = True):
    while True:
        soup = config3.ExtractSoup(url)
        global name 
        name = config3.ExtractName(soup)
        df = CSV(f"{name}")
        print(name)
        raw_position = config3.ExPositions(soup)         
        print(raw_position)
        if raw_position == []:
            print(colored("system sleeping zzz...","green"))
            time.sleep(30)
            continue
        fixed_position = config3.HandlePosition(raw_position)
        print(colored("fixed_position","blue"))
        for i in fixed_position:
            print(colored(i,"blue"))
        if new_position is True:
            #config3.DispatchToTelegram(name,fixed_position) 
            config3.pickle_it(name,fixed_position)
            df2 = FillDataFrame(name,fixed_position,df)
            df = df.append(df2)
            df.to_csv(f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv")
            saved_list = config3.Load_Pickle(name)
            print(colored("SAVED LIST","red")) 
            for i in saved_list:
                print(colored(i,"red"))
            new_position = False
        delta = config3.DetectChanges(name,saved_list,fixed_position)
        print(colored("DELTA","green"))
        print(colored(delta,"green"))
        saved_list = fixed_position
        #config3.telegram_bot_sendtext(delta)
        time.sleep(60)
        

if __name__ == "__main__":
    main2(url)
    time.sleep(10)
