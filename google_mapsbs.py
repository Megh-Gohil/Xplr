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
chrome_options = Options()
filename = "data"
link = "https://www.google.co.in/maps/search/adventure+parks+in+mumbai/@19.0626321,72.7520352,12z/data=!3m1!4b1?entry=ttu"

# chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
record = []
e = []
le = 0

def Selenium_extractor():
    
    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
    data_dict = {"Name" : [], "activity_type" : [], "ratings" : [], "address" : [], "website" : [], "contact" : [], "Open/Closed" : [], "Time" : []}
    while len(a) < 1000:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()
        time.sleep(2)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

        if len(a) == var:
            le+=1
            if le > 5:
                break
        else:
            le = 0
    error_count = 0
    for i in range(len(a)):
    # for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        
        # print("scroll origin", scroll_origin.origin, scroll_origin.y_offset)
        # print("scroll_from_origin performed")
        
        action.move_to_element(a[i]).perform()
        
        a[i].click()
        action.scroll_from_origin(scroll_origin, 0, a[i].size['height']).perform()
        # print(a[i].size['height'])
        time.sleep(random.randint(2,4))
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')

        with open("html_data/google_maps.html", "w") as f:
            f.write(source)
    
        Name_Html = soup.findAll('h1', {"class": "DUwDvf fontHeadlineLarge"})
        activity_type_Html = soup.findAll('button', {"class": "DkEaL"})
        if(len(activity_type_Html) == 0):
            activity_type = "Unknown"
        else:
            activity_type = activity_type_Html[0].text
        name = Name_Html[0].text

        ratings_Html = soup.findAll('span', {"class":"ceNzKf"} )
        if(len(ratings_Html) == 0):
            ratings = "No rating available"
        else:
            ratings = ratings_Html[0]['aria-label']
        details_Html = soup.findAll('div', {"class" : "Io6YTe fontBodyMedium kR99db"})
        try:
            address = details_Html[0].text
        except:
            continue
        links = []
        link_Html = soup.findAll('div', {"class" : "gSkmPd fontBodySmall DshQNd"})
        if(len(list(link_Html)) != 0):
            for i in link_Html:
                links.append(i.text)
        contact = ""
        for i in details_Html:
            if len(str(i.text)) > 4:
                if str(i.text)[-4] == "." or str(i.text)[-3] == ".":
                    links.append(i.text)
            if(len(str(i.text)) > 6):
                if len(str(i.text)) == 12 and str(i.text)[1:6].isnumeric():
                    contact = i.text
        if(len(contact) == 0):
            contact = "Not available"
        

        open_closed = ""
        timing = ""
        try:
            time_open_close = soup.find('span',{'class':'ZDu9vd'})
            open_closed_html = time_open_close.findChildren('span', recursive=True)
            # timing_html = time_open_close.findChild('span', attr={"style" : "font-weight:400;"}, recursive=True)
            time_avail = []
            for i in list(open_closed_html):
                if not ("span" in str(i.contents[0])):
                    time_avail.append(str(i.contents[0]))
            if(len(time_avail) == 2) and (len(time_avail[0]) <= 6):
                open_closed = time_avail[0]
                timing = time_avail[1]
            elif(len(time_avail) == 1):
                if(len(time_avail[0]) <= 6):
                    open_closed = time_avail[0]
                    timing = "Unavailable"
                else:
                    timing = time_avail[0]
                    open_closed = "Unavailable"
            elif(len(time_avail) == 0):
                open_closed = "Unavailable"
                timing = "Unavailable"
            # timing = timing_html.text
        except:
            open_closed = "Unavailable"
            timing = "Unavailable"
             
        if len(open_closed) == 0:
            open_closed = "Unavailable"
        if len(timing) == 0:
            timing = "Unavailable"

        data_dict["Name"].append(name)
        data_dict["activity_type"].append(activity_type)
        data_dict["ratings"].append(ratings)
        data_dict["address"].append(address)
        data_dict["website"].append(links)
        data_dict["contact"].append(contact)
        data_dict["Open/Closed"].append(open_closed)
        data_dict["Time"].append(timing)
        
        # print(name, '||', activity_type, '||', ratings, '||', open_closed, timing)
        
            # if name not in e:
            #     e.append(name)
            #     divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})
            #     for j in range(len(divs)):
            #         if str(divs[j].text)[0] == "+":
            #             phone = divs[j].text

            #     Address_Html= divs[0]
            #     address=Address_Html.text
            #     try:
            #         for z in range(len(divs)):
            #             if str(divs[z].text)[-4] == "." or str(divs[z].text)[-3] == ".":
            #                 website = divs[z].text
            #     except:
            #         website="Not available"
            #     print([name,phone,address,website])
            #     record.append((name,phone,address,website))
            #     df=pd.DataFrame(record,columns=['Name','Phone number','Address','Website'])  # writing data to the file
            #     df.to_csv(filename + '.csv',index=False,encoding='utf-8')
    df = pd.DataFrame(data_dict)
    output_path='data_scrapped/my_csv.csv'
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
    time.sleep(2)
    browser.quit()
        


browser.get(str(link))
time.sleep(10)
Selenium_extractor()