import time
from selenium.webdriver import Chrome, ChromeOptions
from util.newsdb import get_news, update_news_body


# 登录方法
def login():
    option = ChromeOptions()
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    option.add_argument('ignore-certificate-errors')
    driver = Chrome(options=option)
    return driver


# 爬取方法
def spider(driver, source):
    text_body = ''
    try:
        driver.execute_script("window.scrollTo(0,500);")
        # 可能是环球网
        if source == '环球网':
            try:
                driver.find_element_by_xpath('//*[@id="more"]').click()
            except:
                pass
            text_body = driver.find_element_by_class_name('a-con').text
        elif source == '全国党媒信息公共平台':
            text_body = driver.find_element_by_class_name('detail-pubs').text
        else:
            driver.find_element_by_tag_name('article').click
            text_body = driver.find_element_by_tag_name('article').text
    except Exception as e:
        print(e)
        pass
    return text_body


def get_news_body(newsList):
    # 循环爬取
    for i in range(10):
        print(newsList[i].article_url)
        # 前往网址
        driver.get(newsList[i].article_url)
        # 等待加载
        # time.sleep(2)
        # 将返回的正文去除换行
        for j in range(4):
            textbody = spider(driver, newsList[i].source).replace('\n', '')
            if textbody != '':
                break
        newsList[i].article_body = textbody[0:1000]
    update_news_body(newsList)


# 1.调用登陆方法打开浏览器
driver = login()

start = 0
newsList = get_news()
print(len(newsList))
for i in range(40):
    logging = '正在爬取：'
    try:
        # for i in range(start, start+10):
        #     logging = logging+' ' + str(newsList[i].news_id)
        # print(logging)
        # news_id = newsList[start+10].news_id
        # print(f'接下来从{news_id}开始爬')
        get_news_body(newsList[start:])
        # get_news_body(newsList[start:start+10])
        print('爬取10个新闻主体并插入数据库')
        start += 10
    except:
        get_news_body(newsList[start:])
    break


# with open('./url_list.txt', 'w+', encoding='utf-8') as f:
#     for i, news in enumerate(newsList):
#         newsList[i] = news.article_url + '\t' + news.source
#     f.write('\n'.join(newsList))


# driver = login()
# driver.get('http://toutiao.com/group/7032199876079272484/')
# time.sleep(2)
# textbody = spider(driver, '环球')
# print(len(textbody))
