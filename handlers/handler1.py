from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, file_config, json, bot_config_path, FSInputFile, time
from states import add_cabinet_state, add_template_state, edit_time_pars_state, load_reviews_state, duplicate_template_state, edit_template_state, give_admin
from markup import *
import filtersbot
from function import databasework, create_template_func
from datetime import timedelta
import datetime
import filtersbot
import aiocron
import random
from apiozon.api import ozon_api
from apiozon.auth import auth
import asyncio
import threading
import os

router = Router()







@router.message(filtersbot.AdminCheck(), F.text == '/start')
async def start(message: types.Message, state: FSMContext):
    #photo = FSInputFile('kwork8/photo/start_message.jpg')
    await state.clear()
    markup = start_markup()
    #await ozon_api.cabinets()
    await message.answer(f'Добро пожаловать в бота, используйте клавиатуру ниже 👇', reply_markup=markup)
    

# -------------- добавить админа ------------------ #

@router.callback_query(F.data == 'give_admin')
async def give_admin_handler(callback: types.CallbackQuery, state: FSMContext):
    markup = menu()
    await bot.edit_message_text(text='Введите ID пользователя которому нужно дать доступ к боту\n\nID можно узнать здесь - https://t.me/getmyid_bot', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup)
    await state.set_state(give_admin.one)

@router.message(give_admin.one)
async def give_admin_handler2(message: types.Message, state: FSMContext):
    id = message.text
    markup = menu()
    if id.isdigit():
        
        
        try:
            await databasework.update_status(id)
            await message.answer('Успешно, доступ к боту выдан!', reply_markup=markup)
            await state.clear()
        except:
            await message.answer('Ошибка! Проверьте валидность данных', reply_markup=markup)
    else:
        await message.answer('Ошибка! Проверьте валидность данных', reply_markup=markup)

# ------------------------Кабинеты---------------------------- #

@router.callback_query(F.data == 'cabinets')
async def cabinets_get(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    action = 'get_cabinets_edit'
    markup = get_cabinets_markup(action, user_id)
    await bot.edit_message_text(text='Подключенные кабинеты 👇', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup)


@router.callback_query(filtersbot.CallbackDataFilter.filter(F.action.in_(['get_cabinets_edit'])))
async def custom_button(callback: types.CallbackQuery, state: FSMContext):
    call = callback.data.split(':')
    name = call[1]
    cabinet = await databasework.check_name_cabinet_db(name)
    
    markup = get_cabinet_markup(name)
    
    await bot.edit_message_text(text=f"Название кабинета - <b>{cabinet['profile_name']}</b>\n\nНомер телефона - <b><code>{cabinet['phone']}</code></b>\n\nID Компании - {cabinet['company_id']}", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')



# ------------------------Удалить кабинет---------------------------- #



@router.callback_query(filtersbot.CallbackDataFilter.filter(F.action.in_(['delete_cabinet'])))
async def delete_cabinet(callback: types.CallbackQuery, state: FSMContext):
    call = callback.data.split(':')
    name = call[1]
    markup = menu()
    await databasework.delete_cabinet_db(name)
    await bot.edit_message_text(text='Кабинет удален ✔️', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup)

    


# ------------------------Вернуться в меню---------------------------- #

@router.callback_query(F.data == 'main')
async def go_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    #await start(callback.message, state)
    markup = start_markup()
    await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, text='Добро пожаловать в бота, используйте клавиатуру ниже 👇', reply_markup=markup)


@router.callback_query(F.data == 'main2')
async def go_main2(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await start(callback.message, state)

# ------------------------Добавление кабинета---------------------------- #
    
@router.callback_query(F.data == 'add_cabinet')
async def add_cabinet(callback: types.CallbackQuery, state: FSMContext):
    markup = menu()
    #await callback.message.answer('Введите токен 👇', reply_markup=markup)
    await bot.edit_message_text(text='Введите название кабинета 👇', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup)
    await state.set_state(add_cabinet_state.one)
    
    
@router.message(filtersbot.AdminCheck(), add_cabinet_state.one)
async def create_name_cabinet(message: types.Message, state: FSMContext):
    profile_name = message.text
    markup = menu()
    check_name = await databasework.check_name_cabinet_db(profile_name)
    if check_name == None:
        await message.answer('Отлично, введите номер телефона вашего кабинета в формате - 79000000000', reply_markup=markup)
        await state.update_data(profile_name=profile_name)
        await state.set_state(add_cabinet_state.two)
    else: await message.answer('Такое имя уже существует, введите уникальное имя 👇', reply_markup=markup)
    
   

    
@router.message(filtersbot.AdminCheck(), add_cabinet_state.two)
async def insert_token(message: types.Message, state: FSMContext):
    markup = menu()
    phone = message.text
    data = await state.get_data()
    profile_name = data['profile_name']
    if phone.isdigit():
        id_session_phone = random.randint(100000000, 10000000000000)
        id_session_email = random.randint(100000000, 10000000000000)
        #await register_user(profile, phone, id_session_phone, id_session_email)
        #task = asyncio.create_task(register_user(profile, phone, id_session_phone, id_session_email))
        thread = threading.Thread(target=auth.register_user, args=(profile_name, phone, id_session_phone, id_session_email))
        await state.update_data(id_session_phone=id_session_phone, id_session_email=id_session_email, thread=thread, phone=phone)
        thread.daemon = True
        thread.start()
        await message.answer('Отлично, введите код который придет на ваш телефон либо же последние <b>6</b> цифр номера который вам позвонит!\nВведите в течении 100 секунд, иначе сессия прервется! 👇', reply_markup=markup, parse_mode='html')
        await state.set_state(add_cabinet_state.three)
    else: 
        await message.answer('Введите номер телефона в формате - 79000000000', reply_markup=markup)
        

        
@router.message(filtersbot.AdminCheck(), add_cabinet_state.three)
async def insert_token(message: types.Message, state: FSMContext):
    markup = menu()
    code = message.text
    if code.isdigit() and len(code) == 6:
        data = await state.get_data()
        id_session_phone = data['id_session_phone']
        databasework.insert_code_db(id_session_phone, code, types='phone')
        await message.answer('Отлично, введите код который придет на вашу почту состоящий из <b>6</b> цифр!\nВведите в течении 100 секунд, иначе сессия прервется! 👇', reply_markup=markup, parse_mode='html')
        await state.set_state(add_cabinet_state.four)
    else:
        await message.answer('Введите число состоящее из 6 символов!', reply_markup=markup)
        
@router.message(filtersbot.AdminCheck(), add_cabinet_state.four)
async def insert_token(message: types.Message, state: FSMContext):
    markup = menu()
    code = message.text
    if code.isdigit() and len(code) == 6:
        data = await state.get_data()
        id_session_email = data['id_session_email']
        databasework.insert_code_db(id_session_email, code, types='email')
        await message.answer('Отлично, введите ID компании! 👇', reply_markup=markup, parse_mode='html')
        await state.set_state(add_cabinet_state.five)
    else:
        await message.answer('Введите число состоящее из 6 символов!', reply_markup=markup)
        
@router.message(filtersbot.AdminCheck(), add_cabinet_state.five)
async def insert_token(message: types.Message, state: FSMContext):
    markup = menu()
    company_id = message.text
    if company_id.isdigit():
        result = await databasework.check_company_id_cabinet_db(company_id)
        if result == None:
            data = await state.get_data()
            id_session_phone = data['id_session_phone']
            id_session_email = data['id_session_email']
            profile_name = data['profile_name']
            phone = data['phone']
            thread = data['thread']
            thread.join()
            result = databasework.check_code_db(id_session_phone)
            if result['result'] == 'error':
                await message.answer('Во время добавления кабинета произошла ошибка, вы ввели неверный код, попробуйте добавить кабинет еще раз!', reply_markup=markup, parse_mode='html')
                await state.clear()
            else:
                await message.answer('Кабинет успешно добавлен!', reply_markup=markup, parse_mode='html')
                await databasework.insert_cabinet_db(profile_name, phone, company_id, message.from_user.id)
                await state.clear()
        else:
            await message.answer('Кабинет с таким ID уже добавлен!', reply_markup=markup, parse_mode='html')
        
    else:
        await message.answer('Введите число!', reply_markup=markup)        


# ------------------------Добавление шаблона---------------------------- #

# @router.callback_query(F.data == 'add_template')
# async def add_cabinet(callback: types.CallbackQuery, state: FSMContext):
#     markup = text_or_no_markup()
#     #await callback.message.answer('Введите токен 👇', reply_markup=markup)
#     await bot.edit_message_text(text='Выберите для каких отзывов нужен шаблон 👇', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup)


# #@router.message(filtersbot.AdminCheck(), add_template_state.one)
# #async def create_name_template(message: types.Message, state: FSMContext):
# @router.callback_query(F.data.in_(['review_with_text', 'review_no_text']))
# async def text_or_no(callback: types.CallbackQuery, state: FSMContext):
#     markup = menu()
#     if callback.data == 'review_with_text':
#         have_text = 'yes'
#     elif callback.data == 'review_no_text':
#         have_text = 'no'
#     await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, text='Введите название шаблона 👇', reply_markup=markup)
#     await state.set_state(add_template_state.one)
#     await state.update_data(have_text=have_text)

# @router.message(filtersbot.AdminCheck(), add_template_state.one)
# async def create_name_template(message: types.Message, state: FSMContext):
#     name = message.text
#     markup = menu()
#     check_name = await databasework.check_name_template_db(name)
#     check_name2= await databasework.check_name_template_db_all(name)
#     if check_name == None and check_name2 == None:
#         await message.answer('Отлично, введите артикул товара, если введете * то шаблон будет работать для всех товаров, но в первую очередь при обработке отзыва будет искать шаблон на конкрентный артикул, если не найдет - применит общий 👇', reply_markup=markup, parse_mode='html')
#         await state.update_data(name=name)
#         await state.set_state(add_template_state.six)
#     else: await message.answer('Такое имя уже существует, введите уникальное имя 👇', reply_markup=markup)


# @router.message(filtersbot.AdminCheck(), add_template_state.six)
# async def create_articul_template(message: types.Message, state: FSMContext):
#     try:
#         data = await state.get_data()
#         have_text = data['have_text']
        
#         articul = message.text
#         markup = menu()
        
#         if articul.isdigit():
#             check_articul = await databasework.check_name_articul_db(articul, have_text)
#         elif articul == '*':
#             check_articul = await databasework.check_name_articul_db_all(articul, have_text)
#         else:
#             raise ValueError
            
        
#         #check_name = await databasework.check_name_articul_db(articul)
#         if check_articul == None:
#             await message.answer('Отлично, введите артикулы товаров которые можно будет предложить через знак разделителя |\n\nНапример: 12343|345345|345456', reply_markup=markup, parse_mode='html')
#             await state.update_data(articul=articul)
#             await state.set_state(add_template_state.two)
#         else: await message.answer('Такой артикул уже существует, введите уникальный артикул 👇', reply_markup=markup)
#     except:
#         await message.answer('Ошибка! Введите артикул состоящий из цифр либо * 👇', reply_markup=markup)


# @router.message(filtersbot.AdminCheck(), add_template_state.two)
# async def create_offer_template(message: types.Message, state: FSMContext):
#     try:
#         markup = menu()
#         offer = message.text
#         offer_user = message.text
        
#         split_offer = offer.split('|')
#         if split_offer:    
#             for i in split_offer:
#                 if i.isdigit():
#                     pass
#                 else:
#                     raise ValueError
#             await message.answer('Отлично, введите оценки на которые будет реагировать шаблон, введите через разделительный знак |\n\nНапример: <b>3|4|5</b>', reply_markup=markup, parse_mode='html')
#             await state.update_data(offer=split_offer, offer_user=offer_user)
#             await state.set_state(add_template_state.three)
#         else: await message.answer('Введите хотя бы что-то!')
#     except:
#         await message.answer('Ошибка! Введите по форме, артикулы могут состоять только из цифр, проверьте нет ли между артикулами пробелов 👇', reply_markup=markup)


# @router.message(filtersbot.AdminCheck(), add_template_state.three)
# async def get_star_template(message: types.Message, state: FSMContext):
#     star = message.text
#     markup = menu()
#     try:
#         star = star.split('|')
#         for i in star:
#             if i.isdigit():
#                 a = int(i)
#                 if a < 1 or a > 5:
#                     raise Exception
#             else:
#                 await message.answer('Каждое значение должно состоять из цифр и не должно содержать в себе других символов(например пробел и т.д)', reply_markup=markup)
#                 raise Warning 
#         data = await state.get_data()
#         have_text = data['have_text']
#         if have_text == 'yes':
#             await message.answer('Отлично, введите стоп-слова через разделитель для каждой вышеуказанной оценки\n\nПример:\n\n<b>3:не понравилось|не покупайте & 4:бесполезно|не очень & 5:сломалось|приехало неисправно</b>\n\nОбратите внимание, необходимо указать стоп-слова на каждую из оценок используя знак двоеточей, после двоеточей отправьте через знак разделитель | стоп-слова, по которым бот будет пропускать отзывы, для разделения оценок используйте знак &, то есть вы хотите создать стоп-слова для оценки 3\n<b><code>3:стопслово1|стопслово2</code></b>\nДля того чтобы добавить еще одну оценку, используйте знак &, то есть\n<b><code>3:стопслово1|стопслово2 & 4:стопслово3|стопслово4</code></b>\nНеобходимо указать стоп-слова для каждой оценки которую вы указали выше!', reply_markup=markup, parse_mode='html')
#             await state.update_data(star=star)
#             await state.set_state(add_template_state.four)
#         else:
#             await message.answer('Отлично, введите вариации текста через разделитель для каждой вышеуказанной оценки\n\nПример:\n<b>3:текст1|текст2 & 4:текст1|текст2 & 5:текст1|текст2</b>\n\nУказывать вариации текста нужно таким-же образом как и стоп-слова, ими бот будет отвечать на отзывы\n\nТакже в тексе вы можете использовать следующие параметры:\n\n<code>{name}</code> - Имя покупателя\n<code>{brand}</code> - Название вашего бренда\n<code>{offer}</code> - товар который нужно предложить\n\nТаким образом вы сможете сделать следующий текст:\n<b><code>5:{name} спасибо за покупку! {brand} работает для вас! Возможно вам будет интересен этот товар {offer}|Спасибо за покупку {name}! Наш бренд {brand} работает для вас! Возможно вам будет интересен этот товар {offer}</code></b>', reply_markup=markup, parse_mode='html')
#             await state.update_data(star=star, stop_words='', stop_words_user='')
#             await state.set_state(add_template_state.five)
                
            
#     except ValueError:
#         await message.answer('Произошла ошибка, возможно вы ввели текст неправильно, диапазон цифр от 1 до 5, попробуйте еще раз.', reply_markup=markup)
#     except Exception as ex: print(ex)
    
    
# @router.message(filtersbot.AdminCheck(), add_template_state.four)
# async def get_stop_words_template(message: types.Message, state: FSMContext):
#     stop_words = message.text
#     stop_words_user = message.text
#     markup = menu()
#     try:
#         stop_words = stop_words.split('&')
#         data = await state.get_data()
#         star = data['star']
#         star.sort()
#         check_ = []
#         for i in stop_words:
#             a = i.split(':')
#             b = a[0].strip()
#             check_.append(b)
#             b = int(b)
#         check_.sort()
        
#         if check_ == star:
#             pass
#         else: raise ValueError
        
#         await message.answer('Отлично, введите вариации текста через разделитель для каждой вышеуказанной оценки\n\nПример:\n<b>3:текст1|текст2 & 4:текст1|текст2 & 5:текст1|текст2</b>\n\nУказывать вариации текста нужно таким-же образом как и стоп-слова, ими бот будет отвечать на отзывы\n\nТакже в тексе вы можете использовать следующие параметры:\n\n<code>{name}</code> - Имя покупателя\n<code>{brand}</code> - Название вашего бренда\n<code>{offer}</code> - товар который нужно предложить\n\nТаким образом вы сможете сделать следующий текст:\n<b><code>5:{name} спасибо за покупку! {brand} работает для вас! Возможно вам будет интересен этот товар {offer}|Спасибо за покупку {name}! Наш бренд {brand} работает для вас! Возможно вам будет интересен этот товар {offer}</code></b>', reply_markup=markup, parse_mode='html')
#         await state.update_data(stop_words=stop_words, stop_words_user=stop_words_user)
#         await state.set_state(add_template_state.five)
#     except:
#         await message.answer('Произошла ошибка, возможно вы ввели текст неправильно, попробуйте еще раз.', reply_markup=markup)

    
# @router.message(add_template_state.five)
# async def get_text_template(message: types.Message, state: FSMContext):
#     texts = message.text
#     template_user = message.text
#     markup = menu()
#     try:
#         texts = texts.split('&')
#         data = await state.get_data()
#         star = data['star']
#         star.sort()
#         check_ = []
#         for i in texts:
#             a = i.split(':')
#             b = a[0].strip()
#             check_.append(b)
#             b = int(b)
#         check_.sort()
        
#         if check_ == star:
#             pass
#         else: raise ValueError
        
        
#         name = data['name']
#         star = data['star']
#         articul = data['articul']
#         stop_words = data['stop_words']
#         have_text = data['have_text']
#         offer = data['offer']
#         stop_words_user = data['stop_words_user']
#         offer_user = data['offer_user']
#         res = await create_template_func(name, articul, texts, star, stop_words, have_text, offer, template_user, stop_words_user, offer_user, message.from_user.id)
#         await message.answer('Отлично! Шаблон создан.', reply_markup=markup, parse_mode='html')
#         await state.clear()
#     except Exception as ex:
#         print(ex)
#         await message.answer('Произошла ошибка, возможно вы ввели текст неправильно, попробуйте еще раз.', reply_markup=markup)
    

# # --------------------------------- Шаблоны -------------------------------- #

# @router.callback_query(F.data == 'templates')
# async def get_templates(callback: types.CallbackQuery, state: FSMContext):
#     user_id = callback.from_user.id
#     markup = get_templates_markup_user(user_id)
#     await bot.edit_message_text(text='Добавленные шаблоны 👇', message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup)


# @router.callback_query(filtersbot.Templates.filter(F.action.in_(['get_t'])))
# async def custom_button(callback: types.CallbackQuery, state: FSMContext):
#     call = callback.data.split(':')
#     name = call[1]
#     template = await databasework.check_name_template_db(name)
#     if template == None:
#         template = await databasework.check_name_template_db_all(name)
#     template_text = eval(template['template'])
#     star = eval(template['star'])
#     stop_words = eval(template['stop_words'])
#     have_text = template['have_text']
        
#     stars = ''
    
#     for i in star:
#         stars += f'{i}, '   
    
#     markup = get_template_markup(name, have_text)
    
#     await bot.edit_message_text(text=f"Название шаблона - <b>{template['name']}</b>\n\nАртикул - <b>{template['articul']}</b>\n\nНаличие текста в отзыве - <b>{template['have_text']}</b>\n\nОценки - <b>{stars}</b>\n\n<b>Для редактирования шаблона используйте кнопки ниже 👇</b>", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')



# # ---------------------------------- Редактирование шаблона -------------------------------- #



# @router.callback_query(filtersbot.EditTemplate.filter(F.action.in_(['del_t', 'dup_t', 'ed_t_t', 'ed_t_s', 'ed_t_a', 'ed_t_o'])))
# async def edit_template_(callback: types.CallbackQuery, state: FSMContext):
#     markup = menu()
#     call = callback.data.split(':')
#     print(call)
#     name = call[1]
#     have_text = call[2]
#     action = call[-1]
#     if action == 'del_t':
#         check_template = await databasework.check_name_template_db_all(name)
#         if check_template == None:
#             await databasework.delete_template_db(name)
#             await bot.edit_message_text(text=f"Шаблон {name} успешно удален.", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#         else:
#             await databasework.delete_template_db_all(name)
#             await bot.edit_message_text(text=f"Шаблон {name} успешно удален.", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
            
#     elif action == 'dup_t':
#         check_template = await databasework.check_name_template_db_all(name)
#         if check_template == None:
#             await bot.edit_message_text(text=f"Введите артикул, для которого нужно создать такой-же шаблон!", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#             await state.update_data(name=name, have_text=have_text) 
#             await state.set_state(duplicate_template_state.one)
#         else:
#             await bot.edit_message_text(text=f"Вы можете дублировать только тот шаблон, который был создан на определенный артикул!", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#     elif action == 'ed_t_t':
#         template = await databasework.check_name_template_db(name)
#         if template == None:
#             template = await databasework.check_name_template_db_all(name)
#         text = template['template_user']
#         await bot.edit_message_text(text=f"Сейчас в вашем шаблон такой текст:\n\n<b><code>{text}</code></b>\n\n<b>Для изменения текста отредактируйте его и введите в таком-же формате!</b>", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#         await state.set_state(edit_template_state.one)
#         await state.update_data(name=name, have_text=have_text)
#     elif action == 'ed_t_s':
#         template = await databasework.check_name_template_db(name)
#         if template == None:
#             template = await databasework.check_name_template_db_all(name)
#         stop_words_user = template['stop_words_user']
#         await bot.edit_message_text(text=f"Сейчас в вашем шаблон такие стоп-слова:\n\n<b><code>{stop_words_user}</code></b>\n\n<b>Для изменения текста отредактируйте его и введите в таком-же формате!</b>", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#         await state.set_state(edit_template_state.two)
#         await state.update_data(name=name, have_text=have_text)
#     elif action == 'ed_t_a':
#         template = await databasework.check_name_template_db(name)
#         if template == None:
#             template = await databasework.check_name_template_db_all(name)
#         articul = template['articul']
#         if articul == '*':
#             await bot.edit_message_text(text=f"Данный шаблон создан для всех артикулов, его нельзя отредактировать!", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#         else: 
#             await bot.edit_message_text(text=f"Сейчас в вашем шаблон установлен артикул <b><code>{articul}</code></b>\nВведите новый артикул.", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#             await state.set_state(edit_template_state.three)
#             await state.update_data(name=name, have_text=have_text)
#     elif action == 'ed_t_o':
#         template = await databasework.check_name_template_db(name)
#         if template == None:
#             template = await databasework.check_name_template_db_all(name)
#         offer_user = template['offer_user']
#         await bot.edit_message_text(text=f"Сейчас в вашем шаблон такие офферы:\n\n<b><code>{offer_user}</code></b>\n\n<b>Для изменения текста отредактируйте его и введите в таком-же формате!</b>", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
#         await state.set_state(edit_template_state.four)
#         await state.update_data(name=name)
            
#     # ------- Изменение текста
    
    
# @router.message(edit_template_state.one)
# async def edit_template_text_handler(message: types.Message, state: FSMContext):
#     try:
#         data = await state.get_data()
#         name = data['name']
#         texts = message.text
#         template_user_text = message.text
#         markup = menu()
#         template = await databasework.check_name_template_db(name)
#         if template == None:
#             template = await databasework.check_name_template_db_all(name)
#         try:
#             texts = texts.split('&')
#             star = eval(template['star'])
#             star.sort()
#             check_ = []
#             for i in texts:
#                 a = i.split(':')
#                 b = a[0].strip()
#                 check_.append(b)
#                 b = int(b)
#             check_.sort()
#             if check_ == star:
#                 pass
#             else: raise ValueError
#             texts = list(map(str.strip, texts))
#             texts = str(texts) 
#             if template['articul'] == '*':
#                 await databasework.update_template_text_all(texts, template_user_text, name)
#             else:
#                 await databasework.update_template_text(texts, template_user_text, name)
#             await message.answer('Отлично! Текст шаблона отредактирован!', reply_markup=markup, parse_mode='html')
#             await state.clear()
#         except Exception as ex:
#             print(ex)
#             await message.answer('Произошла ошибка, возможно вы ввели текст неправильно, попробуйте еще раз.', reply_markup=markup)
#     except Exception as ex:
#         print(ex)
    
    
    
#  # ----- Изменение стоп-слов
    
    
# @router.message(edit_template_state.two)
# async def edit_template_stop_words_handler(message: types.Message, state: FSMContext):
#     try:
#         data = await state.get_data()
#         name = data['name']
#         have_text = data['have_text']
#         stop_words = message.text
#         stop_words_user = message.text
#         markup = menu()
#         if have_text == 'no':
#             await message.answer('Шаблон работает только на отзывы без текста, у него же не может быть стоп-слов!', reply_markup=markup)
#             await state.clear()
#         else:
#             template = await databasework.check_name_template_db(name)
#             if template == None:
#                 template = await databasework.check_name_template_db_all(name)
#             try:
#                 stop_words = stop_words.split('&')
#                 star = eval(template['star'])
#                 star.sort()
#                 check_ = []
#                 for i in stop_words:
#                     a = i.split(':')
#                     b = a[0].strip()
#                     check_.append(b)
#                     b = int(b)
#                 check_.sort()
#                 if check_ == star:
#                     pass
#                 else: raise ValueError
#                 stop_words = list(map(str.strip, stop_words))
#                 stop_words = str(stop_words) 
#                 if template['articul'] == '*':
#                     await databasework.update_template_stop_words_all(stop_words, stop_words_user, name)
#                 else:
#                     await databasework.update_template_stop_words(stop_words, stop_words_user, name)
#                 await message.answer('Отлично! стоп-слова шаблона отредактировны!', reply_markup=markup, parse_mode='html')
#                 await state.clear()
#             except Exception as ex:
#                 print(ex)
#                 await message.answer('Произошла ошибка, возможно вы ввели стоп-слова неправильно, попробуйте еще раз.', reply_markup=markup)
#     except Exception as ex:
#         print(ex)
    
    
    
# # ----- Изменить артикул
    
    
# @router.message(edit_template_state.three)
# async def edit_template_articul_handler(message: types.Message, state: FSMContext):
#     try:
#         markup = menu()
#         data = await state.get_data()
#         articul_new = message.text
#         have_text = data['have_text']
#         name = data['name']
#         check_articul = await databasework.check_name_articul_db(articul_new, have_text)
#         if check_articul == None:
#             if articul_new.isdigit():
#                 await databasework.update_template_articul(articul_new, name)
#                 await message.answer(f'Успех! Новый артикул <b><code>{articul_new}</code></b> установлен!', reply_markup=markup, parse_mode='html')
#                 await state.clear()
#             else:
#                 await message.answer('Артикул должен состояить из цифр!', reply_markup=markup)
#         else:
#             await message.answer('Шаблон с таким артикулем уже есть!', reply_markup=markup)
#     except Exception as ex:
#         print(ex)
            
            
    
#  # ------ Изменение офферов
    
    
# @router.message(edit_template_state.four)
# async def edit_template_offer_handler(message: types.Message, state: FSMContext):
#     try:
#         markup = menu()
#         data = await state.get_data()
#         offer_new_user = message.text
#         name = data['name']
#         offers_new = offer_new_user.split('|')
#         for i in offers_new:
#             if i.isdigit():
#                 pass
#             else: raise ValueError
#         offers_new = list(map(str.strip, offers_new))
#         offers_new = str(offers_new)
#         template = await databasework.check_name_template_db(name)
#         if template == None:
#             await databasework.update_template_offer_all(offers_new, offer_new_user, name)
#         else:
#             print('1')
#             await databasework.update_template_offer(offers_new, offer_new_user, name)
            
#         await message.answer(f'Новые офферы установлены! \n\n{offer_new_user}', reply_markup=markup)
#         await state.clear()
            
#     except Exception as ex:
#         print(ex)
#         await message.answer('Возникла ошибка, провьте все ли артикулы состоят из цифр', reply=markup)
            
    
    
# # --------------------------- Дублирование шаблона ---------------------------- #
    
# @router.message(duplicate_template_state.one)
# async def duplicate_template_(message: types.Message, state: FSMContext):
#     articul = message.text
#     markup = menu()
    
#     if articul.isdigit():
#         data = await state.get_data()
#         have_text = data['have_text']
#         check_articul = await databasework.check_name_articul_db(articul, have_text)
#         if check_articul == None:
#             await message.answer('Отлично, введите название шаблона', reply_markup=markup)
#             await state.update_data(articul=articul)
#             await state.set_state(duplicate_template_state.two)
#         else: await message.answer('Шаблон на такой артикул уже существует, введите уникальный.', reply_markup=markup)
#     else: await message.answer('Введите артикул состоящий из цифр!', reply_markup=markup)


# @router.message(duplicate_template_state.two)
# async def duplicate_template_(message: types.Message, state: FSMContext):
#     name = message.text
#     markup = menu()
    
#     check_articul = await databasework.check_name_template_db(name)
#     if check_articul == None:
#         data = await state.get_data()
#         old_name = data['name']
#         articul = data['articul']
#         await databasework.insert_duplicate_template_db(name, articul, old_name)
#         await message.answer(f'Отлично, шаблон {name} создан!', reply_markup=markup)
#         await state.clear()
#     else: await message.answer('Шаблон с таким названием уже существует, введите другое', reply_markup=markup)

# ---------------------------------- Изменить тайминг парсера -------------------------------- #


@router.callback_query(F.data == 'edit_time_pars')
async def time_pars(callback: types.CallbackQuery, state: FSMContext):
    markup = menu()
    await bot.edit_message_text(text=f"Сейчас бот собирает отзывы каждые <b>{file_config['time_pars']} секунд</b>, если хотите установить новое значение - введите число в секундках от 300 до 3600.", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
    await state.set_state(edit_time_pars_state.one)

@router.message(edit_time_pars_state.one)
async def edit_time_pars(message: types.Message, state: FSMContext):
    markup = menu()
    time = message.text
    
    if time.isdigit():
        if (int(time) > 200 or int(time) < 1200):
            file_config['time_pars'] = int(time)
            with open(bot_config_path, 'w', encoding='utf-8') as file:
                json.dump(file_config, file, indent=4)  # indent=4 для красивого форматирования (необязательно)
            await message.answer(f'Успешно! Установлено новое значение <b>{time} секунд!</b>', parse_mode='html', reply_markup=markup)
            await state.clear()
        else: await message.answer('Введите число в секундах от 200 до 1200 секунд!', reply_markup=markup)
    else: await message.answer('Введите число!', reply_markup=markup)




# ---------------------------------- Выгрузить отзывы -------------------------------- #
@router.callback_query(F.data == 'load_reviews')
async def load_reviews(callback: types.CallbackQuery, state: FSMContext):
    action='get_cabinets'
    user_id = callback.from_user.id
    markup = get_cabinets_markup(action, user_id)
    await bot.edit_message_text(text=f"Выбери кабинет 👇", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
    #await state.set_state(edit_time_pars_state.one)
    
    
@router.callback_query(filtersbot.CallbackDataFilter.filter(F.action.in_(['get_cabinets'])))
async def custom_button(callback: types.CallbackQuery, state: FSMContext):
    markup = menu()
    call = callback.data.split(':')
    name_cabinet = call[1]
    res = await databasework.check_name_cabinet_db(name_cabinet)
    profile_name = res['profile_name']
    await state.update_data(profile_name=profile_name)
    await bot.edit_message_text(text=f"Укажите время за которое нужно собрать отзывы в формате:\n\n<b>ГГГГ.ММ.ДД-ГГГГ.ММ.ДД</b>\n\nСначала ввести начальную дату, потом конечную дату, например 2023.11.11-2023.12.11", message_id=callback.message.message_id, chat_id=callback.message.chat.id, reply_markup=markup, parse_mode='html')
    await state.set_state(load_reviews_state.one)
    
import csv
@router.message(filtersbot.AdminCheck(), load_reviews_state.one)
async def create_name_cabinet(message: types.Message, state: FSMContext):
    name = message.text
    markup = menu2()
    try:
        dates = name.split('-')
        if len(dates) == 2:
            for i in dates:
                if len(i.split('.')) == 3:
                    pass
                else:
                    raise ValueError
            
            data = await state.get_data()
            profile_name = data['profile_name']
                    
            start_time = dates[0].replace('.', '-')
            end_time = dates[1].replace('.', '-')
            start_date = datetime.datetime.strptime(start_time, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_time, "%Y-%m-%d")
            file_name = 'reviews.csv'
            result = await databasework.get_reviews_db(start_date, end_date, profile_name)
            
            with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['uuid', 'client_name', 'star', 'articul', 'positive_text', 'negative_text', 'comment_text', 'answer', 'date'])
                for i in result:
                    uuid = i['uuid_review']
                    client_name = i['client_name']
                    star = i['star']
                    articul = i['articul']
                    positive_text = i['positive_text']
                    negative_text = i['negative_text']
                    comment_text = i['comment_text']
                    answer = remove_invisible_chars(i['answer'])
                    data = i['datetime']
                    writer.writerow([uuid, client_name, star, articul, positive_text, negative_text, comment_text, answer, data])
            
            file = FSInputFile(file_name)
            await bot.send_document(chat_id=message.chat.id, document=file, caption='Все отзывы за выбранный вами период 👆\nФормат:\n\nuuid;имя клиента;оценка;артикул;достоинства;недостатки;комментарий;ответ;дата', reply_markup=markup)
            os.remove(file_name)
        else:
            await message.answer('Введите верно согласно формату!', reply_markup=markup)
        
    except Exception as ex:
        print(ex)
        await message.answer('Произошла ошибка, попробуйте еще раз', reply_markup=markup)

def remove_invisible_chars(text):
    # Фильтрация видимых символов
    visible_chars = [char for char in text if char.isprintable()]

    # Объединение видимых символов в строку
    cleaned_text = ''.join(visible_chars)

    return cleaned_text

handler1 = router