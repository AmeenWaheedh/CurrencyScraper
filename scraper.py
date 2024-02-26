from bs4 import BeautifulSoup as sp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import requests
import os, time, schedule, pystray
from PIL import Image
from datetime import datetime
import threading

class scraper():
    def on_tray_click(icon, item):
        print("tray icon clicked")

    def on_minimize(window):
        window.hide()
        icon = pystray.Icon("Currency Scraper", Image.open("scraper.png"), "Currency Scraper", menu = scraper.menu)
        icon.run()

    def scrape():
        print ("scraping started")
        url = "https://bankofmaldives.com.mv/exchange-rates"
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(3)
        pagesource = driver.page_source
        driver.quit()

        soup = sp(pagesource,'html.parser')
        table = soup.find_all("tr")
      #  print (table)

        data = []
        for tr in table:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            data.append(row)
        
        for rw in data[1:]:
            #inserting currency short name from the next column
            rw.insert(0,rw[0][:3])
            #amend first element to show currency name without currency short name
            rw[1] = rw[1][4:-1]
            #add two different columns for date and time
            rw.append(datetime.today().strftime('%d/%m/%Y'))
            rw.append(datetime.today().strftime('%H:%M:%S'))

        headers = ['Cur','Currency','Buy','Sell','Date', 'Time']

        df = pd.DataFrame(data, columns=headers)
        df = df[1:len(df)-3]
        
        if(os.path.isfile(r'C:\Users\USER\Documents\scrapeData.csv')):
             df.to_csv(r'C:\Users\USER\Documents\scrapeData.csv', mode='a', index = False, header = False)
             print ('data added')
        else:
             df.to_csv(r'C:\Users\USER\Documents\scrapeData.csv', index = False)
             print("filel created")

    #Function to run the schedule in a seperate thread
    def run_schedule():
        while True:
            schedule.run_pending()
            # time.sleep(24 * 60 * 60)
            time.sleep(10)

    def main():
        #start the scheduele in a seperate thread
        schedule_thread = threading.Thread(target = scraper.run_schedule)
        schedule_thread.start()


        #schedule the scraping task to run once every day
        schedule.every().day.at("07:02").do(scraper.scrape)

        #create the system tray icon
        icon = pystray.Icon("Currency Scraper", Image.open("scraper.png"), "Currency Scraper", menu = scraper.menu)
        icon.run()

    menu = (pystray.MenuItem("Currency Scraper", on_tray_click),)

    def __init__(self):
         self.main

if __name__ == "__main__":
   # app = scraper()
    scraper.main()