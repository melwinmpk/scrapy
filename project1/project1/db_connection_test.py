import mysql.connector

def connect_test():
    conn = mysql.connector.connect(
                        database='scrapylearning'
                        ,user='root'
                        ,password='welcome123'
                        ,host='127.0.0.1' #127.0.0.1
                        #,auth_plugin='mysql_native_password'
                        #port='3306'
                    )
    curr = conn.cursor()

connect_test() 