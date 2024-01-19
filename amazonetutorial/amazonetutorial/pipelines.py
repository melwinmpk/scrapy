# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class AmazonetutorialPipeline:
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
        # self.curr.execute('''
        #                     truncate amazone_tb
        #                     ''')
        self.curr.execute('''
                            CREATE TABLE IF NOT EXISTS amazone_tb(
                                    name text
                                    ,author text
                                    ,price text
                                    ,imagelink text
                            )
                            ''')
        self.conn.commit()
        
    def store_db(self, item):
        SQL_query = f'''
                            INSERT INTO  amazone_tb VALUES (
                                "{(item['product_name'][0])}",
                                "{((''.join(item['product_author'])).split('by')[1]).split('|')[0]}",
                                "{(item['product_price'][0])}",
                                "{(item['product_imagelink'][0])}"
                                )   
                        '''
        #print(SQL_query)
        self.curr.execute(SQL_query)
        self.conn.commit()
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item