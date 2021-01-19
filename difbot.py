import telebot 
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import bs4
import requests
import details
import database
import atexit
import os, shutil
import signal
import time




#token
bot = telebot.TeleBot("1465833248:AAEz1W4GE5xDdiswfiEkNhB6WZ4eRHs_Mbc")

channel_id = -1001402037135
channel = bot.get_chat(channel_id)
downloaded_file = bot.download_file(
    bot.get_file(channel.pinned_message.document.file_id).file_path)
with open("user.db", 'wb') as file: file.write(downloaded_file)

bot.send_message(319202816, "Bot herokuda uyg'ondi bro")

#main buttons
main_buttons = ["🧎Namoz vaqtlari", "🌦Ob-havo ma'lumotlari", "💲Valyuta kursi", "🗣Ismlar ma'nosi"]

api_list = ["https://islom.uz/vaqtlar/", "https://weather.town/forecast/uzbekistan/", "https://nbu.uz/uz/exchange-rates/json/", "https://ismlar.com/name/"]

#namoz regions
region_times = {'Toshkent': 27, 'Qo\'qon': 26, 'Samarqand': 18, 'Andijon': 1, 'Buxoro': 4, 'Navoiy': 14, 'Jizzax': 9, 
'Qarshi': 25, 'Marg\'ilon': 13, 'Namangan': 15, 'Xiva': 21, 'Nukus': 16}


#weah=ther links
regions_field = ['andijan/andijon', 'namangan-province/namangan', 'fergana/fergana', 'toshkent-shahri/tashkent', 'bukhara-province/bukhara', 'samarqand-viloyati/samarqand', 'qashqadaryo-province/qashqadaryo', 'sirdaryo/sirdaryo', 'surxondaryo-viloyati/tirmiz' ,'navoiy-province/navoiy', 'jizzakh-province/jizzax', 'xorazm-viloyati/urganch', 'karakalpakstan/nukus']


#weather regions
regions = ['Andijon', 'Namangan', "Farg'ona", 'Toshkent', 'Buxoro', 'Samarqand', 'Qashqadaryo', 'Sirdaryo', 'Surxondaryo', 'Novoiy', 'Jizzax', 'Xorazm', 'Nukus']

db = database.DbHelper()

details = details.info()

#make main buttons
def MainButtonMaker(markup):
    _list = []

    for i in range(0, len(main_buttons)):
        _list.append(KeyboardButton(main_buttons[i]))
    markup.add(*_list)
    markup.resize_keyboard = True
    return markup


#Starting poin
@bot.message_handler(commands=['start'])

def StartingPoint(message):
    try:
        item = db.GetUser(message.chat.id)

        markup = ReplyKeyboardMarkup(row_width=2)
        markup = MainButtonMaker(markup)

        if len(item) > 0:
            bot.send_message(message.chat.id, "Assalomu alaykum xurmatli foydalanuvchi!Qaytganingizdan xursandmiz. Botdan foydalanish uchun, quyidagilardan birini tanlang👇", reply_markup=markup)
        else:
            db.AddUser(message.chat.id)
            bot.send_message(message.chat.id, "Assalomu alaykum xurmatli foydalanuvchi! Botdan foydalanish uchun, quyidagilardan birini tanlang👇", reply_markup=markup)
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")


@bot.message_handler(func=lambda message: message.text in main_buttons)
def MainSelection(message):
    try:
        index = main_buttons.index(message.text)
        res = 1
        if db.GetUser(message.chat.id)[0]['request'] != None:
            res = int(db.GetUser(message.chat.id)[0]['request']) + 1 
        #namoz vaqti
        if index == 0:
            _list = []
            inline = InlineKeyboardMarkup(row_width=2)
            for item in region_times:
                _list.append(InlineKeyboardButton(text=item, callback_data=str(region_times[item])+' namoz'))
            inline.add(*_list, InlineKeyboardButton(text='❌', callback_data='cancel'))
            bot.send_message(message.chat.id, 'Hududni tanlang:', reply_markup=inline)
        
        #ob-havo
        elif index == 1:
            _list = []
            inline = InlineKeyboardMarkup(row_width=2)
            for item in regions:
                _list.append(InlineKeyboardButton(text=item, callback_data=str(regions.index(item)) + ' havo'))
            inline.add(*_list, InlineKeyboardButton(text='❌', callback_data='cancel'))
            bot.send_message(message.chat.id, 'Hududni tanlang:', reply_markup=inline)
        
        #valyuta    
        elif index == 2:
            inline = InlineKeyboardMarkup(row_width=5)
            result = requests.get(api_list[2])
            r_dict = result.json()
            natija = ""
            for i in range(0, 5):
                natija += f"""Nomi: <b>{r_dict[i]['title']}</b>\nMarkaziy bankda: <b>{r_dict[i]['cb_price']} so'm</b>\n\n"""
            inline.add(InlineKeyboardButton(text='❌', callback_data='cancel'),InlineKeyboardButton(text='➡️', callback_data='next' + "/5 10"))

            bot.send_message(message.chat.id, natija + "\n@khanblogs", parse_mode='html', reply_markup=inline)    
        
        #ismlar ma'nosi
        elif index == 3:
            bot.send_message(message.chat.id, "<b>Ismni kiriting</b>", parse_mode='html')
            db.UpdateUser(message.chat.id, "ism")
        
        db.UpdateRequest(message.chat.id, res)
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")


@bot.message_handler(func=lambda message: db.GetLastMessage(message.chat.id) == 'ism')
def SearchName(message):
    try:
        global ism
        result = requests.get(api_list[3] + message.text)
        soup = bs4.BeautifulSoup(result.text, "lxml")
        if "404" not in soup.select('h2')[0].getText():    
            natija = f"""Ism: <b>{message.text.upper()}</b>\nMa'nosi: <b>{soup.select('p')[0].getText()}</b>"""
        else :
            natija = f"""Ism: <b>{message.text.upper()}</b>\nMa'nosi: <b>Berilgan ismning ma'nosi topilmadi</b>"""
        bot.send_message(message.chat.id, natija + "\n\n@khanblogs", parse_mode='html')
        db.UpdateUser(message.chat.id, "")
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")


#valyuta next handler
@bot.callback_query_handler(func=lambda call: 'next' in call.data)
def NextValyuta(call):
    try:
        
        _list = call.data.split('/')[1]
        inline = InlineKeyboardMarkup(row_width=5)
        result = requests.get(api_list[2])
        r_dict = result.json()
        natija = ""
        if int(_list.split(' ')[1]) <= 20:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            for i in range(int(_list.split(' ')[0]), int(_list.split(' ')[1])):
                natija += f"""Nomi: <b>{r_dict[i]['title']}</b>\nMarkaziy bankda: <b>{r_dict[i]['cb_price']} so'm</b>\n\n"""
            inline.add(InlineKeyboardButton(text='⬅️', callback_data='back' + f"/{int(_list.split(' ')[1]) - 5} {int(_list.split(' ')[0]) - 5}"), InlineKeyboardButton(text='❌', callback_data='cancel'),InlineKeyboardButton(text='➡️', callback_data='next' + f"/{int(_list.split(' ')[0]) + 5} {int(_list.split(' ')[1]) + 5}"))
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            for i in range(int(_list.split(' ')[0]), 24):
                natija += f"""Nomi: <b>{r_dict[i]['title']}</b>\nMarkaziy bankda: <b>{r_dict[i]['cb_price']} so'm</b>\n\n"""
            inline.add(InlineKeyboardButton(text='⬅️', callback_data='back' + "/20 15"), InlineKeyboardButton(text='❌', callback_data='cancel'))
        bot.send_message(call.message.chat.id, natija + "\n@khanblogs", parse_mode='html', reply_markup=inline)    

        
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""") 


#valyuta back handler
@bot.callback_query_handler(func=lambda call: 'back' in call.data)
def BackValyuta(call):
    try:
        _list = call.data.split('/')[1]
        inline = InlineKeyboardMarkup(row_width=5)
        result = requests.get(api_list[2])
        r_dict = result.json()
        natija = ""
        if int(_list.split(' ')[1]) >= 5:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            for i in range(int(_list.split(' ')[1]), int(_list.split(' ')[0])):
                natija += f"""Nomi: <b>{r_dict[i]['title']}</b>\nMarkaziy bankda: <b>{r_dict[i]['cb_price']} so'm</b>\n\n"""
            inline.add(InlineKeyboardButton(text='⬅️', callback_data='back' + f"/{int(_list.split(' ')[0]) - 5} {int(_list.split(' ')[1]) - 5}"), InlineKeyboardButton(text='❌', callback_data='cancel'),InlineKeyboardButton(text='➡️', callback_data='next' + f"/{int(_list.split(' ')[1]) + 5} {int(_list.split(' ')[0]) + 5}"))
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            for i in range(0, 5):                
                natija += f"""Nomi: <b>{r_dict[i]['title']}</b>\nMarkaziy bankda: <b>{r_dict[i]['cb_price']} so'm</b>\n\n"""
            inline.add(InlineKeyboardButton(text='❌', callback_data='cancel'),InlineKeyboardButton(text='➡️', callback_data='next' + "/5 10"))

        bot.send_message(call.message.chat.id, natija + "\n@khanblogs", parse_mode='html', reply_markup=inline)
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")


#cancel handler
@bot.callback_query_handler(func=lambda call: 'cancel' in call.data)
def CancelValyuta(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Bekor qilindi")
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")


#namoz region selection
@bot.callback_query_handler(func=lambda call: 'namoz' in call.data)
def NamozVaqti(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        result =details.NamozVaqtlari(api_list[0] + call.data.split(' ')[0] + '/1')

        #print(result.content)

        bot.send_message(call.message.chat.id, result, parse_mode='html')
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")
    

#weather region selection    
@bot.callback_query_handler(func=lambda call: 'havo' in call.data)
def ObHavo(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        result = details.ObHavo(api_list[1] + regions_field[int(call.data.split(' ')[0])], regions[int(call.data.split(' ')[0])])

        bot.send_message(call.message.chat.id, result, parse_mode='html')
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")


@bot.message_handler(func=lambda message: str(message.text).lower() == "info" and message.chat.id == 319202816)
def AdminInfo(message):
    try:
        item = db.GetAllDatas()

        bot.send_message(319202816, f"""Foydalanuvchilar soni: <b>{len(item)}</b>\nSo'rovlar soni: <b>{sum(int(i['request']) for i in item)}</b>""", parse_mode='html')
    except Exception as e:
        bot.send_message(319202816, f"""Xatolik:\n{e}""")


@bot.message_handler(func=lambda message: message.text == "baza" and message.chat.id == 319202816)  
def Baza(message):
    try:
        with open('user.db', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.send_message(319202816, e)                           

def main():
    try:
        bot.polling(none_stop = True)
    except Exception as e:
        time.sleep(3)
        bot.send_message(319202816, e)
        bot.stop_polling()

def exit_handler():
    bot.send_message(319202816, "Botni uyqusi kelib qolibdi")
    bot.send_document(channel_id, open("user.db", 'rb'))

def handler(signum, frame):
    bot.send_message(319202816, "Botni uyqusi kelib qolibdi")
    msg = bot.send_document(channel_id, open("user.db", 'rb'))
    try:
        bot.unpin_chat_message(channel_id)
        bot.pin_chat_message(channel_id, msg.message_id, disable_notification = True)
    except Exception as e:
        bot.send_message(319202816,e)

atexit.register(exit_handler)
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM, handler)

main()