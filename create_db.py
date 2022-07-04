import pymysql.cursors
from config import HOST, PORT, USER, PASSWORD, DB_NAME

user_scheme = "CREATE TABLE `users`(" \
              "username text," \
              "user_id BIGINT NOT NULL PRIMARY KEY, " \
              "already_send bool NOT NULL" \
              ");"

project_scheme = "CREATE TABLE `project`(" \
                 "project_name text, " \
                 "creator_id BIGINT NOT NULL PRIMARY KEY," \
                 "chat_link text, " \
                 "support_link text," \
                 "info_channel_link text, " \
                 "total_users BIGINT, pending_users BIGINT, " \
                 "declined_users BIGINT, accepted_users BIGINT" \
                 ");"


def connect(db_name=None):
    try:
        connection_ = pymysql.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        print("Connection Successful")
        return connection_
    except Exception as err:
        print("Connection was failed")
        print(err)


connection = connect()
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE {DB_NAME}")
cursor.close()

connection = connect(DB_NAME)
cursor = connection.cursor()

cursor.execute(user_scheme)
cursor.execute(project_scheme)

cursor.close()
