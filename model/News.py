__metaclass__ = type


# 封装每个新闻实体
class News:

    # 构造方法
    def __init__(self, news_id, created, title, tag, abstract, article_url, behot_time,
                 publish_time, comment_count, like_count, read_count, source,
                 keywordStr):
        self.news_id = news_id
        self.created = created
        self.title = title
        self.tag = tag
        self.article_body = None,
        self.abstract = abstract
        self.article_url = article_url
        self.behot_time = behot_time
        self.publish_time = publish_time
        self.comment_count = comment_count
        self.like_count = like_count
        self.read_count = read_count
        self.source = source
        self.keywordStr = keywordStr
        self.keywordsToList()

    def keywordsToList(self):
        self.keywordList = self.keywordStr.split(',')
        self.keywordList = [x.strip()
                            for x in self.keywordList if x.strip() != '']
