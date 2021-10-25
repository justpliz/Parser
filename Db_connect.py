import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='parser',
                                         user='root',
                                         password='MYSQL')

    cursor = connection.cursor()
    cursor.execute("SELECT RESOURCE_URL FROM resource")
    original_url = cursor.fetchall()[0]
    original_str_url = ''.join(map(str, original_url))
    #connection.close()


    mySql_create_table_query = """CREATE TABLE resource (
                                 RESOURCE_ID bigint(20) NOT NULL AUTO_INCREMENT,
                                 RESOURCE_NAME varchar(255) NULL,
                                 RESOURCE_URL varchar(255) NULL,
                                 top_tag varchar(255) NOT NULL,
                                 bottom_tag varchar(255) NOT NULL,
                                 title_tag varchar(255) NOT NULL,
                                 date_cut varchar(255) NOT NULL,
                                 PRIMARY KEY (RESOURCE_ID)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_create_table_query)
    print("resource Table created successfully")


    mySql_create_table_query = """CREATE TABLE items ( 
                                 id int(11) NOT NULL AUTO_INCREMENT,
                                 res_id int(11) NOT NULL,
                                 link varchar(255) NOT NULL,
                                 title text NOT NULL,
                                 content text NOT NULL,
                                 nd_date int(11) NOT NULL,
                                 s_date int(11) NOT NULL,
                                 not_date date NOT NULL,              
                                 PRIMARY KEY (id)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_create_table_query)
    print("items Table created successfully")

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")



def insert_item(res_id, link, title, content, nd_date, s_date, not_date):
    try:
        connection = mysql.connector.connect(host='localhost', #connect
                                             database='parser',
                                             user='root',
                                             password='MYSQL')
        cursor = connection.cursor()
        mySql_insert_items_query = """INSERT INTO Items (res_id, link, title, content, nd_date, s_date, not_date)
                               VALUES
                               (%s, %s, %s, %s, %s, %s, %s) """
        record = (res_id, link, title, content, nd_date, s_date, not_date)
        cursor.execute(mySql_insert_items_query, record)
        connection.commit()
        print("Record inserted successfully into Items table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")