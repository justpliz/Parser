import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='parser',
                                         user='root',
                                         password='MYSQL')

    cursor = connection.cursor()
    cursor.execute("SELECT RESOURCE_URL FROM resource")
    originalURL = cursor.fetchall()[0]
    originalStrURL = ''.join(map(str, originalURL))
    #print(originalStrURL)
    #connection.close()


    mySql_Create_Table_Query = """CREATE TABLE resource (
                                 RESOURCE_ID bigint(20) NOT NULL,
                                 RESOURCE_NAME varchar(255) NULL,
                                 RESOURCE_URL varchar(255) NULL,
                                 top_tag varchar(255) NOT NULL,
                                 bottom_tag varchar(255) NOT NULL,
                                 title_tag varchar(255) NOT NULL,
                                 date_cut varchar(255) NOT NULL,
                                 PRIMARY KEY (RESOURCE_ID)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("resource Table created successfully ")


    mySql_Create_Table_Query = """CREATE TABLE items ( 
                                 id int(11) NOT NULL,
                                 res_id int(11) NOT NULL,
                                 link varchar(255) NOT NULL,
                                 title text NOT NULL,
                                 content text NOT NULL,
                                 nd_date int(11) NOT NULL,
                                 s_date int(11) NOT NULL,
                                 not_date date NOT NULL,              
                                 PRIMARY KEY (id)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("items Table created successfully ")

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")



def insert_varibles_into_table(id, res_id, link, title, content, nd_date, s_date, not_date):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='parser',
                                             user='root',
                                             password='MYSQL')
        cursor = connection.cursor()
        MySql_Insert_Items_Query = """INSERT INTO Items (id, res_id, link, title, content, nd_date, s_date, not_date)
                               VALUES
                               (%s, %s, %s, %s, %s, %s, %s, %s) """
        record = (id, res_id, link, title, content, nd_date, s_date, not_date)
        cursor.execute(MySql_Insert_Items_Query, record)
        connection.commit()
        print("Record inserted successfully into Laptop table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")