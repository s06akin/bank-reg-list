import requests
from bs4 import BeautifulSoup
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=6, minute=50)
def scheduled_job():
    data = []
    result = []
    reg = []
    
    otzyv_url = 'https://cbr.ru/banking_sector/likvidbase/PartSelectorState1//'
    otzyv_response = requests.get(otzyv_url)
    otzyv_soup = BeautifulSoup(otzyv_response.text, 'lxml')
    otzyv_find_table = otzyv_soup.find('table', class_='data')
    otzyv_rows = otzyv_find_table.find_all('tr')

    for row in otzyv_rows:
        cols = row.find_all('td')
        cols = [el.text.strip() for el in cols]
        if cols:
            data.append([el for el in cols if el])

    for i in data:
        for j in i: 
            result.append(j)
    
    for index in range(len(result)):
        if index % 2 == 0:
            reg.append(result[index])
        

    moratoriy_url = 'https://cbr.ru/banking_sector/PrBankrot/moratoriy/'
    moratoriy_response = requests.get(moratoriy_url)
    moratoriy_soup = BeautifulSoup(moratoriy_response.text, 'lxml')
    moratoriy_find_dropdown = moratoriy_soup.find('div', id='DropDown_content')
    moratoriy_find_table = moratoriy_find_dropdown.find('table')
    moratoriy_find_reg = moratoriy_find_table.find_all('td', width='60px')

    moratoriy_reg = [el.text.strip() for el in moratoriy_find_reg] 

    if len(moratoriy_reg) != 0:
        for index in range(len(moratoriy_reg)):
            reg.append(moratoriy_reg[index])
        
    
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('sunnyasobakin@gmail.com','kdvteoxtngppxkxz')
    
    message = '\n\n'.join(["Subject: bank_list", "\r\n".join(reg)])
    smtpObj.sendmail("sunnyasobakin@gmail.com","ta_exch_mon_sis@nsd.ru", message)

sched.start()