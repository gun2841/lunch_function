import collections
import concurrent.futures
import requests
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap
import requests
import folium
import openpyxl
import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import requests
import csv
import urllib.request
import urllib.parse
import re
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import platform
from tqdm import tqdm
from time import sleep
from tqdm import trange
from haversine import haversine
cnt = 0
def whole_region(keyword, start_x, start_y, end_x, end_y):
    # print(start_x,start_y,end_x,end_y)
    page_num = 1
    # 데이터가 담길 리스트
    all_data_list = []
    while (1):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': keyword, 'page': page_num,'category_group_code':'FD6',
                  'rect': f'{start_x},{start_y},{end_x},{end_y}'}
        headers = {"Authorization": "KakaoAK 15c832307cafb72e89dbe1990cb85584"}
        ## 입력예시 -->> headers = {"Authorization": "KakaoAK f64acbasdfasdfasf70e4f52f737760657"}
        resp = requests.get(url, params=params, headers=headers)
        search_count = resp.json()['meta']['total_count']
        #print('총 개수', search_count)
        if search_count > 45:
            #print('좌표 4등분')
            dividing_x = (start_x + end_x) / 2
            dividing_y = (start_y + end_y) / 2
            ## 4등분 중 왼쪽 아래
            all_data_list.extend(whole_region(keyword, start_x, start_y, dividing_x, dividing_y))
            ## 4등분 중 오른쪽 아래
            all_data_list.extend(whole_region(keyword, dividing_x, start_y, end_x, dividing_y))
            ## 4등분 중 왼쪽 위
            all_data_list.extend(whole_region(keyword, start_x, dividing_y, dividing_x, end_y))
            ## 4등분 중 오른쪽 위
            all_data_list.extend(whole_region(keyword, dividing_x, dividing_y, end_x, end_y))
            return all_data_list
        else:
            if resp.json()['meta']['is_end']:
                all_data_list.extend(resp.json()['documents'])
                return all_data_list
            # 아니면 다음 페이지로 넘어가서 데이터 저장
            else:
                #print('다음페이지')
                page_num += 1
                all_data_list.extend(resp.json()['documents'])
def overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y):
    # 최종 데이터가 담길 리스트
    overlapped_result = []

    # 지도를 사각형으로 나누면서 데이터 받아옴
    for i in trange(1, num_x + 1):  ## 1,10
        end_x = start_x + next_x
        initial_start_y = start_y
        for j in range(1, num_y + 1):  ## 1,6
            end_y = initial_start_y + next_y
            each_result = whole_region(keyword, start_x, initial_start_y, end_x, end_y)
            overlapped_result.extend(each_result)
            initial_start_y = end_y
        start_x = end_x

    return overlapped_result
def make_map(dfs,loc_y,loc_x):
    # 지도 생성하기
    m = folium.Map(location=[loc_y,loc_x],
                   zoom_start=12)

    # 미니맵 추가
    minimap = MiniMap()
    m.add_child(minimap)

    # 마커
    for i in range(len(dfs)):
        #l = haversine((loc_y, loc_x), (float(df['Y'][i]), float(df['X'][i])), unit='m')
        folium.Marker([dfs['Y'][i],dfs['X'][i]],
                  tooltip=dfs['stores'][i],
                  popup=dfs['place_url'][i],
                  ).add_to(m)
    m.save('./test2.html')
    return m
#################### 메뉴 가져오기
def _getMenuInfo(menu):
    menuName = menu.select('.info_menu > .loss_word')[0].text
    menuPrices = menu.select('.info_menu > .price_menu')
    menuPrice = ''

    if len(menuPrices) != 0:
        menuPrice =  menuPrices[0].text.split(' ')[1]

    return [menuName, menuPrice]
def get_menu(li):
    global cnt
    options = webdriver.ChromeOptions()
    options.add_argument('lang=ko_KR')
    options.add_argument('headless')
    options.add_argument('"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36"')
    chromedriver_path = ""
    if platform.system() == "Windows":
        chromedriver_path = "./chromedriver.exe"
    elif platform.system() == "Linux":
        chromedriver_path = "./chromedriver"
    driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)

    sleep(1)
    driver.get(li[1])
    sleep(1)
    try:
        result = driver.switch_to.alert()
        result.accept()
    except:
        pass
    menuInfos = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    rate=""
    try:
        rate = soup.select_one(  '#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b').text
        menuonlyType = soup.select('.cont_menu > .list_menu > .menuonly_type')
        nophotoType = soup.select('.cont_menu > .list_menu > .nophoto_type')
        photoType = soup.select('.cont_menu > .list_menu > .photo_type')
        if len(menuonlyType) != 0:
            for menu in menuonlyType:
                menuInfos.append(_getMenuInfo(menu))
        elif len(nophotoType) != 0:
            for menu in nophotoType:
                menuInfos.append(_getMenuInfo(menu))
        else:
            for menu in photoType:
                menuInfos.append(_getMenuInfo(menu))
    except:
        pass
    #print(li)
    cnt+=1
    print(cnt)

    driver.close()
    #print(rate[:-1],menuInfos)
    return li[0],rate[:-1],menuInfos
def get_content(ID, urls):
    data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results=[]
        for i in range(len(urls)):
            results.append(executor.submit(get_menu,[ID[i],urls[i]]))
        for f in concurrent.futures.as_completed(results):
            data.append(f.result())
    return data