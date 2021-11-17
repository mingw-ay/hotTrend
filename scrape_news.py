from model.News import News
from scrape_content import scrape_comment
from util.newsdb import add_news, add_comments, get_newsNum
from scrape_content import scrape_comment
import requests
import time
import execjs

# 需要爬取的评到及id
array_channel_id = [
    '3189398996', '3189399007', '3189398999',  '3189398972', '3189398957',
    '3189398984', '3189398981', '3189398995', '3189398960', '3189398968'
]
array_channel_name = [
    'hot', 'finance', 'tech', 'entertainment', 'sports', 'fashion',
    'digital', 'game', 'military', 'world'
]
headers = {
    'cookie':
    'ttcid=00bc2fa788004311b7da7442686d524226; csrftoken=c59b6047f660e65a1f661a7bd19a498a; MONITOR_WEB_ID=7009637787465680415; MONITOR_DEVICE_ID=17fb5952-8c0d-45d0-8936-ace6b7a53bed; _S_WIN_WH=1280_648; _S_DPR=1.5; _S_IPAD=0; passport_csrf_token=01d3ce90f6f6ffe1550a2b5abb15034f; tt_webid=7009637787465680415; _tea_utm_cache_2018=undefined; __ac_nonce=061946709008b9a6bb858; __ac_signature=_02B4Z6wo00f01E4Y3hQAAIDAzhokVEwgwJROPNqAAHIZw4yL4X2UkC6rIBkQdbtHM2A6GTl.RuJD-Fo7re8.YqTLtDFaPR.AdF3kXH1-Xuh6Wdoa.tuTgOmsf5OSpgXL32OCOsF0YRooG7Go22; tt_scid=M--0InyDeCuxY2RCo6CMALHYaYqLCTnAeWuSZLq5qNIPd-5FgGflSm-NKrz4AkCibd16; s_v_web_id=verify_4a220507418516811edf80b57fb86b55',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

# 记录本次爬取新闻的序号以及爬取时间戳（10位）
initial_behot_time = int(time.time())
try:
    newsNum = get_newsNum()+1
except Exception as e:
    newsNum = 1


# 将时间戳转换为正常时间格式的方法
def convertToTime(timestamp):
    # 转为localtime
    time_local = time.localtime(timestamp)
    # 使用strftime转为需要的格式
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


# 每个板块的爬虫方法：
def scrape_channel(channel_id, max_behot_time):
    # 全局newsNum
    global newsNum
    # 得到created
    created = max_behot_time
    max_behot_time = 0
    # 循环10次爬取该频道
    for i in range(0, 10):
        # 爬取新闻列表的api
        feed_url = f'https://www.toutiao.com/api/pc/list/feed?channel_id={channel_id}&max_behot_time={max_behot_time}&category=pc_profile_channel'
        # 运行acrawler.js得到返回值
        with open('acrawler.js', encoding='utf-8') as f:
            js_data = f.read()
        c = execjs.compile(js_data)
        feed_url = c.call("getUrl", f'{feed_url}')
        # 打印最终要爬取的url
        print(feed_url)
        # 开始爬取
        feeds = requests.get(feed_url, headers=headers,
                             timeout=30).json()['data']
        # 改变最大时间
        try:
            max_behot_time = feeds[len(feeds) - 1]['behot_time']
        except:
            continue

        # 初始化列表
        newsList = []
        commentList = []

        # 循环得到的新闻
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

            # 排除所有视频
            if 'video' in feed['tag'] or '视频' in keywordStr:
                continue

            # 得到初始的news_id
            news_id = newsNum
            news = News(news_id, created, feed['title'], '#'+feed['tag'], feed['Abstract'],
                        feed['display_url'], convertToTime(feed['behot_time']),
                        convertToTime(feed['publish_time']),
                        feed['comment_count'], feed['like_count'],
                        feed['read_count'], feed['source'], keywordStr)
            newsNum += 1

            # 将处理后的news接入列表
            newsList.append(news)

            # 判断该新闻是否有评论
            if feed['comment_count'] != 0:
                # 判断该新闻是否视频
                is_video = False
                if '视频' in keywordStr:
                    is_video = True
                # 调用爬取评论方法
                comment = scrape_comment(news_id, feed['display_url'],
                                         is_video, feed['comment_count'])
                # 将得到的comment对象接入列表
                commentList.append(comment)

        # 加入数据库
        add_news(newsList)
        add_comments(commentList)

        # 休息一会儿，防止被怀疑
        time.sleep(1)


# 循环，爬取每一个频道
for channel_id in array_channel_id:
    # the news_array feeds
    print('scrape from channel',
          array_channel_name[array_channel_id.index(channel_id)])
    scrape_channel(channel_id=channel_id, max_behot_time=initial_behot_time)
