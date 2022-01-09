from bs4 import BeautifulSoup
import os
from termcolor import colored 
from datetime import datetime 
import requests
import pickle
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import logging
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains  
from datetime import datetime 

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome("/home/amrokamalelsiddig/projects/chromedriver", options=chrome_options)
os.system("clear")



def ExtractSoup(link):
    driver.get(link)
    driver.implicitly_wait(10)
    #position_tab = driver.find_element_by_id("tab-MYPOSITIONS")
    WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, "tab-MYPOSITIONS" )).click()
    #position_tab.click()
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    time.sleep(1)
    return(soup)



def ExtractName(soup):
    name = soup.find("div",{"class":"css-1kmpww2"}).text
    return(name)

def Validator(soup):
    test_list = [] 
    for position in soup.find_all("td",{"class":"rc-table-cell"}):
        test_list.append(position.text)
    test_list.remove("No result")
    if len(test_list) < 5 :
        validator = 0
    else:
        validator = 1
    return(validator)

def ExPositions(soup):
    positions = [] 
    for position in soup.find_all("td",{"class":"rc-table-cell"}):
        if position.text == "No result":
            pass
        else:
            positions.append(position.text)
    return (positions)

def telegram_bot_sendtext(bot_message):
    bot_token = "1895906452:AAHFC6CDlxo3NnIOADD7ULVHC7FY0zoCdUc"
    bot_chatID = '-1001499346072'
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def DispatchToTelegram(name , FixedList):
        nl = "\n"
        emoji = 0
        negative = '🔻' 
        positive = '💹'
        for i in FixedList:
            #emoji = '🟢' if i[8] < 20 else '🟠' if i[8] < 50 else '🔴'
            side = 0 
            if i[5] >= 0 :
                side = positive
            else:
                side = negative
            if i[8] < 20:
                emoji = '🟢'
            elif i[8] > 20 and i[8] < 50:
                emoji = '🟠'
            elif i[8] > 51 :
                emoji = '🔴'
            text = (
            f"{str(name)}"                                          + nl +
            "Pair           "  +     i[0]                           + nl +
            "Side           "  +     i[2]                           + nl +
            "Size           "  + str(i[1])                          + nl +
            "Entry Price    "  + str(i[3])                          + nl +
            "PNL            "  + str(round(i[5],0)) +" $"  + " " + str(side) + nl +
            "ROI            "  + str(i[6]) +" %"  + " " + str(side) + nl +
            "@              "  + str(i[7])                          + nl +
            "Leverage       "  + str(round(i[8],0)) + " "+ str(emoji))
            
        return (telegram_bot_sendtext(text))



def HandlePosition(RawPositionList):
    FixedPositionInfo = []   
    for i in RawPositionList:
        i = i.replace(",","")
        if "USDT" in i:
            FixedPositionInfo.append(i)
        elif "USD" in i:
            FixedPositionInfo.append(i)
        elif "BUSD" in i:
            FixedPositionInfo.append(i)
        elif "%)" in i:
            i = i.replace("%)","")
            i = i.split(" (")
            try:
                FixedPositionInfo.append(float(i[0]))
                FixedPositionInfo.append(float(i[1]))
            except ValueError:
                FixedPositionInfo.append(0)                
                FixedPositionInfo.append(0)
        elif ("-" and ":") in i:
            FixedPositionInfo.append(i)
        else:
            FixedPositionInfo.append(float(i))
    MotherOfPosition = [[]for i in range(int(len(FixedPositionInfo)//7))]
    FirstElement = 0
    LastElement = 7
    for position in range(len(MotherOfPosition)):
        MotherOfPosition[position] = FixedPositionInfo[FirstElement:LastElement]
        LastElement += 7
        FirstElement += 7
    leverge = 0
    for i in MotherOfPosition:
        try:    
            leverge =  round(int((i[1]*i[3])/(i[4]/i[5]))/100,0)
            leverge = int(leverge)
            if leverge < 0 :
                leverge = leverge * -1
                leverge = int(leverge)
            i.append(leverge)
        except ZeroDivisionError or TypeError:
            i.append(1)
        if i[1] < 0:
            i.insert(2,"Short")
        else:
            i.insert(2,"Long")
    return (MotherOfPosition)

def pickle_it(name,Fixed_List):
    now = datetime.now()
    now = time.strftime("%m-%d, %H-%M")
    file = open(f"{name}","wb")
    pickle.dump(Fixed_List,file)
    file.close()
    print(colored(">>>>>> This from pickle_it","cyan"))
    return print(colored(f"**** Position of {name} Saved Successfully ****","green"))

            
def Load_Pickle(name):
    file = open(f"{name}","rb")
    SavedList = pickle.load(file)
    return(SavedList)
    
def number_of_pages(soup):
    for countofpages in  soup.find_all("div",{"class":"css-b0tuh4"}):
        for x in countofpages.text:
            x = x
    return(x)



def status_checker(current_time):
    current_time= current_time.rsplit(":")
    if int(current_time[2]) == (30) or int(current_time[2]) == (00):
        return telegram_bot_sendtext("🟢 bot is running ")

def DispatchToTelegram2(FixedList):
        nl = "\n"
        emoji = 0
        negative = '🔻'
        positive = '💹'
        for i in FixedList:
            #emoji = '🟢' if i[8] < 20 else '🟠' if i[8] < 50 else '🔴'
            side = 0
            if i[5] >= 0 :
                side = positive
            else:
                side = negative
            if i[8] < 20:
                emoji = '🟢'
            elif i[8] > 20 and i[8] < 50:
                emoji = '🟠'
            elif i[8] > 51 :
                emoji = '🔴'
            text = (
            "Pair           "+     i[0]                                                    + nl +
            "Side           "+     i[2]                                                    + nl +
            "Size           "+ str(i[1])  + " /$ " + str(round(float(i[1]) *float(i[3]),1))+ nl +
            "Entry Price    "+ str(i[3])                                                   + nl +
            "PNL            "+ str(round(i[5],0)) +" $"  + " " + str(side)                 + nl +
            "ROI            "+ str(i[6]) +" %"  + " " + str(side)                          + nl +
            "@              "+ str(i[7])                                                   + nl +
            "Leverage       "+ str(round(i[8],0)) + " "+ str(emoji)                        + nl +
            " #######################################################\n")
        return (text) 

def DetectChanges(name, listA, listB):
    smallListA = [i[0] for i in listA]
    smallListB = [i[0] for i in listB]

    answer = ""

    for i in range(len(smallListA)):
        if smallListA[i] in smallListB:
            tempB = listB[smallListB.index(smallListA[i])]
            if (float(listA[i][1] ) < float(tempB[1])) and (listA[i][2] == "Long"): answer += f"{name} just increased size {smallListA[i]} from {listA[i][1]} to {tempB[1]} \n \n"
            elif (float(listA[i][1]  ) > float (tempB[1])) and (listA[i][2] == "Short") : answer += f"{name} just increased size {smallListA[i]} from {listA[i][1]} to {tempB[1]}  \n \n" 
    
            elif (float(listA[i][1]) > float(tempB[1])): answer += f"{name} just reduced size {smallListA[i]} from {listA[i][1]} to {tempB[1]}\n \n"
            if(listA[i][2]!=tempB[2]):
                answer += f"{name} flipped {smallListA[i]} position from {listA[i][2]} to {tempB[2]} with {tempB[1]}\n \n"
            if(listA[i][-1]!=tempB[-1]):
                answer += f"{name} changed leverage on {smallListA[i]} \n position from {listA[i][-1]} >>>>>>>>>>  {tempB[-1]}\n \n"
        else:
            answer += f"{name} just closed {smallListA[i]} position at {listA[i][4]} \n \n"
    smallListB = [i for i in smallListB if i not in smallListA]
    for i in smallListB:
        new = ""
        new = [pair for pair in listB if pair not in listA]
        DisptachToTelegram2(new)
        answer += f"{name} just opened new {i} position\n {new}"
    answer = answer[:-1]
    return answer
