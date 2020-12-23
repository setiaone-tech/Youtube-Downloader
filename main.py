import requests
import json
import telebot
from pythonping import ping
import wget
import urllib
import datetime

api = "TELEGRAM API-KEY"
bot = telebot.TeleBot(api,threaded=False)
def log(message, perintah):
    nama_awal = message.chat.first_name
    nama_akhir = message.chat.last_name
    ttd = datetime.datetime.now().strftime('%d-%B-%Y')
    text_log = '{}, {} {}, {}\n'.format(ttd, nama_awal, nama_akhir, perintah)
    log_bot = open('log_bot.txt', 'a')
    log_bot.write(text_log)
    log_bot.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    log(message, 'start')
    bot.reply_to(message, "Selamat datang di BOT Youtube Downloader")
    
@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Cara menggunakan BOT Youtube Downloader")
    bot.send_message(chat_id, "contoh : /search[spasi]pencarian")
    bot.send_message(chat_id, "contoh penggunaan : /search windah cita-cita")
    
@bot.message_handler(commands=['search'])
def send_search(message):
    log(message, message.text)
    chat_id = message.chat.id
    pesan = message.text
    bagi = pesan.split(" ",1)
    search = bagi[1]
    judul = ""
    url = requests.get("https://mhankbarbars.herokuapp.com/api/ytsearch?q="+search+"&apiKey=api-key").json()
    num = 0
    markup = telebot.types.InlineKeyboardMarkup()
    if url['status'] == 200:
        for i in range(10):
            num += 1
            judul += str(num)+"."+str(url['result'][i]['title'])+" "+str(url['result'][i]['duration'])+"\n"
        id1 = telebot.types.InlineKeyboardButton(text="1🎬", callback_data="/m4 "+url['result'][0]['link'])
        id2 = telebot.types.InlineKeyboardButton(text="2🎬", callback_data="/m4 "+url['result'][1]['link'])
        id3 = telebot.types.InlineKeyboardButton(text="3🎬", callback_data="/m4 "+url['result'][2]['link'])
        id4 = telebot.types.InlineKeyboardButton(text="4🎬", callback_data="/m4 "+url['result'][3]['link'])
        id5 = telebot.types.InlineKeyboardButton(text="5🎬", callback_data="/m4 "+url['result'][4]['link'])
        id6 = telebot.types.InlineKeyboardButton(text="6🎬", callback_data="/m4 "+url['result'][5]['link'])
        id7 = telebot.types.InlineKeyboardButton(text="7🎬", callback_data="/m4 "+url['result'][6]['link'])
        id8 = telebot.types.InlineKeyboardButton(text="8🎬", callback_data="/m4 "+url['result'][7]['link'])
        id9 = telebot.types.InlineKeyboardButton(text="9🎬", callback_data="/m4 "+url['result'][8]['link'])
        id10 = telebot.types.InlineKeyboardButton(text="10🎬", callback_data="/m4 "+url['result'][9]['link'])
        id11 = telebot.types.InlineKeyboardButton(text="1🎧", callback_data="/m3 "+url['result'][0]['link'])
        id12 = telebot.types.InlineKeyboardButton(text="2🎧", callback_data="/m3 "+url['result'][1]['link'])
        id13 = telebot.types.InlineKeyboardButton(text="3🎧", callback_data="/m3 "+url['result'][2]['link'])
        id14 = telebot.types.InlineKeyboardButton(text="4🎧", callback_data="/m3 "+url['result'][3]['link'])
        id15 = telebot.types.InlineKeyboardButton(text="5🎧", callback_data="/m3 "+url['result'][4]['link'])
        id16 = telebot.types.InlineKeyboardButton(text="6🎧", callback_data="/m3 "+url['result'][5]['link'])
        id17 = telebot.types.InlineKeyboardButton(text="7🎧", callback_data="/m3 "+url['result'][6]['link'])
        id18 = telebot.types.InlineKeyboardButton(text="8🎧", callback_data="/m3 "+url['result'][7]['link'])
        id19 = telebot.types.InlineKeyboardButton(text="9🎧", callback_data="/m3 "+url['result'][8]['link'])
        id20 = telebot.types.InlineKeyboardButton(text="10🎧", callback_data="/m3 "+url['result'][9]['link'])
        markup.row(id1,id2,id3,id4,id5)
        markup.row(id6,id7,id8,id9,id10)
        markup.row(id11,id12,id13,id14,id15)
        markup.row(id16,id17,id18,id19,id20)
        bot.send_message(chat_id, text=judul, reply_markup = markup)
    else:
        bot.send_message(chat_id, url['error'])
    
@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    cari = call.data
    bagi = cari.split(" ",1)
    search = bagi[1]
    if bagi[0] == "/m4":
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Authorization": "Bearer Api-Key"
        }
        data = {
        "url" : search
        }
        url = requests.get("https://afara.my.id/api/v3/get-youtube-video-link", data=json.dumps(data), headers=headers).json()
        bot.send_message(call.from_user.id, "Permintaan anda sedang di proses...")
        if url['status'] == 'success':
            bot.send_video(call.from_user.id, url['data']['urls'][0]['url'])
        else:
            bot.send_message(call.from_user.id, url['error'])
    else:
        url = requests.get('https://mhankbarbars.herokuapp.com/api/yta?url='+search+'&apiKey=api-key').json()
        if url['status'] == 200:
            bagi = url['filesize'].split(" ")
            ukuran = bagi[0]
            if float(ukuran) < 20:
                bot.send_message(call.from_user.id, "Mohon tunggu sebentar... sedang mendownload lagu sebesar "+url['filesize']+" mb")
                target = url['result']
                r = requests.get(target)
                open(url['title']+'.MP3', 'wb').write(r.content)
                lagu = open(url['title']+".MP3", "rb")
                bot.send_audio(call.from_user.id, lagu)
            else:
                bot.send_message(call.from_user.id, "Ukuran file lebih dari 20mb!")
        else:
            bot.send_message(call.from_user.id, url['message'])
        
@bot.message_handler(commands=['about'])
def send_about(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "BOT ini dibuat menggunakan bahasa pemrogram Python.\nBOT ini dibuat dikala kegabutan melanda.\n\nAuthor : Tia\nSpecial Thanks : pyTelegramBotAPI Indonesia")

@bot.message_handler(commands=['cek'])
def send_cek(message):
        chat_id = message.chat.id
        hasil = ping('mhankbarbars.herokuapp.com')
        bot.send_message(chat_id, hasil)
while True:
      try:           
         bot.polling(none_stop = True, interval = 10, timeout = 60)
      except:
         bot.stop_polling()
