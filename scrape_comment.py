import requests
from model.Comment import Comment

# 本文件主要包括爬取某一页面的评论
# 需要使用的参数
headers = {
    'cookie':
    '__ac_nonce=0619904ac00774a934109; __ac_signature=_02B4Z6wo00f01fZ5f1QAAIDBdnuFF-l27KH2WXvAABwJJOITcIIQvCaWnuuyqVzCLSSdIV40tuS.xII6Su3CmWtdTdgquB6Q-MeQPzrPV0OxzgzX0VidOveTIEhbbLsvTEU69a0Jo1HTgKbmf8; csrftoken=ef3f0b25a019f5d84be837edeb46fb53; MONITOR_WEB_ID=7009637787465680415; s_v_web_id=verify_5af18547cbf141431b5b247abb20749c; _tea_utm_cache_2018=undefined; MONITOR_DEVICE_ID=b8774009-19de-48e5-b864-73b0c0841d35; tt_scid=n5K00FVbJZ.6M9HtiJJR5NPGJIo-6XwsnNExZxeQlv9H.tkUrXz1ADC-jIf26sS3b2c9',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}


# 传入,news_id,news_url,boolean值（代表是不是视频）以及视频评论个数
def get_comment(news_id, url, is_video, commentCount):
    # 得到新闻id及评论个数
    if commentCount > 30:
        commentCount = 30
    group_id = url.split('/')[4]
    # 得到评论链接
    if(is_video):
        comment_url = f'https://www.ixigua.com/tlb/comment/article/v5/tab_comments/?tab_index=0&count={commentCount}&group_id={group_id}&item_id={group_id}&aid=1768'
    else:
        comment_url = f'https://www.toutiao.com/article/v2/tab_comments/?aid=24&app_name=toutiao_web&offset=0&count={commentCount}&group_id={group_id}&item_id={group_id}'
    # 爬取api
    data = requests.get(comment_url).json()['data']
    commentList = []
    comment_len = 0
    for item in data:
        text = item['comment']['text']
        comment_len += len(text)
        if comment_len < 600:
            commentList.append(text)
    # 返回
    comment = Comment(news_id, url, '    '.join(commentList), comment_url)
    return comment
