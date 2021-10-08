__metaclass__ = type


# this is a class for every single entity
class News:

    # Constructor there it is
    def __init__(self, title, tag, abstract, article_url, behot_time,
                 publish_time, comment_count, like_count, read_count, source,
                 keywordStr):
        self.title = title
        self.tag = tag
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
        self.keywordList.remove('')

    def greeting(self):
        print(
            f'the title is: \n {self.title} \nthe abstract is \n {self.abstract}\n'
            +
            f'the article_url is \n {self.article_url} \nthe behot_time is \n {self.behot_time} \n'
            +
            f'the publish_time is: \n {self.publish_time} \nthe comment_count is \n {self.comment_count} \n'
            +
            f'the read_count is: \n {self.read_count} \nthe source is \n {self.source} \n'
        )
