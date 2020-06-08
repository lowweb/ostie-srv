from mysql.connector import MySQLConnection, Error
from db_config import read_db_config

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
    query = "INSERT INTO recent_search(film,artist,song,movieurl,imgurl,datetime) VALUES(%s,%s,%s,%s,%s,%s)"
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
    del_query = "DELETE FROM music"
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(del_query)
        conn.commit()
        print('delete music')
        for row in data_array:
            # print(row)
            cursor.execute(query, row)
            conn.commit()
        # cursor.executemany(query, data_array)
        # conn.commit()
        print('music inserted')
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()



