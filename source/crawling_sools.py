import time
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver

# add selenium browser option
driver = "/mnt/d/AI_BootCamp/N3XX/N3XX_Project/Sool_Han_Jan/source/chromedriver" 
options = webdriver.ChromeOptions()
options.add_argument("--window-size=960,960");
browser = webdriver.Chrome(driver, options=options)
interval = 3

def movingPages(nums, work):
    sools = list()
    idx = 0

    #"https://thesool.com/front/find/M000000082/list.do?searchType=2&searchKey=&searchKind=&levelType=&searchString=&productId=&pageIndex={page}&categoryNm=&kind="
    if work == 0:
        url = "https://thesool.com/front/find/M000000082/list.do?searchType=2&searchKey=&searchKind=&levelType=&searchString=&productId=&pageIndex="
        idx = 1
        while True:
            browser.get(url + str(idx))
            if not getProductNum(nums):
                break
            idx += 1
            time.sleep(interval)
        return nums
    for num in nums:
        browser.get(f"https://thesool.com/front/find/M000000082/view.do?searchType=2&searchKey=&searchKind=&levelType=&searchString=&productId={num}")
        sools.append(getInfo(num))
        idx += 1
        time.sleep(interval)
        # browser.close()
    return sools

def getProductNum(nums):
    soup = BeautifulSoup(browser.page_source, "lxml")
    if soup.find_all("div", attrs={"class":"no-data"}) != []:
        return
    items = soup.find_all("div", attrs={"class":"name"})
    for item in items:
        num = item['onclick'].split("'")[1]
        nums.append(num)
    return nums

def getInfo(num):
    dict_info = dict()
    soup = BeautifulSoup(browser.page_source, "lxml")

    name = soup.find("dt", attrs={"class":"subject"}).text
    image = soup.find("div", attrs={"class":"thumb"})
    info_list = soup.find("ul", attrs={"class":"info-list"}).find_all("li")
    dict_info['productNum'] = num
    dict_info['name'] = name
    dict_info['image'] = image.find("img")["src"]
    for item in info_list:
        feature = item.find_next("strong").text.strip()
        value = item.find_next("span").text.strip()
        dict_info[feature] = value
    return dict_info

productNums = list()
movingPages(productNums, 0)
sools = movingPages(productNums, 1)
with open('data/json/sools.json','w') as f:
    json.dump(sools,f)
