import pymysql
from config import file_config



def connect():
    connection = pymysql.connect(
        host=file_config['db_host'],
        port=file_config['db_port'],
        user=file_config['db_log'],
        password=file_config['db_pass'],
        database=file_config['db_name'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
