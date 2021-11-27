from flask import Flask, json, render_template, jsonify
from util.newsdb import get_categories, get_news_byCaid, getNewsByCreatedTime

app = Flask(__name__)


# 首页分类展示所有的爬取的新闻的类别
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/categories")
def getCategories():
    categories = get_categories()
    return jsonify(categories)


@app.route("/categories/<categoryId>")
def getNews(categoryId):
    categoryId = '#'+categoryId
    newsList = get_news_byCaid(categoryId)
    newsList = [news.__dict__ for news in newsList]
    print(jsonify(newsList))
    return jsonify({'data': newsList})


@app.route("/news/<createdTime>")
def getNewsByTimestp(createdTime):
    newsList = getNewsByCreatedTime(createdTime)
    newsList = [news.__dict__ for news in newsList]
    print(jsonify(newsList))
    return jsonify({'data': newsList})


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
