from flask import Flask, render_template
from util.newsdb import get_categories, get_news_byCaid

app = Flask(__name__)


# 首页分类展示所有的爬取的新闻的类别
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/category/<categoryId>")
def category(categoryId):
    categories = get_categories()
    newsList = get_news_byCaid(categoryId)
    return render_template('category.html',
                           categories=categories,
                           allnews=newsList)


if __name__ == '__main__':
    app.run(debug=True)
