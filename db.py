from MySQLdb import connect, cursors, Error
import pprint
import MySQLdb
from contextlib import closing

MYSQLCONF = {
    'host': 'localhost', # хост базы данных
    'user': '*', # имя пользователя базы данных
    'password': '*', # пароль пользователя базы данных
    'db': '*', # имя базы данных
    'charset': 'utf8', # используемая кодировка базы данных
    'autocommit': True, # автоматический cursor.commit()
    # извлекаемые строки из БД принимают вид словаря
    'cursorclass': cursors.DictCursor
}

def write_change_price(product_id, old_price, new_price):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO `all_changes_price` (`id`, `product_id`, `old_price`, `new_price`, `date`) VALUES (NULL, '{product_id}', '{old_price}', '{new_price}', CURRENT_TIMESTAMP)")
    db.close()


def output_product_change(product_id):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM `all_changes_price` WHERE `product_id` = {product_id}')
    result = cursor.fetchall()
    return result





