import mysql.connector

# a dic for config
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'on_hot'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
