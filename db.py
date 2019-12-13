import sqlite3


conn = sqlite3.connect("test.db")
cursor = conn.cursor()

request = "select * from tests"

cursor.execute(request)
data = cursor.fetchall()
print(data)