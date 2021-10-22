import requests
from model.Comment import Comment

# 本文件主要包括爬取某一页面的评论
# 需要使用的参数
headers = {
    'cookie':
    'ttcid=6c3e28f42423412caa4378942dcbe36f23; csrftoken=4efb247cc103db0866e0fb0efe1865a8; MONITOR_WEB_ID=6988780148074038791; tt_webid=7009957373263824398; __ac_nonce=0614d434f00ef9e7a2a05; __ac_signature=_02B4Z6wo00f01wbHT9gAAIDBTeMfqNJx.Y8G40tAAKEGByDXQvfpb9YjqUCLswNFT64CgdfQGSFDaeOvMCOWqb4PIVzTo-sRekpV9-iJE6QeoHqtKX4pfbcBUodJgxxSmF3.ANLWc2.diGeS7d; s_v_web_id=verify_ktxsn1qj_I54FCrES_wtX6_4kZE_AApw_lZAWN4jDZttV; tt_scid=-AYM1AjQQmFOwd99R.7aeNxLWE.zsj3Q5Nu05qrjWOBD0GSVdO0A3UquMcrSlf8lc79d',
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
