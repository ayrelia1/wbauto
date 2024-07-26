import requests
import json
import datetime
import random
from config import bot, Message, CHAT_ID_OZON_SUCCESS, CHAT_ID_OZON_ERROR, CHAT_ID_OZON_SUCCESS_4_5, CHAT_ID_OZON_ERROR_4_5, CHAT_ID_OZON_SUCCESS_1_2_3, CHAT_ID_OZON_ERROR_1_2_3, logging
import time
import threading
from bs4 import BeautifulSoup
import json
import re
import traceback
from markup import *
from seleniumrequests import Chrome
import os
import asyncio
from apiozon.driver_selenium import get_user_browser
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Устанавливаем учетные данные для доступа к Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_table.json', scope)
client = gspread.authorize(creds)

sheet_1_2_3_success = client.open('1-2-3 Ответ')# открываем таблицу
worksheet_1_2_3_success = sheet_1_2_3_success.sheet1 # открываем таблицу

sheet_4_5_success = client.open('4-5 Ответ')# открываем таблицу
worksheet_4_5_success = sheet_4_5_success.sheet1 # открываем таблицу

sheet_all_success = client.open('Все ответы')# открываем таблицу
worksheet_all_success = sheet_all_success.sheet1 # открываем таблицу

sheet_4_5_error = client.open('Неотвеченные 4-5')# открываем таблицу
worksheet_4_5_error = sheet_4_5_error.sheet1 # открываем таблицу

sheet_1_2_3_error = client.open('Неотвеченные 1-2-3')# открываем таблицу
worksheet_1_2_3_error = sheet_1_2_3_error.sheet1 # открываем таблицу




    
class ozon_api:  
    async def cabinets() -> None:
            # sheet_1_2_3_success = client.open('1-2-3 Ответ')# открываем таблицу
            # worksheet_1_2_3_success = sheet_1_2_3_success.sheet1 # открываем таблицу

            # sheet_4_5_success = client.open('4-5 Ответ')# открываем таблицу
            # worksheet_4_5_success = sheet_4_5_success.sheet1 # открываем таблицу

            # sheet_all_success = client.open('Все ответы')# открываем таблицу
            # worksheet_all_success = sheet_all_success.sheet1 # открываем таблицу

            # sheet_4_5_error = client.open('Неотвеченные 4-5')# открываем таблицу
            # worksheet_4_5_error = sheet_4_5_error.sheet1 # открываем таблицу

            # sheet_1_2_3_error = client.open('Неотвеченные 1-2-3')# открываем таблицу
            # worksheet_1_2_3_error = sheet_1_2_3_error.sheet1 # открываем таблицу
            
            # sheets = {
            #     "worksheet_4_5_success": worksheet_4_5_success,
            #     "worksheet_1_2_3_success": worksheet_1_2_3_success,
            #     "worksheet_all_success": worksheet_all_success,
            #     "worksheet_4_5_error": worksheet_4_5_error,
            #     "worksheet_1_2_3_error": worksheet_4_5_success
            # }
        
            cabinets = databasework.get_cabinets()
            
            for i in cabinets:
                profile_name = i['profile_name']
                company_id = i['company_id']
                user_id = i['user_id']
                driver = get_user_browser(profile_name)
                print(profile_name, company_id)
                reviews = await ozon_api.get_reviews(driver, profile_name, company_id)
               
                await ozon_api.check_review(driver, reviews, company_id, profile_name, user_id)
                #await ozon_api.questions(driver, company_id)
                driver.quit()
                
                
    async def get_reviews(driver: Chrome, profile_name: str, company_id: int) -> dict:
        result = []
        driver.get('https://seller.ozon.ru/app/dashboard/main')
        await asyncio.sleep(3)
        pagination_last_timestamp = None
        pagination_last_uuid = None
        for _ in range(2):

            data = {
                "with_counters": False,
                "sort": {
                    "sort_by": "PUBLISHED_AT",
                    "sort_direction": "DESC"
                },
                "company_type": "seller",
                "filter": {
                    "interaction_status": [
                    "NOT_VIEWED"
                    ]
                },
                "company_id": company_id,
                "pagination_last_timestamp": pagination_last_timestamp,
                "pagination_last_uuid": pagination_last_uuid
                }
            data = json.dumps(data)
            response = driver.execute_script(
                f'''
                var xhr = new XMLHttpRequest();
                var params = {data};
                var url = "https://seller.ozon.ru/api/v3/review/list";
                xhr.open('POST', url, false);
                xhr.send(JSON.stringify(params));
                return xhr.responseText;
            ''')
            
            response = json.loads(response)
            pagination_last_timestamp = response['pagination_last_timestamp']
            pagination_last_uuid = response['pagination_last_uuid']

            result.extend(response['result'])
        print(result)
        return result
            
    async def check_review(driver: Chrome, reviews: dict, company_id: int, profile_name: str, user_id: int):
       
        for i in reviews:
            
            try:
                id_review = i['uuid']
                check_review = await databasework.check_review_db(id_review)
                if check_review == 'new':
                    await ozon_api.get_answer_review(driver, i, company_id, profile_name, user_id)
                else:
                    continue
            except Exception as ex:
                logging.error(F'CHECK or ANSWER ERROR - {ex}')
                
                continue
        

    async def get_answer_review(driver: Chrome, review: dict, company_id: int, profile_name: str, user_id: int):
        review_text_positive = review['text']['positive']
        review_text_negative = review['text']['negative']
        review_text_comment = review['text']['comment']
        review_aricul = review['product']['offer_id']
        review_star = review['rating']
        review_supplier = review['product']['brand_info']['name']
        review_user_name = review['author_name']
        review_uuid = review['uuid']
        
        text_for_answer = ''
        
        if review_text_positive or review_text_negative or review_text_comment:
            have_text = 'да'
            if int(review_star) < 4: # проверяем, если 1-2-3 с текстом
                await ozon_api.send_review(text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star, status='Ошибка')
                return
        else:
            have_text = 'нет'
        template = await databasework.check_name_articul_db_user(review_aricul, have_text, user_id, review_star) #  берем шаблон
        
        if len(template) == 0: # если не найден 
            await ozon_api.send_review(text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star, status='Ошибка')
            return
        template = random.choice(template) # берем рандомный

        if have_text == 'да': # проверка стоп-слов
            stop_words: str = template['stop_words']
            
            stop_words = stop_words.split(', ')

            for i in stop_words:
                if i != '':
                    pattern = r'\b' + re.escape(i.lower()) + r'\b'  # Создаем регулярное выражение для поиска целого слова
                    if re.search(pattern, review_text_positive.lower()) or re.search(pattern, review_text_negative.lower()) or re.search(pattern, review_text_comment.lower()):
                        await ozon_api.send_review(text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star, status='Ошибка')
                        print(f'стоп-слово - {i}')
                        return  # стоп слово, отправляем в отдельный чат
                else:
                    continue
        else: 
            pass
                
        # offer = check_['offer']
        # offer = eval(offer)
        # randoms_offer = random.randint(0, len(offer)-1)
        # offer_answer = f'https://ozon.ru/product/{offer[randoms_offer]}'
        
        
        # text_template = check_['template']
        # text_template = eval(text_template)
        # for i in text_template:
        #     splited = i.split(":")
        #     if splited[0] == str(review_star): 
        #         splited_text_template = splited[1]
        #         break
        # text_template_answer = await ozon_api.generate_text(splited_text_template)
        
        text_template_answer: str = template['template']
        
        text_for_answer = text_template_answer.format(name=review_user_name, brand=review_supplier) # offer=offer_answer
        await ozon_api.answer_review(driver, text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star)

    async def answer_review(driver: Chrome, text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star):
        data = {
            "company_id": company_id,
            "company_type": "seller",
            "review_uuid": review_uuid,
            "text": text_for_answer
            }  
        data = json.dumps(data)
        
        response = driver.execute_script(
            f'''
            var xhr = new XMLHttpRequest();
            var params = {data};
            var url = "https://seller.ozon.ru/api/review/comment/create";
            xhr.open('POST', url, false);
            xhr.send(JSON.stringify(params));
            return xhr.responseText;
        ''')
        
        response = json.loads(response)
        if response['result'] == True:
            print(f'Успех!\n{review_aricul}\n{review_uuid}\n{text_for_answer}')

            
            await ozon_api.send_review(text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star, status='Отправлен')
        else:
            print('error request')
            return
        
    async def send_review(text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, profile_name, review_supplier, review_user_name, company_id, review_star, status): 
        
        try:
            
            now_time = datetime.datetime.now()
            now_time = str(now_time)
            if status == 'Отправлен':
                text=f'Бот ответил на отзыв!\n\nОценка - <b>{review_star}</b>\nАртикул - <b><code>{review_aricul}</code></b>\nБренд - <b>{review_supplier}</b>\nДостоинста - <b>{review_text_positive}</b>\nНедостатки - <b>{review_text_negative}</b>\nКомментарий- <b>{review_text_comment}</b>\n\nОтвет - <b>{text_for_answer}</b>'
                data_google_table = [review_uuid, review_text_positive, review_text_negative, review_text_comment, text_for_answer, now_time, review_star, review_supplier, review_aricul] # данные для гугл таблицы отправлено
                worksheet_all_success.append_row(values=data_google_table) # добавляем в гугл таблицу все ответы
                
                if int(review_star) > 3:
                    worksheet_4_5_success.append_row(values=data_google_table) # добавляем в гугл таблицу 4-5 отзывы
                    #await bot.send_message(chat_id=CHAT_ID_OZON_SUCCESS_4_5, text=text, reply_markup=markup, parse_mode='html')
                    await ozon_api.send_msg(CHAT_ID_OZON_SUCCESS_4_5, text, review_aricul)
                    await asyncio.sleep(0.2)
                else:
                    #await bot.send_message(chat_id=CHAT_ID_OZON_SUCCESS_1_2_3, text=text, reply_markup=markup, parse_mode='html')
                    await ozon_api.send_msg(CHAT_ID_OZON_SUCCESS_1_2_3, text, review_aricul)
                    await asyncio.sleep(0.2)
                    worksheet_1_2_3_success.append_row(values=data_google_table) # добавляем в гугл таблицу 4-5 отзывы
                
                
                chat_id = CHAT_ID_OZON_SUCCESS
                
            else:
                text=f'Бот не ответил на отзыв!\n\nОценка - <b>{review_star}</b>\nАртикул - <b><code>{review_aricul}</code></b>\nБренд - <b>{review_supplier}</b>\nДостоинста - <b>{review_text_positive}</b>\nНедостатки - <b>{review_text_negative}</b>\nКомментарий- <b>{review_text_comment}</b>'
                data_google_table = [review_uuid, review_text_positive, review_text_negative, review_text_comment, review_star, now_time, review_supplier, review_aricul, 'НЕТ'] # данные для гугл таблицы не отправлено
                if int(review_star) > 3:
                    #await bot.send_message(chat_id=CHAT_ID_OZON_ERROR_4_5, text=text, reply_markup=markup, parse_mode='html')
                    await ozon_api.send_msg(CHAT_ID_OZON_ERROR_4_5, text, review_aricul)
                    await asyncio.sleep(0.2)
                    worksheet_4_5_error.append_row(values=data_google_table) # добавляем в гугл таблицу НЕ ОТПРАВЛЕННЫЕ
                else:
                    #await bot.send_message(chat_id=CHAT_ID_OZON_ERROR_1_2_3, text=text, reply_markup=markup, parse_mode='html')
                    await ozon_api.send_msg(CHAT_ID_OZON_ERROR_1_2_3, text, review_aricul)
                    await asyncio.sleep(0.2)
                    worksheet_1_2_3_error.append_row(values=data_google_table) # добавляем в гугл таблицу НЕ ОТПРАВЛЕННЫЕ
                
                
                chat_id = CHAT_ID_OZON_ERROR

            
            


            #await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
            await ozon_api.send_msg(chat_id, text, review_aricul)
            await databasework.insert_reviews(text_for_answer, review_uuid, review_text_positive, review_text_negative, review_text_comment, review_aricul, review_supplier, profile_name, review_user_name, company_id, review_star, status)
            await asyncio.sleep(2)
        except Exception as ex:
            print(ex)
        
        
    # async def generate_text(splited_text_template):
    #     splited_text_template2 = splited_text_template.split('|')
    #     randoms_text_template = random.randint(0, len(splited_text_template2)-1)
    #     text_template_answer = splited_text_template2[randoms_text_template]
    #     if text_template_answer == '':
    #         await ozon_api.generate_text(splited_text_template)
    #     else:
    #         return text_template_answer  
            
    async def send_msg(chat_id: int, text: str, review_articul: str):
        markup = question_markup(review_articul)
        try:
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
        except Exception as ex:
            logging.error(f'ERROR SEND MSG - {ex}')
        
            
    async def questions(driver: Chrome, company_id: int):
        driver.get('https://seller.ozon.ru/app/dashboard/main')
        await asyncio.sleep(1)
        data = {
            "sc_company_id": company_id,
            "with_brands": False,
            "with_counters": False,
            "company_type": "brand",
            "filter": {
                "status": "NEW"
            },
            "pagination_last_id": "0"
            }
        data = json.dumps(data)
        response = driver.execute_script(
            f'''
            var xhr = new XMLHttpRequest();
            var params = {data};
            var url = "https://seller.ozon.ru/api/v1/question-list";
            xhr.open('POST', url, false);
            xhr.send(JSON.stringify(params));
            return xhr.responseText;
        ''')
        response = json.loads(response)
        print(response)
        try:
            for i in response['result']:
                print(i)
                if i['answers_total_count'] == 0:
                    await ozon_api.check_question(i)
        except Exception as ex:
            logging.error(F'questions ERROR - {ex}')
        
    async def check_question(question: dict):
        question_id = question['id']
        check_question = await databasework.check_question_db(question_id)
        if check_question == None:
            await ozon_api.send_question(question)
        else:
            return
        
    async def send_question(question: dict):
        question_id = question['id']
        question_text = question['text']
        articul = question['product']['sku']
        product = question['product']['title']
        supplierName = question['brand_info']['name']
        if supplierName == 'LeafToGo':
            chat_id = CHAT_ID_OZON_ERROR
        else:
            chat_id = CHAT_ID_OZON_ERROR
            
        markup = question_markup(articul)
        await bot.send_message(chat_id=chat_id, text=f'Пришел новый вопрос!\n\nНазвание товара - <b>{product}</b>\nАртикул - <b><code>{articul}</code></b>\nКабинет - <b>{supplierName}</b>\n\nВопрос - <b>{question_text}</b>', reply_markup=markup, parse_mode='html')
        await databasework.insert_question(question_id, question_text, supplierName, articul, product)
        await asyncio.sleep(2)
    
    
    
    

