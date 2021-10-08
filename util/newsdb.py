from util.database import db, cursor
from model.News import News


# insert a newsList
def add_news(NewsList):
    try:
        # the sql statement for insert
        sql = ("INSERT INTO news(title,tag,abstract,article_url,"
               "behot_time,publish_time,comment_count,"
               "like_count,read_count,source,keyword_str"
               ")"
               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        for news in NewsList:
            cursor.execute(
                sql, (news.title, news.tag, news.abstract, news.article_url,
                      news.behot_time, news.publish_time, news.comment_count,
                      news.like_count, news.read_count, news.source,
                      news.keywordStr))
            db.commit()
            id = cursor.lastrowid
            print(f'just added the news {id}')
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


# get the news with a specific categoryid
def get_news_byCaid(categoryId):
    try:
        # the sql statement for insert
        sql = "SELECT * FROM news WHERE tag = %s"
        cursor.execute(sql, (categoryId, ))
        nodes = cursor.fetchall()
        # initial the list
        newsList = []
        for i in range(len(nodes)):
            news = News(nodes[i][2], nodes[i][3], nodes[i][4], nodes[i][5],
                        nodes[i][6], nodes[i][7], nodes[i][9], nodes[i][10],
                        nodes[i][11], nodes[i][12], nodes[i][8])
            newsList.append(news)
        print(len(newsList))
        return newsList
    except Exception as e:
        print(e)


# refresh auto_increament
def refresh_auto():
    cursor.execute("ALTER TABLE news AUTO_INCREMENT = 1")
