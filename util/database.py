import mysql.connector

# a dic for config
config = {
    'user': 'root',
    'password': 'fork1313',
    'host': '121.43.37.118',
    'database': 'news_scrawler'
    # 'buffered': True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
