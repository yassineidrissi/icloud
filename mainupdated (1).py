import os 
import logging
import pickle
import time
from termcolor import colored 
#from config import DispatchToTelegram, ExPositions, ExtractName, ExtractSoup, HandlePosition, Load_Pickle,  pickle_it, telegram_bot_sendtext
import config3
logging.basicConfig(filename="data/file1.log",level=logging.INFO,format="%(asctime)s:%(levelname)s:%(message)s")

#tradinghorse
url = "https://www.binance.com/en/futures-activity/leaderboard?type=myProfile&tradeType=PERPETUAL&encryptedUid=D64DDD2177FA081E3F361F70C703A562"


saved_list = [] 


def main2(url,new_position = True):
    config3.telegram_bot_sendtext(url)
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
    try:
        main2(url)
    except:
        config3.telegram_bot_sendtext(f" 🚧🚧🚧 {name} disconnected 🚧🚧🚧 ")

