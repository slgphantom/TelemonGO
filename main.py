# encoding=utf8  

#import for telegram
import sys
import time
import telepot
import ConfigParser
from functions import check_iv_cp, show_map, gps

#config
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

allowed_list = eval(config.get('Telegram', 'allow_list'))
bot_token = config.get('Telegram', 'bot_token')
bot = telepot.Bot(bot_token)


def handle(msg):
    global ac_sum

    #Access Control
    if msg['chat']['id'] in allowed_list:
        check_iv_cp(msg)
        gps(msg)
        show_map(msg)
    else:
        gps(msg)
        show_map(msg)

bot.message_loop({'chat': handle})
print('Listening ...')

while 1:
    time.sleep(10)
