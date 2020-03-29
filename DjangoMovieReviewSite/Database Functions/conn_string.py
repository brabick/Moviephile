import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    passwd="my@llure32SQL",
    db="movie_review_db",
    autocommit=True
)
cursor = connection.cursor()

