
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# add selenium browser option
options = webdriver.ChromeOptions()
options.add_argument("--window-size=960,960");

def crawlingSools():

    sools = dict()
    idx = 0

    # 모든 술의 정보 가져오기
    for page in range(1, 100):
        # open web page "thesool.com"
        browser = webdriver.Chrome("../chromedriver", options=options)
        url = f"https://thesool.com/front/find/M000000082/list.do?searchType=2&searchKey=&searchKind=&levelType=&searchString=&productId=&pageIndex={page}&categoryNm=&kind="
        browser.get(url);

        # get product information
        elem = browser.find_elements_by_class_name("item");

        # 한 페이지의 모든 술의 상세 정보 긁어오기
        for e in elem:
            # get image link
            try:
                image = e.find_element_by_tag_name("img").get_attribute("src")
                product_num = image.split('=')[1].split('&')[0]
            except:
                continue;
            # define BeautifulSoup object of current page
            soup = BeautifulSoup(e.text, "lxml")
            sool = soup.find('p').get_text()
            info = sool.split('\n')
            # info add in dict
            name = info[0]
            if ("(중복)" in name) | ("(단종)" in name):
                continue;
            ingredient = info[2].split('주원료 ')[1]
            ingredient = ingredient.strip(" 등").split(", ")
            proof = info[3].split('/')[2]
            if len(info) > 5:
                feature = info[5]
            else:
                feature = "";
            sools[idx] = {"image":image, "product_num":product_num,
                    "name":name, "ingredient":ingredient,
                 "proof":proof.strip(), "intro":feature}
            idx+=1;
        time.sleep(2);

    time.sleep(2);
    browser.quit();
    return sools;

sools = crawlingSools();
print(len(sools));
for sool in sools.values():
    print(sool["name"]);
