import requests
from model.Comment import Comment
from util.payload import headers

# 本文件主要包括爬取某一页面的评论


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
    try:
        data = requests.get(comment_url).json()['data']
        commentList = []
        comment_len = 0
        for item in data:
            text = item['comment']['text']
            comment_len += len(text)
            if comment_len < 600:
                commentList.append(text)
    except Exception as e:
        print(e)
        commentList = []
    # 返回
    comment = Comment(news_id, url, '    '.join(commentList), comment_url)
    return comment
