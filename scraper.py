from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
from datetime import date, datetime
import time
import os
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

'''
    Selenium stuff - setting the config for the Chromdriver which we will use
    to scrape the site. 
'''
service = Service(executable_path='./chromedriver')
options = Options()
options.add_argument('--incognito')
options.add_argument('--headless') # Comment this out if you want to watch it scrape the site 
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=service, options=options)

URL = "https://nuforc.org/subndx/?id=lPA"
NEXT_BUTTON_XPATH = '//*[@id="table_1_next"]'
NUMBER_OF_PAGES = 51

# Make sure the Next button exists before we try to click it.
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

driver.get(URL)
time.sleep(5) # Pause to make sure chrome loads the data before we try to read it ...

html = driver.page_source
table = bs(html, features='html.parser')
table_titles = table.find_all('th')
table_headers = [title.text for title in table_titles]
df = pd.DataFrame(columns=table_headers)

print("Created DataFrame with headers from table")
print(table_headers)

for i in range(0, NUMBER_OF_PAGES + 1):
    print(f'Reading page {i+1}')
    time.sleep(2)
    
    html = driver.page_source

    table = bs(html, features='html.parser')
    column_data = table.find_all('tr')

    prev_len = len(df)

    for row in column_data[1:]:
        row_data = row.find_all('td')
        each_row_data = [data.text for data in row_data]
        
        length = len(df)
        df.loc[length] = each_row_data

    df.drop(df.tail(1).index,inplace=True) 
    print(f'Succesfully read {len(df) - prev_len} rows into DataFrame')
    print(df.head)

    if check_exists_by_xpath(driver, NEXT_BUTTON_XPATH):
        element = driver.find_element(By.XPATH, NEXT_BUTTON_XPATH)
        driver.execute_script('arguments[0].scrollIntoView();', element)
        driver.execute_script('window.scrollBy(0, -200);')
        element.click()
        print("Clicked next page button ...")
        break
    else:
        break
        print('No next page - scraping complete :)')


today = date.today()
output_path =f'data/nuforc_data_PA-{today}.csv'
df.to_csv(output_path, index=False)

print(f'Successfully read data to {output_path}')