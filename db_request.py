from mysql.connector import MySQLConnection, Error
from db_config import read_db_config
import datetime

def sql_request (query):
    """
    input: query - запрос
    output: result - возвращеает информацию по запросу с ключем по названию поля в таблице
    """
    result=[]
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        # query = conn.escape(query)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
    except Error as e:
        print('Error:', e)
        #обработчик ошибок к примеру выслать на email ошибку
        return result
    finally:
        cursor.close()
        conn.close()

def insert_recent (data_array):
    """
    input - массив данных кликнутой ссылки
    Перед началом вставки чистим таблицу
    """
    query = "INSERT INTO recent_search(film,artist,song,movieurl,imgurl,datetime,locale) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, data_array)
        conn.commit()
        # print('resent_insert')
    except Error as e:
        print('Error:', e)
    finally:
        cursor.close()
        conn.close()


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
        print('delete artists table')
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



