from model.News import News
from util.newsdb import add_news
import requests
import time
import execjs

# then there're those channels that we want
array_channel_id = [
    '3189398996', '3189399007','3189398999',  '3189398972', '3189398957',
    '3189398984', '94349549395', '3189398981', '3189398995', '3189398965',
    '3189399004', '3189398960', '3189398983', '3189398959', '3189398968'
]
array_channel_name = [
    'hot', 'finance', 'tech', 'entertainment', 'sports', 'fashion', 'food',
    'digital', 'game', 'history', 'baby', 'military', 'travel', 'regimen',
    'world'
]
headers = {
    'cookie':
    'ttcid=6c3e28f42423412caa4378942dcbe36f23; csrftoken=4efb247cc103db0866e0fb0efe1865a8; MONITOR_WEB_ID=6988780148074038791; tt_webid=7009957373263824398; __ac_nonce=0614d434f00ef9e7a2a05; __ac_signature=_02B4Z6wo00f01wbHT9gAAIDBTeMfqNJx.Y8G40tAAKEGByDXQvfpb9YjqUCLswNFT64CgdfQGSFDaeOvMCOWqb4PIVzTo-sRekpV9-iJE6QeoHqtKX4pfbcBUodJgxxSmF3.ANLWc2.diGeS7d; s_v_web_id=verify_ktxsn1qj_I54FCrES_wtX6_4kZE_AApw_lZAWN4jDZttV; tt_scid=-AYM1AjQQmFOwd99R.7aeNxLWE.zsj3Q5Nu05qrjWOBD0GSVdO0A3UquMcrSlf8lc79d',
    'user-agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}


# we need a function for convert timestamp
def convertToTime(timestamp):
    # make it localtime
    time_local = time.localtime(timestamp)
    # then shift it to the new time style
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


# 每个板块的爬虫方法：
def scrape_channel(channel_id, max_behot_time=int(time.time())):
    # loop for 10 times
    for i in range(0, 11):
        # the url for the certain api
        feed_url = f'https://www.toutiao.com/api/pc/list/feed?channel_id={channel_id}&max_behot_time={max_behot_time}&category=pc_profile_channel'
        # 运行acrawler.js得到返回值
        with open('acrawler.js', encoding='utf-8') as f:
            js_data = f.read()
        c = execjs.compile(js_data)
        feed_url = c.call("getUrl", f'{feed_url}')
        # 打印最终要爬取的url
        print(feed_url)
        # 开始爬取
        feeds = requests.get(feed_url, headers=headers).json()['data']
        # 改变最大时间
        max_behot_time = feeds[len(feeds) - 1]['behot_time']

        # give me a NewsList
        NewsList = []

        # loop through feed and get what we need
        for feed in feeds:
            # 可能是新闻没有tag，故而排除没有tag的元素
            if feed.get('tag') == None:
                continue

            # 得到关键词字符串
            keywordStr = ''
            filter_words = feed['filter_words']['filter_words']
            for fwords in filter_words:
                if fwords['name'].startswith('不想看'):
                    # 将关键词假如keywordStr中去
                    keywordStr = keywordStr + fwords['name'].replace(
                        '不想看:', '') + ','

            # 创建news对象
            news = News(feed['title'], feed['tag'], feed['Abstract'],
                        feed['article_url'], convertToTime(feed['behot_time']),
                        convertToTime(feed['publish_time']),
                        feed['comment_count'], feed['like_count'],
                        feed['read_count'], feed['source'], keywordStr)

            # append news to the list
            NewsList.append(news)
            # news.greeting()

        # add the list to database
        add_news(NewsList)

        time.sleep(1)


# 循环，爬取每一个频道
for channel_id in array_channel_id:
    # the news_array feeds
    print('scrape from channel',
          array_channel_name[array_channel_id.index(channel_id)])
    scrape_channel(channel_id)
