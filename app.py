import telegram
import configparser
import redis
from random import randint

#Telegram libs
from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
#from apiclient.discovery import build

#libraes for geting images from google
from bs4 import BeautifulSoup
import requests
import re
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import os
try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

import json


# Configuring bot
config = configparser.ConfigParser()
config.read_file(open('config.ini'))

# Connecting to Telegram API
# Updater retrieves information and dispatcher connects commands
updater = Updater(token=config['DEFAULT']['token'])
dispatcher = updater.dispatcher

# Connecting to Redis db
db = redis.StrictRedis(host=config['DB']['host'],
                       port=config['DB']['port'],
                       db=config['DB']['db'])

def start(bot, update):
    try:
        me = bot.get_me()

        # Welcome message
        msg = "Eae!\n"
        msg += "Eu sou o {0} .\n".format(me.first_name)
        msg += "Quer ver umas fotos maneiras de Dogs? \n\n"
        msg += "/support - Fale com o desenvolvedor\n"
        msg += "/settings - Configurações \n\n"
        msg += "/pic - Mostre a imagem de um Doggo com sobrancelha aleatório"	

        # Commands menu
        main_menu_keyboard = [[telegram.KeyboardButton('/support')],
                          [telegram.KeyboardButton('/settings')],
			  [telegram.KeyboardButton('/pic')]]
        reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

        # Send the message with menu
        bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=reply_kb_markup)
    except Exception as e:
        print (e)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def support(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                        text="Por Favor, entre em contato com o desenvolvedor : @lukassl")
    except Exception as e:
        print (e)

support_handler = CommandHandler('support', support)
dispatcher.add_handler(support_handler)

def pic(bot, update):
    try:
        def get_soup(url,header):
            return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

        query = 'dog with eyebrows'# you can change the query for the image  here
        image_type="ActiOn"
        query= query.split()
        query='+'.join(query)
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        print (url)

        #add the directory for your image here
        DIR="Pictures"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = get_soup(url,header)


        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))

        print  ("there are total" , len(ActualImages),"images")

        ###print images
        aux = []
        for i , (img , Type) in enumerate( ActualImages):
            try:
                aux.append(img)
                
            except Exception as e:
                print (img)
                print (e)
        num = randint(0,99)
        bot.send_photo(chat_id=update.message.chat_id,photo=''+aux[num]+'')

    except Exception as e:
        print (e)
            
           

pic_handler = CommandHandler('pic', pic)
dispatcher.add_handler(pic_handler)


def settings(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                        text="Fiquei com preguiça de fazer isso, malz ae")

settings_handler = CommandHandler('settings', settings)
dispatcher.add_handler(settings_handler)


def unknown(bot, update):
    try:
        msg = "Digita direito, não entendi o que você quer :/."
        bot.send_message(chat_id=update.message.chat_id,
                         text=msg)
    except Exception as e:
        print (e)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
