import mysql.connector
def get_connection1():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="website"
    )

# mycursor.execute("CREATE DATABASE website")
# mycursor.execute("CREATE TABLE data (id int AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255), email VARCHAR(255),password VARCHAR(255))")
