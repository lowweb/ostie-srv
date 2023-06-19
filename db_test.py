from mysql.connector import MySQLConnection, Error
from db_config import read_db_config
import datetime

def insert_music(data_array):
    """
    input - множество групп/исполнителей
    Перед началом вставки чистим таблицу
    """
    query = "INSERT INTO artists(id,nconst,fullname,proffesion,titles) VALUES(%s,%s,%s,%s,%s)"
    del_query = "DELETE FROM artists"
    update_query = "insert into update_info (actionname,datetime) values (%s, %s)"

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(del_query)
        conn.commit()
        print('delete music')
        for row in data_array:
            cursor.execute(query, row)
            conn.commit()
        print('music inserted')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(update_query, ['update artists', now])
        conn.commit()
        print('update artists table')
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

print('hello')
insert_music([])



