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
        sql = ('select max(news_id) from tt_news')
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)


# 得到当前评论数量
def get_commentNum():
    try:
        # sql语句
        sql = ('select max(comment_id) from comment')
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result[0][0]
    except Exception as e:
        print(e)


# 插入新闻列表,同时插入热值
def add_news(NewsList):
    dup_count = 0
    dup_kw = []
    # 插入sql语句
    sql0 = ("INSERT INTO tt_news(news_id,created,behot_time,publish_time,title,"
            "tag,abstract,article_url,source,keyword_str,cmt_count,like_count,read_count"
            ")"
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # 得到当前评论最大id
    newsNum = get_newsNum()
    if(newsNum == None):
        newsNum = 1
    else:
        newsNum += 1
    for news in NewsList:
        try:
            # 插入news表
            cursor.execute(
                sql0, (newsNum, news.created, news.behot_time, news.publish_time, news.title,
                       news.tag, news.abstract, news.article_url, news.source, news.keywordStr,
                       news.comment_count, news.like_count, news.read_count
                       ))
            db.commit()
            newsNum += 1
            print(f'成功加入新闻{newsNum}号')
        except Exception as e:
            dup_count += 1
            dup_kw.append(news.keywordStr)
    dup_kw = '\n'.join(dup_kw)
    print(f'又有{dup_count}个重复新闻，其关键词分别是:\n{dup_kw}')


# 插入评论的方法
def add_comments(commentList):
    dup_count = 0
    # 插入列表sql语句
    sql = ("INSERT INTO comment(comment_id,article_url,comment_str,comment_url,sentiment)"
           "VALUES(%s,%s,%s,%s,%s)")
    # 得到当前评论最大id
    commentNum = get_commentNum()
    if(commentNum == None):
        commentNum = 1
    else:
        commentNum += 1
    for comment in commentList:
        try:
            cursor.execute(
                sql, (commentNum, comment.article_url, comment.comment_str, comment.comment_url, comment.sentiment))
            db.commit()
            commentNum += 1
            print(f'成功加入评论{commentNum}号')
        except Exception as e:
            dup_count += 1
    print(f'共{len(commentList)}条评论，其中{dup_count}个重复')


# 获得所有分类
def get_categories():
    try:
        # the sql statement for insert
        sql = "SELECT tag FROM tt_news group by tag"
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
        sql = ("SELECT * FROM tt_news WHERE tag = %s order by news_id asc LIMIT 20")
        cursor.execute(sql, (categoryId,))
        nodes = cursor.fetchall()
        # 初始化列表
        newsList = []
        for i in range(len(nodes)-1):
            news = News(nodes[i][0], nodes[i][1], nodes[i][4], nodes[i][5], nodes[i][7],
                        nodes[i][8], nodes[i][2], nodes[i][3], nodes[i][11],
                        nodes[i][12], nodes[i][13], nodes[i][10], nodes[i][9])
            newsList.append(news)
        return newsList
    except Exception as e:
        print(e)


# 获得某个时间戳的所有新闻
def getNewsByCreatedTime(createdTime):
    try:
        # sql语句
        sql = ("SELECT * FROM tt_news WHERE created = %s order by news_id asc LIMIT 20")
        cursor.execute(sql, (createdTime,))
        nodes = cursor.fetchall()
        # 初始化列表
        newsList = []
        for i in range(len(nodes)-1):
            news = News(nodes[i][0], nodes[i][1], nodes[i][4], nodes[i][5], nodes[i][7],
                        nodes[i][8], nodes[i][2], nodes[i][3], nodes[i][11],
                        nodes[i][12], nodes[i][13], nodes[i][10], nodes[i][9])
            newsList.append(news)
        return newsList
    except Exception as e:
        print(e)

# 获得所有未进行分类的新闻


def get_news():
    try:
        # sql语句
        # sql = "SELECT * FROM ttnews WHERE tag is null or TRIM(tag) = '' "
        sql = "SELECT * FROM tt_news WHERE article_body is Null or TRIM(article_body)='' "
        print(sql)
        cursor.execute(sql)
        nodes = cursor.fetchall()
        # 初始化列表
        newsList = []
        for i in range(len(nodes)):
            news = News(nodes[i][0], nodes[i][1], nodes[i][4], nodes[i][5], nodes[i][7],
                        nodes[i][8], nodes[i][2], nodes[i][3], nodes[i][11], nodes[i][12],
                        nodes[i][13], nodes[i][10], nodes[i][9])
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
            comment = Comment(None, nodes[i][1], nodes[i][2], nodes[i][3])
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


# 将爬取的新闻主题插入的方法
def update_news_body(newsList):
    try:
        # the sql statement for insert
        sql = ("UPDATE tt_news "
               "SET article_body = %s"
               "WHERE news_id = %s")
        for news in newsList:
            cursor.execute(
                sql, (news.article_body, news.news_id))
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


# 去重留一方法
def delete_unsatisfied():
    try:
        news = []
        sql = ("DELETE comment "
               "FROM comment, "
               "(SELECT min(comment_id) comment_id, article_url "
               "FROM comment "
               "GROUP BY article_url "
               "HAVING count(*) > 1) t2 "
               "WHERE comment.article_url = t2.article_url AND comment.comment_id > t2.comment_id")
        # sql = 'SELECT * FROM tt_news where char_length(article_body)<100'
        cursor.execute(sql)
        db.commit()
        # nodes = cursor.fetchall()
        # for i in range(len(nodes)):
        #     news.append(str(nodes[i][0])+'\t'+nodes[i][1])
        # with open('./news_id_list.txt', 'w+', encoding='utf8') as f:
        #     f.write('\n'.join(news))

    except Exception as e:
        print(e)


def to_tt_hotvalue():
    try:
        sql = 'SELECT created,article_url,cmt_count,like_count,read_count FROM tt_news'
        sql0 = ("INSERT INTO tt_hotvalue(created,article_url,cmt_count,like_count,read_count)"
                "VALUES(%s,%s,%s,%s,%s)"
                )
        cursor.execute(sql)
        nodes = cursor.fetchall()
        print(type(nodes))
        for node in nodes:
            cursor.execute(sql0, (node[0], node[1], node[2], node[3], node[4]))
            db.commit()
    except Exception as e:
        print(e)
