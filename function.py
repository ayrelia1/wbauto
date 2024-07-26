from config import types
from db.db import connect
import random
import string
import datetime
import requests
import json
import base64
import pandas as pd
from io import BytesIO

class databasework:
    
    async def create_user(message: types.Message):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM users WHERE tg_id = %s")
            cursor.execute(sql, (message.chat.id,))
            result = cursor.fetchall()
            if len(result) == 0:
                sql = ("INSERT INTO users (tg_id, username, ban, status, subscribe) VALUES (%s, %s, 'no', 'user', 'yes')")
                cursor.execute(sql, (message.chat.id, message.from_user.username,))
                connection.commit()
        connection.close()
        
    async def check_user(id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE tg_id = %s"
            cursor.execute(sql, (id))
            result = cursor.fetchall()
        connection.close()
        return result
                
    async def check_ban(tg_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE tg_id = %s"
            cursor.execute(sql, (tg_id,))
            result = cursor.fetchall()
            check_ban = result[0]['ban'] 
        connection.close()
        return check_ban    

    async def check_admin(message: types.Message):
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE tg_id = %s"
            cursor.execute(sql, (message.from_user.id,))
            result = cursor.fetchall()
            if result:
                check_admin = result[0]['status'] 
            else:
                check_admin='no'
        connection.close()
        return check_admin == 'admin'
    
    def get_cabinets():
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM cabinets"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        return result
    
    def get_cabinets_user_id(user_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM cabinets WHERE user_id = %s"
            cursor.execute(sql, (str(user_id), ))
            result = cursor.fetchall()
        connection.close()
        return result
    
    
    async def check_review_db(id_review):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM reviews WHERE uuid_review = %s")
            cursor.execute(sql, (id_review,))
            result = cursor.fetchone()
        connection.close()
        if result == None:
            return 'new'
        else: return 'old'
    
    
    async def insert_reviews(text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star, status):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("INSERT INTO reviews (uuid_review, client_name, star, cabinet, profile_name, articul, positive_text, negative_text, comment_text, answer, datetime, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (review_uuid, review_user_name, review_star, review_supplier, profile_name, review_aricul, review_text_positive, review_text_negative, review_text_comment, text_for_answer, datetime.date.today(), status,))
            connection.commit()
        connection.close()
                
                
    async def get_reviews_db(start_date, end_date, profile_name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = """SELECT * 
                    FROM reviews 
                    WHERE datetime BETWEEN %s AND %s
                        AND cabinet = %s
                    ORDER BY datetime;"""
            cursor.execute(sql, (start_date, end_date, profile_name,))
            result = cursor.fetchall()
        connection.close()
        return result
            
    
    async def check_phone_db(token):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM cabinets WHERE phone = %s")
            cursor.execute(sql, (token, ))
            result = cursor.fetchone()
        connection.close()
        if result == None:
            return 'new'
        else: return 'old'
        
    def check_code_db(id_session):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM temp_register WHERE id_session = %s")
            cursor.execute(sql, (id_session,))
            result = cursor.fetchone()
        connection.close()
        return result
    
    def insert_code_db(id_session, code, types):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("INSERT INTO temp_register (id_session, code, type) VALUES (%s, %s, %s)")
            cursor.execute(sql, (id_session, code, types,))
            connection.commit()
        connection.close()
        
    def update_status_register_db(result, id_session):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE temp_register SET result = %s WHERE id_session = %s")
            cursor.execute(sql, (result, id_session,))
            connection.commit()
        connection.close()
        
    async def insert_cabinet_db(profile_name, phone, company_id, user_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("INSERT INTO cabinets (profile_name, phone, company_id, user_id) VALUES (%s, %s, %s, %s)")
            cursor.execute(sql, (profile_name, phone, int(company_id), user_id, ))
            connection.commit()
        connection.close()
        
    async def check_company_id_cabinet_db(company_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM cabinets WHERE company_id = %s")
            cursor.execute(sql, (company_id,))
            result = cursor.fetchone()
        connection.close()
        return result
            

    async def check_name_cabinet_db(name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM cabinets WHERE profile_name = %s")
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        connection.close()
        return result
            
        
    async def delete_cabinet_db(name):
        connection = connect()   
        with connection.cursor() as cursor:
            sql = ("DELETE FROM cabinets WHERE profile_name = %s")
            cursor.execute(sql, (name,))     
            connection.commit()
        connection.close()
    
            
    
    
    async def check_name_template_db(name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM templates WHERE name = %s")
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        connection.close()
        return result
        
    async def delete_template_db(name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("DELETE FROM templates WHERE name = %s")
            cursor.execute(sql, (name,))
            connection.commit()
        connection.close()
        return

    async def delete_template_db_all(name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("DELETE FROM all_templates WHERE name = %s")
            cursor.execute(sql, (name,))
            connection.commit()
        connection.close()
        return
        
        
    async def check_name_template_db_all(name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM all_templates WHERE name = %s")
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        connection.close()
        return result
        
            
    async def check_name_articul_db(articul, have_text):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM templates WHERE articul = %s AND have_text = %s")
            cursor.execute(sql, (articul, have_text,))
            result = cursor.fetchone()
        connection.close()
        return result

            
    async def check_name_articul_db_all(articul, have_text):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM all_templates WHERE articul = %s AND have_text = %s")
            cursor.execute(sql, (articul, have_text,))
            result = cursor.fetchone()
        connection.close()
        return result

    async def check_name_articul_db_user(articul, have_text, user_id, star):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM templates WHERE articul = %s AND have_text = %s AND user_id = %s AND star = %s")
            cursor.execute(sql, (articul, have_text, user_id, star, ))
            result = cursor.fetchall()
        connection.close()
        return result
    
    async def check_name_articul_db_all_user(articul, have_text, user_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM all_templates WHERE articul = %s AND have_text = %s AND user_id = %s")
            cursor.execute(sql, (articul, have_text, user_id, ))
            result = cursor.fetchone()
        connection.close()
        return result
    
            
    async def insert_template(name, articul, texts, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, user_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("INSERT INTO templates (name, articul, template, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (name, articul, texts, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, user_id,))
            connection.commit()
        connection.close()
        
    async def insert_template2(name, articul, texts, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, user_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("INSERT INTO all_templates (name, articul, template, star, stop_words, have_text, offer, template_user, stop_words_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(sql, (name, articul, texts, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, user_id,))
            connection.commit()
        connection.close()
        
    async def update_template_text(texts, template_user_text, name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE templates SET template = %s, template_user = %s WHERE name = %s")
            cursor.execute(sql, (texts, template_user_text, name,))
            connection.commit()
        connection.close()
        
    async def update_template_text_all(texts, template_user_text, name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE all_templates SET template = %s, template_user = %s WHERE name = %s")
            cursor.execute(sql, (texts, template_user_text, name,))
            connection.commit()
        connection.close()
        
        
    async def update_template_stop_words(stop_words, stop_words_user, name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE templates SET stop_words = %s, stop_words_user = %s WHERE name = %s")
            cursor.execute(sql, (stop_words, stop_words_user, name,))
            connection.commit()
        connection.close()
        
    async def update_status(id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE users SET status = 'admin' WHERE tg_id = %s")
            cursor.execute(sql, (id,))
            connection.commit()
        connection.close()
        
    async def update_template_stop_words_all(stop_words, stop_words_user, name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE all_templates SET stop_words = %s, stop_words_user = %s WHERE name = %s")
            cursor.execute(sql, (stop_words, stop_words_user, name,))
            connection.commit()
        connection.close()
        
    async def update_template_articul(articul, name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE templates SET articul = %s WHERE name = %s")
            cursor.execute(sql, (articul, name,))
            connection.commit()
        connection.close()
        
        
    async def update_template_offer(offer, offer_user, name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE templates SET offer = %s, offer_user = %s WHERE name = %s")
            cursor.execute(sql, (offer, offer_user, name,))
            connection.commit()
        connection.close()

    async def update_template_offer_all(offer, offer_user, name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("UPDATE all_templates SET offer = %s, offer_user = %s WHERE name = %s")
            cursor.execute(sql, (offer, offer_user, name,))
            connection.commit()
        connection.close()
    
    
    def get_templates_db():
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM templates"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        return result
    
    def get_templates_db_all():
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM all_templates"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        return result
    
    def get_templates_db_user(user_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM templates WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
        connection.close()
        print(result)
        return result
    
    def get_templates_db_all_user(user_id):
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM all_templates WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
        connection.close()
        return result
    
    
    async def check_articuls_db2(articul):
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM templates WHERE CONCAT(',', articul, ',') LIKE '%,%s,%'"
            cursor.execute(sql, (articul, ))
            result = cursor.fetchone()
        connection.close()
        print(result)
        return result    


    async def insert_duplicate_template_db(name, articul, old_name):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("""INSERT INTO templates (name, articul, template, template_user, star, stop_words, stop_words_user, have_text, offer, offer_user, user_id)
                    SELECT %s, %s, template, template_user, star, stop_words, stop_words_user, have_text, offer, offer_user, user_id
                    FROM templates
                    WHERE name = %s""")
            cursor.execute(sql, (name, articul, old_name,))
            connection.commit()
        connection.close()


    async def check_question_db(id_question):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM questions WHERE id_question = %s ")
            cursor.execute(sql, (id_question,))
            result = cursor.fetchone()
        connection.close()
        return result

    async def insert_question(id_question, text, supplierName, articul, productName):
        connection = connect()
        with connection.cursor() as cursor:
            sql = ("INSERT INTO questions (id_question, text, supplierName, articul, productName, time) VALUES (%s, %s, %s, %s, %s, %s)")
            time = datetime.datetime.now()
            cursor.execute(sql, (id_question, text, supplierName, articul, productName, time,))
            connection.commit()
        connection.close()
        

        
    
    
            
            
async def create_template_func(name, articul, texts, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, user_id):
    stop_words = list(map(str.strip, stop_words))
    texts = list(map(str.strip, texts))
    offer = list(map(str.strip, offer))
    star = list(map(str.strip, star))
    offer = str(offer)
    star = str(star)
    stop_words=str(stop_words)
    texts=str(texts)
    if articul == '*':
        await databasework.insert_template2(name, articul, texts, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, user_id)
    else: 
        await databasework.insert_template(name, articul, texts, star, stop_words,have_text, offer, template_user, stop_words_user, offer_user, user_id)
            
            

    