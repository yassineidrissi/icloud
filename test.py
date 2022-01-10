import pandas as pd 
import csv
from datetime import datetime 
import time
from os.path import exists
import os


#check if there is any file under the trader name or no ; return True or Flase 
def csv_exisit(name):
    return os.path.exists(f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv")

#creat Date frame and save to file under the trader name 

def Creat_Data_Frame(name):
    header = ["Time","Trader","Pair","Size","Side","Entry","Marked_Price","PNL","ROI","Date/Time of last update","leverage"]
    df = pd.DataFrame(columns=header)
    df = df.set_index("Time")
    df = df.dropna()
    df.to_csv(f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv")
    return (df)


def FillDataFrame(name,fixed_list,df):
    header = ["Trader","Pair","Size","Side","Entry","Marked_Price","PNL","ROI","Date/Time of last update","leverage"]
    df = pd.DataFrame(columns=header)
    for i in fixed_list:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        df = df.append({header[0]:name,header[1]:(i[0]),header[2]:(i[1]),header[3]:(i[2]),
        header[4]:(i[3]),header[5]:(i[4]),header[6]:(i[5]),header[7]:(i[6]),header[8]:(i[7]),header[9]:(i[8]),"Time":dt_string},
        ignore_index=True)
        time.sleep(2)
    df = df.set_index("Time")
    df = df.dropna()
    df.to_csv(f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv")
    return (df)


lst = [['ETHUSDT', -1441.538, 'Short', 3853.33, 3854.94, -2323.73, -0.2091, '2021-12-14 21:42:50', 5],
['BTCUSDT', -29.835, 'Short', 47760.48, 48337.67, -17220.48, -23.8816, '2021-12-14 12:01:59', 19],
['AXSUSDT', -5199.0, 'Short', 96.08, 95.86, 1151.02, 2.3095, '2021-12-14 12:24:48', 9]]

def CSV(name):
    if csv_exisit(name) == False:
        df = Creat_Data_Frame(name)
        return(df)
    else:
        df =  pd.read_csv(f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv")
        return(df)

def csv_exit(name,fixed_list):
    df = pd.read_csv(f"dataframe\{name}.csv") 
    return(FillDataFrame(name,df,fixed_list))    
    
def csv_reduce(name,fixed_list):
    df = pd.read_csv(f"dataframe\{name}.csv")
    

























