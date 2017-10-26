# encoding=utf8

#-----import-----#
import ConfigParser
import sys
import time

import telepot

from functions import *
#----------#

#-----config-----#
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

allowed_list = eval(config.get('Telegram', 'allow_list'))
bot_token = config.get('Telegram', 'bot_token')
bot = telepot.Bot(bot_token)
#----------#

#-----Telegram Handler-----#
def handle(msg):
    #Access Control
    if msg['chat']['id'] in allowed_list:
        check_iv_cp(msg)
        get_gps(msg)
        get_map(msg)
        wecatch(msg)
        poketrack(msg)
    else:
        get_gps(msg)
        get_map(msg)
        wecatch(msg)
        poketrack(msg)


bot.message_loop({'chat': handle})
print('Listening ...')
#----------#

while 1:
    time.sleep(10)
