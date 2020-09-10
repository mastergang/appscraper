# -*- coding: utf-8 -*-
# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

class chromeDriver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # 한국어 변환 추가
        chrome_options.add_argument("lang=ko_KR")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        time.sleep(2)
        driver = webdriver.Chrome( '/data16/appscrap/chromedriver', options=chrome_options)
        time.sleep(2)
        self.driver = driver

    def get(self, url):
        self.driver.get(url)
        time.sleep(5)

    def exeScroll(self):
        no_of_pagedowns = 30
        body = self.driver.find_element_by_tag_name("body")
        while no_of_pagedowns:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns-=1

    def getHtml(self):
        return self.driver.page_source


    def close(self):
        self.driver.quit()