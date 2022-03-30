# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from Tools import Alert
from OperacteData import InsertOperaction
import datetime

# 无用函数


def doNothing():
    return

# 爬数


def GetData():
    getTime=0
    month = datetime.datetime.now().strftime('%Y%m')
    InsertSql = "INSERT INTO `weibohot`.weibohot_" + month + " ( `node`, `hot_num`) VALUES "
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    chrome_options = Options()
    # 定义无窗口运行,否则在服务器环境会报错
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(
        chrome_options=chrome_options, executable_path="/usr/local/bin/chromedriver")
    # /usr/local/bin/chromedriver
    while  True:
        if getTime > 5:
            Alert('微博热搜搜集异常')
            break
        getTime=getTime+1
        try:
            browser.get(url)
        except:
            Alert("微博热搜网址异常")
        else:

            time.sleep(10)
            xpath = '//*[@id="pl_top_realtimehot"]/table/tbody/tr'
            elems = browser.find_elements_by_xpath(xpath)

            for elem in elems:
                try:
                    int(elem.find_element_by_class_name('td-01').text)
                except:
                    doNothing()
                else:
                    info = elem.find_element_by_class_name('td-02').text
                    title = info.split(' ')[0]
                    num = info.split(' ')[-1]
                    InsertSql = InsertSql + '(\'' + title + '\',' + num + '),'
            InsertSql = re.sub(r',$', ';', InsertSql)
        
        if InsertSql != "INSERT INTO `weibohot`.weibohot_" + month + " ( `node`, `hot_num`) VALUES ":
 
            InsertOperaction(InsertSql)
            break
    browser.quit()
    return InsertSql
