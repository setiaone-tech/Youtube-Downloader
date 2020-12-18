import requests
import json
import telebot

api = "Api-Key Telegram Bot"
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
        for i in url['result']:
            num += 1
            judul += str(num)+"."+str(i['title'])+"\n"
            markup.add(telebot.types.InlineKeyboardButton(text=num, callback_data=i['link']))
        bot.send_message(chat_id, text=judul, reply_markup = markup)
    else:
        bot.send_message(chat_id, url['error'])
    
@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    cari = call.data
    url = requests.get('https://mhankbarbars.herokuapp.com/api/ytv?url='+cari+'&apiKey=API-KEY').json()
    bot.send_message(call.from_user.id, "Permintaan anda sedang di proses...")
    if url['status'] == 200:
        bot.send_video(call.from_user.id, url['result'])
    else:
        bot.send_message(call.from_user.id, url['error']
        
@bot.message_handler(commands=['about'])
def send_about(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "Author : Tia:)\n Thanks For : Feri <3"

while True:
  try:
    bot.polling()
  except:
    bot.stop_polling()
