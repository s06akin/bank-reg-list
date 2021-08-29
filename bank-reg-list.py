import requests
from bs4 import BeautifulSoup
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', minutes=5)
def scheduled_job():
    data = []
    result = []
    reg = []
    
    url = 'https://cbr.ru/banking_sector/likvidbase/PartSelectorState1//'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    find_table = soup.find('table', class_='data')
    
    rows = find_table.find_all('tr')
    
    for row in rows:
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
        
    
    
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('sunnyasobakin@gmail.com','oxK6Ukzz5ve3AE')
    
    message = '\n\n'.join(["Subject: bank_list", "\r\n".join(reg)])
    smtpObj.sendmail("sunnyasobakin@gmail.com","sunnyasobakin@gmail.com", message)
    # ta_exch_mon_sis@nsd.ru

sched.start()