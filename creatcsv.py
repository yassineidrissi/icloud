from typing import Dict
import pandas as pd 
import csv
from datetime import datetime 
import time
from os.path import exists
import os

from pandas.core.frame import DataFrame 
#os.system("cls") 

dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                   
lst = [['ETHUSDT', -1441.538, 'Short', 3853.33, 3854.94, -2323.73, -0.2091, '2021-12-14 21:42:50', 5],
['BTCUSDT', -29.835, 'Short', 47760.48, 48337.67, -17220.48, -23.8816, '2021-12-14 12:01:59', 19],
['AXSUSDT', -5199.0, 'Short', 96.08, 95.86, 1151.02, 2.3095, '2021-12-14 12:24:48', 9]]


#check if csv file exisit or not if not to creat new csv file under user name 
def csv_exisit(name):
    return os.path.exists(f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv") 

#funcation  to creat csv file and 
def Creat_Data_Frame(name,fixed_list):
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

def Creat_Data_Frame2(name,fixed_list):
    header = ["Time","Trader","Pair","Size","Side","Entry","Marked_Price","PNL","ROI","Date/Time of last update","leverage"]
    df = pd.DataFrame(columns=header)
    df = df.set_index("Time")
    df = df.dropna()
    df.to_csv(f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv")
    return (df)




# if_not_csv_creat("HAMZA",lst)



#Pass updated data frame after 
def appendDFToCSV_void(df, csvFilePath, sep=","):
    import os
    if not os.path.isfile(csvFilePath):
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
    elif len(df.columns) != len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns):
        raise Exception("Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns)) + " columns.")
    elif not (df.columns == pd.read_csv(csvFilePath, nrows=1, sep=sep).columns).all():
        raise Exception("Columns and column order of dataframe and csv file do not match!!")
    else:
        df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)
    
def if_not_csv_creat(name,fixed_list,df):
    if (csv_exisit(name)) == False:
        Creat_Data_Frame2(name=name,fixed_list=fixed_list)
    else:
        appendDFToCSV_void(df,f"/home/amrokamalelsiddig/updated_parasites/dataframes/{name}.csv",sep=",")

header = ["Time","Trader","Pair","Size","Side","Entry","Marked_Price","PNL","ROI","Date/Time of last update","leverage"]
df = pd.DataFrame(columns=header)
if_not_csv_creat("amro",lst,df)

