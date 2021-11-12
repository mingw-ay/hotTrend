from util.database import db, cursor
from model.News import News
from model.Comment import Comment
# from Comment import Comment
# from News import News
# from database import db, cursor


# 获得当前新闻数量
def get_newsNum():
    try:
        # sql语句
        sql = ('select max(news_id) from news')
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)


# 插入新闻列表,同时插入热值
def add_news(NewsList):
    try:
        # 插入sql语句
        sql0 = ("INSERT INTO news(news_id,created,behot_time,publish_time,title,"
                "tag,abstract,article_url,source,keyword_str"
                ")"
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        sql1 = ("INSERT INTO hotvalue(news_id,created,comment_count,like_count,read_count"
                ")"
                "VALUES(%s,%s,%s,%s,%s)")
        for news in NewsList:
            # 插入news表
            cursor.execute(
                sql0, (news.news_id, news.created, news.behot_time, news.publish_time, news.title,
                       news.tag, news.abstract, news.article_url, news.source, news.keywordStr
                       ))
            db.commit()
            # 插入hotvalue表
            cursor.execute(
                sql1, (news.news_id, news.created,
                       news.comment_count, news.like_count, news.read_count))
            db.commit()
            print(f'just added the news {news.news_id}')
    except Exception as e:
        print(e)


# 插入评论的方法
def add_comments(commentList):
    try:
        # 插入列表sql语句
        sql = ("INSERT INTO comment(news_id,comment_str,comment_url,sentiment)"
               "VALUES(%s,%s,%s,%s)")
        for comment in commentList:
            cursor.execute(
                sql, (comment.news_id, comment.comment_str, comment.comment_url, comment.sentiment
                      ))
            db.commit()
            print(f'just added the comment {comment.news_id}')
    except Exception as e:
        print(e)


# 获得所有分类
def get_categories():
    try:
        # the sql statement for insert
        sql = "SELECT tag FROM news group by tag"
        cursor.execute(sql)
        categories = cursor.fetchall()
        for i in range(len(categories)):
            categories[i] = categories[i][0]
        return categories
    except Exception as e:
        print(e)


# 获得某一类的所有新闻
def get_news_byCaid(categoryId):
    try:
        # sql语句
        sql = ("SELECT * FROM news,hotvalue WHERE tag = %s and news.news_id = hotvalue.news_id"
               " and news.created = hotvalue.created")
        cursor.execute(sql, (categoryId,))
        nodes = cursor.fetchall()
        # 初始化列表
        newsList = []
        for i in range(len(nodes)-1):
            news = News(nodes[i][0], nodes[i][1], nodes[i][4], nodes[i][5], nodes[i][6],
                        nodes[i][7], nodes[i][2], nodes[i][3], nodes[i][13],
                        nodes[i][14], nodes[i][15], nodes[i][9], nodes[i][8])
            newsList.append(news)
        return newsList
    except Exception as e:
        print(e)


# 获得所有未进行分类的新闻
def get_news():
    try:
        # sql语句
        sql = "SELECT * FROM news WHERE tag is null or TRIM(tag) = '' "
        cursor.execute(sql)
        nodes = cursor.fetchall()
        # 初始化列表
        newsList = []
        for i in range(len(nodes)):
            news = News(nodes[i][0], nodes[i][1], nodes[i][4], nodes[i][5], nodes[i][6],
                        nodes[i][7], nodes[i][2], nodes[i][3], None, None, None, nodes[i][9], nodes[i][8])
            newsList.append(news)
        return newsList
    except Exception as e:
        print(e)


# 提取关键词以及分类结束后更新列表
def update_news(newsList):
    try:
        # the sql statement for insert
        sql = ("UPDATE news "
               "SET tag = %s, keyword_str = %s "
               "WHERE news_id = %s")
        for news in newsList:
            cursor.execute(
                sql, (news.tag, news.keywordStr, news.news_id))
            db.commit()
    except Exception as e:
        print(e)


# 获得所有未经过情感分析的评论
def get_comments_without():
    try:
        # sql语句
        sql = "SELECT * FROM comment WHERE sentiment is null or TRIM(sentiment) = '' LIMIT 20;"
        cursor.execute(sql)
        nodes = cursor.fetchall()
        # 初始化列表
        commentList = []
        for i in range(len(nodes)):
            comment = Comment(nodes[i][1], nodes[i][2], nodes[i][3])
            commentList.append(comment)
        return commentList
    except Exception as e:
        print(e)


# 将情感分析过后的comment进行更新
def update_comments(commentList):
    try:
        # the sql statement for insert
        sql = ("UPDATE comment "
               "SET sentiment = %s, positive = %s, confidence = %s "
               "WHERE news_id = %s")
        for comment in commentList:
            cursor.execute(
                sql, (comment.sentiment, comment.positive, comment.confidence, comment.news_id))
            db.commit()
    except Exception as e:
        print(e)


# 将情感分析过后的comment进行更新
def database_edits():
    try:
        # the sql statement for insert
        sql = ("SELECT * FROM news")
        cursor.execute(sql)
        nodes = cursor.fetchall()
        # 初始化列表
        hotvalueList = []
        for i in range(len(nodes)):
            hotvalue = {
                'news_id': nodes[i][0],
                'created': nodes[i][1],
                'comment_count': nodes[i][9],
                'like_count': nodes[i][10],
                'read_count': nodes[i][11],
            }
            hotvalueList.append(hotvalue)
        for hotvalue in hotvalueList:
            sql0 = ("INSERT INTO hotvalue(news_id,created,comment_count,like_count,read_count"
                    ")"
                    "VALUES(%s,%s,%s,%s,%s)")
            cursor.execute(
                sql0, (hotvalue['news_id'], hotvalue['created'],
                       hotvalue['comment_count'], hotvalue['like_count'], hotvalue['read_count']))
            db.commit()
    except Exception as e:
        print(e)
