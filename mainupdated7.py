import os 
import logging
import pickle
import time
from termcolor import colored 
#from config import DispatchToTelegram, ExPositions, ExtractName, ExtractSoup, HandlePosition, Load_Pickle,  pickle_it, telegram_bot_sendtext
import config3
logging.basicConfig(filename="file7.log",level=logging.INFO,format="%(asctime)s:%(levelname)s:%(message)s")

#cast 
url = "https://www.binance.com/en/futures-activity/leaderboard?type=myProfile&tradeType=PERPETUAL&encryptedUid=6864A4EF8B67EDA5A35B98A6C2014B37"


def main2(url,new_position = True):
    while True:
        soup = config3.ExtractSoup(url)
        name = config3.ExtractName(soup)
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
            config3.DispatchToTelegram(name,fixed_position) 
            config3.pickle_it(name,fixed_position)
            saved_list = config3.Load_Pickle(name)
            print(colored("SAVED LIST","red")) 
            for i in saved_list:
                print(colored(i,"red"))
            new_position = False
        delta = config3.DetectChanges(name,saved_list,fixed_position)
        print(colored("DELTA","green"))
        print(colored(delta,"green"))
        saved_list = fixed_position
        config3.telegram_bot_sendtext(delta)
        time.sleep(60)
        
if __name__ == "__main__":
    main2(url)


