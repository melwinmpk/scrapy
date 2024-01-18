# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector



class Project1Pipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()
        
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
                        database="scrapylearning"
                        ,user='root'
                        ,password='welcome123'
                        ,host='127.0.0.1'#127.0.0.1
                        #port='3306'
                    )
        self.conn.autocommit = True
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute('''
                            CREATE TABLE IF NOT EXISTS quotes_tb(
                                title text,
                                author text,
                                tag text
                            )
                            ''')

    def store_db(self, item):
        SQL_query = f'''
                            INSERT INTO  quotes_tb VALUES (
                                "{(item['title'][0].strip('“”')).replace('"','')}",
                                '{item['author'][0]}',
                                '{'|'.join(item['tag'])}'
                                )   
                        '''
        self.curr.execute(SQL_query)
        self.conn.commit()
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item
