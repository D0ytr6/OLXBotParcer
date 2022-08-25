import psycopg2

connection = psycopg2.connect(
    database="users",
    user="postgres",
    password="1234",
    host="127.0.0.1",
    port="5432"
)

def create_db_if_none():
    cur = connection.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Users_Data (ID SERIAL PRIMARY KEY, Telegram_ID bigint, Telegram_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Users_Requests (ID SERIAL PRIMARY KEY, Telegram_ID bigint, Telegram_username TEXT"
        ", Request TEXT, Request_time TEXT)")
    connection.commit()
