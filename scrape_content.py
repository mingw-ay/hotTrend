import requests
from model.Comment import Comment

# 本文件主要包括爬取某一页面的评论
# 需要使用的参数
headers = {
    'cookie':
    'ttcid=00bc2fa788004311b7da7442686d524226; csrftoken=c59b6047f660e65a1f661a7bd19a498a; MONITOR_WEB_ID=7009637787465680415; MONITOR_DEVICE_ID=17fb5952-8c0d-45d0-8936-ace6b7a53bed; _S_WIN_WH=1280_648; _S_DPR=1.5; _S_IPAD=0; passport_csrf_token=01d3ce90f6f6ffe1550a2b5abb15034f; tt_webid=7009637787465680415; _tea_utm_cache_2018=undefined; __ac_nonce=061946709008b9a6bb858; __ac_signature=_02B4Z6wo00f01E4Y3hQAAIDAzhokVEwgwJROPNqAAHIZw4yL4X2UkC6rIBkQdbtHM2A6GTl.RuJD-Fo7re8.YqTLtDFaPR.AdF3kXH1-Xuh6Wdoa.tuTgOmsf5OSpgXL32OCOsF0YRooG7Go22; tt_scid=M--0InyDeCuxY2RCo6CMALHYaYqLCTnAeWuSZLq5qNIPd-5FgGflSm-NKrz4AkCibd16; s_v_web_id=verify_4a220507418516811edf80b57fb86b55',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}


# 传入,news_id,news_url,boolean值（代表是不是视频）以及视频评论个数
def scrape_comment(news_id, url, is_video, commentCount):
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
    comment = Comment(news_id, '    '.join(commentList), comment_url)
    return comment
