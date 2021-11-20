import requests
from model.Comment import Comment

# 本文件主要包括爬取某一页面的评论
# 需要使用的参数
headers = {
    'cookie':
    '__ac_nonce=06198fb5d0028f235645b; __ac_signature=_02B4Z6wo00f016fH6PAAAIDDJ8USseWiey-n5-xAAIhxd8; ttcid=1f91d8a58d7943f9bfdba13e533e34af36; csrftoken=0c80651dc788b91a0f1d33c8b4273ca2; MONITOR_WEB_ID=7032647174854051365; tt_scid=9kik67w.Tn17PlxIaK.XpcoKabB7sUBY.S8-c3UQMdD.Yai6NViXD8kdvac0u3ch3aa1; s_v_web_id=verify_ab0c212b68bbf3b2e75730bcf1015df3; MONITOR_DEVICE_ID=fd0f515d-6c88-4a28-a63b-ffe60b5fc94b; _tea_utm_cache_2018=undefined',
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
