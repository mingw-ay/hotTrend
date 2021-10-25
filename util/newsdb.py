from util.database import db, cursor
from model.News import News


# 插入新闻列表
def add_news(NewsList):
    try:
        # 插入sql语句
        sql = ("INSERT INTO news(news_id,behot_time,publish_time,title,"
               "tag,abstract,article_url,comment_count,"
               "like_count,read_count,source,keyword_str"
               ")"
               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        for news in NewsList:
            cursor.execute(
                sql, (news.news_id, news.behot_time, news.publish_time,  news.title, news.tag, news.abstract,
                      news.article_url, news.comment_count, news.like_count, news.read_count,
                      news.source, news.keywordStr
                      ))
            db.commit()
            print(f'just added the news {news.news_id}')
    except Exception as e:
        print(e)


# 插入评论的方法
def add_comments(commentList):
    try:
        # the sql statement for insert
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


# get all the categories
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
        sql = "SELECT * FROM news WHERE tag = %s"
        cursor.execute(sql, (categoryId,))
        nodes = cursor.fetchall()
        # 初始化列表
        newsList = []
        for i in range(len(nodes)-1):
            news = News(nodes[i][0], nodes[i][3], nodes[i][4], nodes[i][5],
                        nodes[i][6], nodes[i][1], nodes[i][2], nodes[i][8],
                        nodes[i][9], nodes[i][10], nodes[i][11], nodes[i][7])
            newsList.append(news)
        return newsList
    except Exception as e:
        print(e)


# refresh auto_increament
def refresh_auto():
    cursor.execute("ALTER TABLE news AUTO_INCREMENT = 1")


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
            news = News(nodes[i][0], nodes[i][3], nodes[i][4], nodes[i][5],
                        nodes[i][6], nodes[i][1], nodes[i][2], nodes[i][8],
                        nodes[i][9], nodes[i][10], nodes[i][11], nodes[i][7])
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
