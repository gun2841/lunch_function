import os
from time import sleep
from selenium import webdriver
import urllib.request
import platform

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')
chromedriver_path =""
if platform.system()=="Windows":
    chromedriver_path= "./chromedriver.exe"
elif platform.system() == "Linux":
    chromedriver_path = "./chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기
print(driver)
driver.implicitly_wait(4)  # 렌더링 될때까지 기다린다 4초
driver.get('https://pf.kakao.com/_xcwwCs')  # 주소 가져오기


imgs = driver.find_element_by_class_name("link_thumb")
imgs.click()
sleep(1)
img = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div/div/img").get_attribute("src")
print(img)
urllib.request.urlretrieve(img,"./menu.jpg")
