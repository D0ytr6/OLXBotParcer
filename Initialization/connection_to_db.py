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

def create_tracking(message, now):
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO telegram_base_users_tracking_info (track_text, request_time, 'isTracking', telegram_id_id) VALUES (%s, %s, %s, (Select id from telegram_base_users_data where telegram_id = %s)))",
        (message.from_user.id, message.from_user.username, message.text, now.strftime("%d-%m-%Y %H:%M")))
    connection.commit()