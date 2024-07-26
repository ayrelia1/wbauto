import pandas
import pymysql
import json

bot_config_path = 'config_bot.json'


with open(bot_config_path, 'r+') as file:
    file_config = json.load(file)


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


stop_words = """Нюанс, минус, минусов, минус, начало капать, капает, протекает, потек, сломался, перестал работать, не работает; сгорел, перестал заряжаться, перестала заряжаться, не тот товар, накипь, не включился, не включается, плохое качество, низкое качество, неприятный привкус, свяжитесь, вмятина, царапина, дефект, заводской брак, брак, скол, не справляется, потекла, белый налет, налет, разводы, громко, громкий, шум, гул, производство Китай откуда Корея, Китай, китайская копия, китайская подделка, заедает, заклинило, заклинил, заклинила,  расстроило, расстроилась, расстроился, сломанный, сломан, дефект, с большим трудом, несоответствие, хлипкая, хлипковатой, хлипкий, хлипковат, хлипко, еле держится, отломилась, отломился, не показывает, не выводит, слабая мощность, мало толку, перестал показывать, подделка, не оригинал, копия, шумит, шумно, быстро садится, разрядился, разряжается, привкус, осадок, не стоит своих денег, не полный комплект, неэффективно, пришлось, приходится, не увлажняет, не повышает, не меняется, не тянет, не корректно, раскрутилось, ?, сойдёт, проблема, проблемы, сочится, шумноват, не понимаю, не написано, не удобно, неудобно, долгая доставка, не получается, шумновато, поцарапанный,  неприятный вкус, продавец отказал, крупный недостаток, сложности, недостаток, не комплект, некомплект, пожелание, не положили, тонковат, воняет, вонь, претензия, дорогой, дороговато, не разобралась, не разобрался, неоригинальная, не оригинальная, бесполезен, бесполезный, дешевенький, дешевый, в комплектиции нет, дешевле, железные нервы, нервы, ужасное отношение, ужас, болото, гарантийный талон, гарантийного талона, ожидала большего, слабый, слабая, слабо, не хватает в комплекте, талон не заполнен, гарантийный талон не заполнен, обидно, нет переходника, не набирает, вода не набирается, не накапливается, непонятная инструкция, не понятная инструкция, разочарована, разочарован, неправильно показывает, не правильно показывает, огорчил, огорчила, огорчилась, огорчились, огорчение, перестал работать, перестал работать, некорректно, песок, не запускает, не запускается, проблематично, ерунда, бред, гудит, не стоит таких денег, не стоит своих денег, слабоват, трещина, треснут, разлом
"""

user_id = '5301155177'

def insert_text():
    print('go')
    # Замените 'file.xlsx' на путь к вашему Excel-файлу
    file_path = '4-5 текст + стоп слова .xlsx'

    # Загрузка Excel-файла в объект DataFrame
    df = pandas.read_excel(file_path)

    # Цикл по строкам DataFrame
    for index, row in df.iterrows():
        try:
            # Получение данных из каждого столбца
            article = row['Артикул ']
            star = row['Оценка']
            text = row['Текст ответа']
            text_in_rew = row['Наличие текста в отзыве - ДА/НЕТ']

            # Ваш код обработки данных
            
            # Пример вывода данных
            connection = connect()
            with connection.cursor() as cursor:
                
                
                
                sql = ("INSERT INTO templates (articul, template, star, have_text, user_id) VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(sql, (article, text, star, text_in_rew, user_id,))
                connection.commit()
            connection.close()
        except Exception as e:
            print(e)
        
def insert_text2():
    print('go')
    # Замените 'file.xlsx' на путь к вашему Excel-файлу
    file_path = '4-5 текст + стоп слова .xlsx'

    # Загрузка Excel-файла в объект DataFrame
    df = pandas.read_excel(file_path)

    # Цикл по строкам DataFrame
    for index, row in df.iterrows():
        try:
            # Получение данных из каждого столбца
            article = row['Артикул ']
            star = row['Оценка']
            text = row['Стоп-слова']
            text_in_rew = row['Наличие текста в отзыве - ДА/НЕТ']

            # Ваш код обработки данных
            
            # Пример вывода данных
            connection = connect()
            with connection.cursor() as cursor:
                sql1 = ("SELECT * FROM `templates` WHERE star = %s and have_text = %s and articul = %s")
                cursor.execute(sql1, (star, text_in_rew, article,))
                result = cursor.fetchall()
                for i in result:
                    sql = ("UPDATE `templates` SET stop_words = %s WHERE id = %s")
                    cursor.execute(sql, (text, i['id'],))
                    connection.commit()
            connection.close()
        except Exception as e:
            print(e)
        
def insert_text3():

# Цикл по строкам DataFrame
    try:

        # Ваш код обработки данных
        
        # Пример вывода данных
        connection = connect()
        with connection.cursor() as cursor:
            have_text = 'да'
            sql1 = ("SELECT * FROM templates WHERE have_text = %s and stop_words IS NULL")
            cursor.execute(sql1, (have_text,))
            result = cursor.fetchall()
            for i in result:
                print(i)
                sql = ("UPDATE `templates` SET stop_words = %s WHERE id = %s")
                cursor.execute(sql, (stop_words, i['id'],))
                connection.commit()
        connection.close()
    except Exception as e:
        print(e)
    
        
if __name__ == '__main__':
    insert_text2()