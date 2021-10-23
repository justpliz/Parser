import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='parser',
                                         user='root',
                                         password='MYSQL')
    # Получаем кортеж ссылок для парсинга, выбираем нужную в формате string
    cursor = connection.cursor()
    cursor.execute("SELECT URL FROM input_URL")
    originalURL = cursor.fetchall()[0]
    originalStrURL = ' '.join(map(str, originalURL))
    #print(originalStrURL)
    #connection.close()

    # Создание таблицы ссылок для парсинга
    mySql_Create_Table_Query = """CREATE TABLE input_URL (
                                 Id int(11) NOT NULL,
                                 URL varchar(250) NOT NULL,
                                 PRIMARY KEY (Id)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("input_URL Table created successfully ")

    # Создание таблицы с выходными данными
    mySql_Create_Table_Query = """CREATE TABLE output_content ( 
                                 Id int(11) NOT NULL,
                                 URL varchar(250) NOT NULL,
                                 Heading varchar(500) NOT NULL,
                                 Data DATE NOT NULL,
                                 Content TEXT NOT NULL,                                               
                                 PRIMARY KEY (Id)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("output_content Table created successfully ")

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

