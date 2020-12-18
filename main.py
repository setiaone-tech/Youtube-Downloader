import requests
import json
import telebot

api = "Api-Key"
bot = telebot.TeleBot(api,threaded=False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Selamat datang di BOT Youtube Downloader")
    
@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Cara menggunakan BOT Youtube Downloader")
    bot.send_message(chat_id, "contoh : /search[spasi]pencarian")
    bot.send_message(chat_id, "contoh penggunaan : /search windah cita-cita")
    
@bot.message_handler(commands=['search'])
def send_search(message):
    chat_id = message.chat.id
    pesan = message.text
    bagi = pesan.split(" ",1)
    search = bagi[1]
    judul = ""
    url = requests.get("https://mhankbarbars.herokuapp.com/api/ytsearch?q="+search+"&apiKey=API-KEY").json()
    num = 0
    markup = telebot.types.InlineKeyboardMarkup()
    if url['status'] == 200:
        for i in range(10):
            num += 1
            judul += str(num)+"."+str(url['result'][i]['title'])+" "+str(url['result'][i]['duration'])+"\n"
        id1 = telebot.types.InlineKeyboardButton(text="1", callback_data=url['result'][0]['link'])
        id2 = telebot.types.InlineKeyboardButton(text="2", callback_data=url['result'][1]['link'])
        id3 = telebot.types.InlineKeyboardButton(text="3", callback_data=url['result'][2]['link'])
        id4 = telebot.types.InlineKeyboardButton(text="4", callback_data=url['result'][3]['link'])
        id5 = telebot.types.InlineKeyboardButton(text="5", callback_data=url['result'][4]['link'])
        id6 = telebot.types.InlineKeyboardButton(text="6", callback_data=url['result'][5]['link'])
        id7 = telebot.types.InlineKeyboardButton(text="7", callback_data=url['result'][6]['link'])
        id8 = telebot.types.InlineKeyboardButton(text="8", callback_data=url['result'][7]['link'])
        id9 = telebot.types.InlineKeyboardButton(text="9", callback_data=url['result'][8]['link'])
        id10 = telebot.types.InlineKeyboardButton(text="10", callback_data=url['result'][9]['link'])
        markup.row(id1,id2,id3,id4,id5)
        markup.row(id6,id7,id8,id9,id10)
        bot.send_message(chat_id, text=judul, reply_markup = markup)
    else:
        bot.send_message(chat_id, url['error'])
    
@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    cari = call.data
    url = requests.get('https://mhankbarbars.herokuapp.com/api/ytv?url='+cari+'&apiKey=API-KEY').json()
    bot.send_message(call.from_user.id, "Permintaan anda sedang di proses...")
    if url['status'] == 200:
        bot.send_video(call.from_user.id, url['result'], caption = "title : "+str(url['title'])+"\nFileSize : "+str(url['filesize']))
    else:
        bot.send_message(call.from_user.id, url['error'])
        
@bot.message_handler(commands=['about'])
def send_about(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "BOT ini dibuat menggunakan bahasa pemrogram Python.\nBOT ini dibuat dikala kegabutan melanda.\n\nAuthor : Tia\nSpecial Thanks : pyTelegramBotAPI Indonesia")

while True:
  try:
    bot.polling()
  except:
    bot.stop_polling()
