class Comment:

    # 评论Comment的构造方法
    def __init__(self, news_id, article_url, comment_str, comment_url):
        self.news_id = news_id
        self.article_url = article_url
        self.comment_str = comment_str
        self.comment_url = comment_url
        self.sentiment = None
        self.positive = None
        self.confidence = None
