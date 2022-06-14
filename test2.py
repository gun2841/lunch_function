import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import csv
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
import platform
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36"}

url="https://map.kakao.com/"
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
chromedriver_path=""
if platform.system()=="Windows":
    chromedriver_path= "./chromedriver.exe"
elif platform.system() == "Linux":
    chromedriver_path = "./chromedriver"
driver=webdriver.Chrome(os.path.join(os.getcwd(),chromedriver_path),options=options)

driver.get(url)
searchloc= input("test")
filename=input("파일이름")

### 검색창에 입력하기
search_area=driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
search_area.send_keys(searchloc)
driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
time.sleep(2)

data = []
def storeNamePrint():
    time.sleep(0.2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    lists = soup.select('.placelist > .PlaceItem')
    count = 1
    for list in lists:
        temp = []
        print(list)
        list_name = list.select(".head_item > .tit_name > .link_name")[0].text
        list_rate = list.select(".rating > .score > .num")[0].text
        review = list.select(".rating > .review")[0].text
        link = list.select(".contact > .moreview")[0]['href']
        addr = list.select(".addr")[0].text
        category=list.select(".subcategory")[0].text
        # info\.search\.place\.list > li:nth-child(1) > div.head_item.clickArea > span
        review = review[3:len(review)]

        review = int(re.sub(",", "", review))

        print(list_name, list_rate, review, link, addr)
        temp.append(list_name)
        temp.append(list_rate)
        temp.append(review)
        temp.append(link)
        temp.append(addr)
        temp.append(category)
        data.append(temp)

### 장소탭 누르기
driver.find_element_by_xpath('//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER)
spage=1
epage=0
time.sleep(1)
for i in range(0,34):
    try:
        epage+=1
        print("**",spage,"**")
        page= f'//*[@id="info.search.page.no{epage}"]'
        driver.find_element_by_xpath(page).send_keys(Keys.ENTER)
        storeNamePrint()
        if(epage)%5==0:
            driver.find_element_by_xpath('//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
            epage=0
        spage+=1
    finally:
        pass
f = open(filename+".csv","w",encoding="utf-8-sig",newline="")
writercsv=csv.writer(f)
header=['Name','Rate','Review','Link','Addr','category']
writercsv.writerow(header)
for i in data:
    writercsv.writerow(i)
print("end")