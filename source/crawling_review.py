import time
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver

# add selenium browser option
driver = "/mnt/d/AI_BootCamp/N3XX/N3XX_Project/Sool_Han_Jan/source/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--window-size=960,960");
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) like Gecko")
browser = webdriver.Chrome(driver, options=options)
interval = 3
review = dict()


def searchReview(items, sorts):
    reviews = list()
    global review

    for idx, item in enumerate(items):
        review = {"name" : item, "sort": sorts[idx], "price" : 0, 
        "cnt_heart" : 0, "score": 0, "cnt_view": 0}
        # url = f"https://search.shopping.naver.com/search/all?query={item}&bt=-1&frm=NVSCPRO"
        # browser.get(url)
        # elements = browser.find_elements_by_class_name("subFilter_sort__rQUtM")
        
        url = f"https://www.soolmarket.com/goods/goods_search.php?adUrl=https%3A%2F%2Fwww.soolmarket.com%2Fgoods%2Fgoods_search.php%3Fkeyword%3D%25EC%2595%2588%25EB%258F%2599%25EC%2586%258C%25EC%25A3%25BC&keyword={item}&recentCount=5"
        browser.get(url)
        # elements = browser.find_elements_by_class_name("item_tit_box")
        elements = browser.find_elements_by_xpath("//*[@id=\"contents\"]/div/div[2]/div/div/div[3]/div/div/ul/li[1]/div/div[1]/a")
        if elements == []:
            reviews.append(review)
            continue
        elements[0].click()
        time.sleep(interval)
        review = (getReview(item))
        reviews.append(review)
        time.sleep(interval)
    
    # browser.close()
    return reviews

def getReview(item):
    soup = BeautifulSoup(browser.page_source, "lxml")
    global review

    price = soup.select_one("#frmView > div > div > div.item_detail_list > dl.item_price > dd > strong > strong").text
    score = soup.select_one("#plusReviewForm > div.plus_review_info > div.plus_review_num > div > div > strong").text
    cnt_post = soup.select_one("#plusReviewForm > div.plus_review_info > div.plus_review_num > div > ul > li:nth-child(1) > strong").text
    cnt_view = soup.select_one("#plusReviewForm > div.plus_review_info > div.plus_review_num > div > ul > li:nth-child(3) > strong").text
    review["price"] = int(price.replace(',',''))
    review["score"] = float(score)
    review["cnt_post"] = int(cnt_post.split(' ')[0])
    review["cnt_view"] = int(cnt_view.split(' ')[0])
    return review

def windowQuit():
    browser.quit();

names = list()
sorts = list()
file = open("data/json/sools.json")
jsonString = json.load(file)
for info in jsonString:
    names.append(info["name"])
    sorts.append(info["종류"])
# 네이버 작업 횟수 100건 이하 권장
# reviews = searchReview(names[600:700])
reviews = searchReview(names, sorts)
windowQuit()
# print(reviews)
with open('data/json/reviews.json','w') as f:
    json.dump(reviews,f)
