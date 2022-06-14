import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('lang=ko_KR')
chromedriver_path = "./chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기

def main():
    global driver, menu_wb

    driver.implicitly_wait(4)
    driver.get('https://map.kakao.com/')

    search("당산역 음식점")

    driver.quit()
    print("finish")


def search(place):
    global driver

    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')
    search_area.send_keys(place)
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
    sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    search_area.clear()
    # 1페이지 크롤링
    place_lists = soup.select('.placelist > li')  # 장소 목록 list
    crawling(place_lists)

    # 더보기 클릭해서 2페이지
    try:
        driver.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
        sleep(1)
        # 2 페이지 이후 크롤링 시작
        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            search_page = soup.select("#info\.search\.page > .pageWrap > a")
            sleep(1)
            for i in range(1,len(search_page)+1):
                xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
                driver.find_element_by_xpath(xPath).send_keys(Keys.ENTER)
                place_lists = soup.select('.placelist > li')  # 장소 목록 list
                crawling(place_lists)
            next_page='//*[@id="info.search.page.next"]'
            disable=soup.select('#info\.search\.page\.next')[0].attrs['class'][0]
            if disable != "next":

                break
            driver.find_element_by_xpath(next_page).send_keys(Keys.ENTER)
            sleep(1)
    except ElementNotInteractableException:
        print('not found')
    finally:
        search_area.clear()

def crawling(placeLists):
    for i, place in enumerate(placeLists):
        find_tag = place.attrs['class'][0]
        if find_tag=='AdItem':
            print("find!!!!!!!!!!!!!!!!")
        else:
            #menuInfos = getMenuInfo(i, driver)
            #print(menuInfos)
            Info=getInfo(i,driver)
            print(Info)

def getInfo(i,driver):
    detail_page_xpath = '//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]'
    driver.find_element_by_xpath(detail_page_xpath).send_keys(Keys.ENTER)
    driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환
    sleep(1)
    Infos = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    sleep(1)
    # mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2
    # mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2
    title = soup.select_one('#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2')
    rate = soup.select_one('#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b')
    #category = soup.find('#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > span.txt_location')[0].text
    print(title)
    Infos.append(title.text)
    Infos.append(rate.text)
    #Infos.append(category)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환
    return Infos

def getMenuInfo(i, driver):
    # 상세페이지로 가서 메뉴찾기

    detail_page_xpath = '//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]'
    driver.find_element_by_xpath(detail_page_xpath).send_keys(Keys.ENTER)
    driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환
    sleep(1)

    menuInfos = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 메뉴의 3가지 타입
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

    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환

    return menuInfos

def _getMenuInfo(menu):
    menuName = menu.select('.info_menu > .loss_word')[0].text
    menuPrices = menu.select('.info_menu > .price_menu')
    menuPrice = ''

    if len(menuPrices) != 0:
        menuPrice =  menuPrices[0].text.split(' ')[1]

    return [menuName, menuPrice]

if __name__ == "__main__":
    main()