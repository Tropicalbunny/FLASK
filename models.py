import sqlite3
 
#login database connections
databaseLoginConnection = sqlite3.connect('loginInfo.db')

cursor = databaseLoginConnection.cursor()
cursor.execute(""" 
CREATE TABLE loginInfo ( 
    id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    email TEXT NOT NULL, 
    password TEXT NOT NULL
); 
""") 