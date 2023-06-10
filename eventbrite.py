from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import random
from selenium.webdriver.chrome.options import Options
import os
import subprocess

chrome_options = Options()
filename = "data"
link = "https://www.eventbrite.com/d/india--mumbai/all-events/?page="

# chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
record = []
e = []
le = 0

event_ids = []

def Selenium_extractor():
    
    action = ActionChains(browser)
    # with open("eventbrite_data/ev.html", "w") as file:
    #     file.write(browser.page_source)
    time.sleep(2)

    a = browser.find_elements(By.XPATH, '//div[@data-testid="event-card-tracking-layer"]')
    
    for i in a:
        event_ids.append(i.get_attribute("data-event-id"))
        

for i in range(7):
    time.sleep(2)
    try:
        browser.get(str(link) + str(i+1))
        time.sleep(2)
        Selenium_extractor()
    except:
        continue
browser.quit()
unique_event_ids = [*set(event_ids)]
website1 = "https://www.eventbrite.com/api/v3/destination/events/?event_ids="
website2 = "&expand=event_sales_status,image,primary_venue,saves,ticket_availability,primary_organizer,public_collections"
for i in unique_event_ids:
    cmd = subprocess.Popen(["GET", website1 + str(i) + website2], stdout=subprocess.PIPE)
    time.sleep(2)
    output = str(cmd.communicate())
    print(output[0])
    break