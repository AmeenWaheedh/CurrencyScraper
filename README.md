# CurrencyScraper
Python application to scrape BML Exchange rates data daily

The application scrapes data from https://www.bankofmaldives.com.mv/exchange-rates and works from system tray.
Data is added to a scv file which is then used as a source for Currency Visualizer applications. It focuses on graphical representation of currency rate variances over time.

After scraping, CurrencyScraper waits for 10 seconds and schedules for next days task. Runs every day mornig at 7:02
