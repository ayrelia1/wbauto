from config import types, InlineKeyboardBuilder
import filtersbot
from function import databasework



def start_markup():
    markup = (
        InlineKeyboardBuilder()
        .button(text='Добавить кабинет ➕', callback_data='add_cabinet')
        .button(text='Кабинеты 🗒', callback_data='cabinets')
        # .button(text='Создать шаблон ➕', callback_data='add_template')
        # .button(text='Шаблоны 📕', callback_data='templates')
        .button(text='Тайминг парсера 🖊', callback_data='edit_time_pars')
        .button(text='Выгрузить отзывы 📈', callback_data='load_reviews')
        .button(text='Выдать доступ 📈', callback_data='give_admin')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


def menu():
    markup = (
        InlineKeyboardBuilder()
        .button(text='В главное меню 🔙', callback_data='main')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup

def menu2():
    markup = (
        InlineKeyboardBuilder()
        .button(text='В главное меню 🔙', callback_data='main2')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


def get_cabinets_markup(action, user_id):
    cabinets = databasework.get_cabinets_user_id(user_id)
    markup = InlineKeyboardBuilder()
    
    for i in cabinets:
        name = i['profile_name']
        markup.row(types.InlineKeyboardButton(text=(f"{name}"), callback_data=filtersbot.CallbackDataFilter(action=action, cabinet=name).pack()))
    markup.row(types.InlineKeyboardButton(text='В главное меню 🔙', callback_data='main'))

    return markup.as_markup()

def get_cabinet_markup(name):
    action = 'delete_cabinet'
    markup = (
        InlineKeyboardBuilder()
        .button(text=('Удалить кабинет ➖'), callback_data=filtersbot.CallbackDataFilter(action=action, cabinet=name).pack())
        .button(text=('В главное меню 🔙'), callback_data='main')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


def get_templates_markup():
    templates = databasework.get_templates_db()
    markup = InlineKeyboardBuilder()
    
    for i in templates:
        name = i['name']
        action = 'get_t'
        markup.row(types.InlineKeyboardButton(text=(f"{name}"), callback_data=filtersbot.Templates(action=action, name=name).pack()))
        
    templates_all = databasework.get_templates_db_all()
        
    for i in templates_all:
        name = i['name']
        action = 'get_t'
        markup.row(types.InlineKeyboardButton(text=(f"{name}"), callback_data=filtersbot.Templates(action=action, name=name).pack()))
    markup.row(types.InlineKeyboardButton(text='В главное меню 🔙', callback_data='main'))
    
    return markup.as_markup()


def get_templates_markup_user(user_id):
    templates = databasework.get_templates_db_user(str(user_id))
    markup = InlineKeyboardBuilder()
    for i in templates:
        name = i['name']
        action = 'get_t'
        markup.row(types.InlineKeyboardButton(text=(f"{name}"), callback_data=filtersbot.Templates(action=action, name=name).pack()))
        
    templates_all = databasework.get_templates_db_all_user(str(user_id))
        
    for i in templates_all:
        name = i['name']
        action = 'get_t'
        markup.row(types.InlineKeyboardButton(text=(f"{name}"), callback_data=filtersbot.Templates(action=action, name=name).pack()))
    markup.row(types.InlineKeyboardButton(text='В главное меню 🔙', callback_data='main'))
    
    return markup.as_markup()


def get_template_markup(name, have_text):
    markup = (
        InlineKeyboardBuilder()
        .button(text=('Удалить шаблон ➖'), callback_data=filtersbot.EditTemplate(action='del_t', name_template=name, have_text=have_text).pack())
        .button(text=('Дублировать шаблон ➕'), callback_data=filtersbot.EditTemplate(action='dup_t', name_template=name, have_text=have_text).pack())
        .button(text=('Изменить текст 🖊'), callback_data=filtersbot.EditTemplate(action='ed_t_t', name_template=name, have_text=have_text).pack())
        .button(text=('Изменить стоп-слова 🖊'), callback_data=filtersbot.EditTemplate(action='ed_t_s', name_template=name, have_text=have_text).pack())
        .button(text=('Изменить артикул 🖊'), callback_data=filtersbot.EditTemplate(action='ed_t_a', name_template=name, have_text=have_text).pack())
        .button(text=('Изменить офферы 🖊'), callback_data=filtersbot.EditTemplate(action='ed_t_o', name_template=name, have_text=have_text).pack())
        .button(text=('В главное меню 🔙'), callback_data='main')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


def text_or_no_markup():
    markup = (
        InlineKeyboardBuilder()
        .button(text='Для отзыва с текстом ➕', callback_data='review_with_text')
        .button(text='Для отзыва без текста ➖', callback_data='review_no_text')
        .button(text=('В главное меню 🔙'), callback_data='main')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup



def question_markup(articul):
    markup = (
        InlineKeyboardBuilder()
        .button(text=('Перейти к товару 🔜'), url=(f'https://www.ozon.ru/product/{articul}'))
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup
