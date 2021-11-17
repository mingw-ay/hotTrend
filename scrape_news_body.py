import csv
import time
from selenium.webdriver import Chrome, ChromeOptions
from util.newsdb import get_news


# 登录方法
def login(url):
    option = ChromeOptions()
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)
    return driver


# 爬取方法
def spider(driver):
    try:
        text_body = driver.find_element_by_tag_name('article').text
        return text_body
    except Exception as e:
        return ''


# 从数据库中得到所有新闻
newsList = get_news()
# 调用登陆方法
driver = login(newsList[0].article_url)
# 打开一个csv文件用于保存newsid和对应的新闻主题
f = open('news_body.csv', 'a+', encoding='utf8')
newsWriter = csv.writer(f, delimiter=',', lineterminator='\n')
newsWriter.writerow(['news_id', 'news_body'])
# 循环爬取
for news in newsList[1:]:
    # 前往网址
    driver.get('news.article_url')
    # 等待加载
    time.sleep(3)
    # 将返回的正文去除换行
    textbody = spider(driver).replace('\n', '')
    # 追加一行
    newsWriter.writerow([news.news_id, textbody])

f.close()
