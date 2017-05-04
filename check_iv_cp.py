# encoding=utf8  

#import for telegram
import sys
import time
import telepot
from functions import check_iv_cp, show_map, gps

##+++++++++++++++++++++++Edit below items+++++++++++++++++++++++++++#
#hash_key = "<hashkey>"
#ac_list = ["<username>"]
#pw_list = ["<password>"]
#home_lat = float(<lat>)
#home_lng = float(<lng>)
#allowed_list = [<telegram_id>]
#own_id = <telegram_id>
#bot = telepot.Bot("<bot_token>")
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def handle(msg):
    global ac_sum

    #Access Control
    if msg['chat']['id'] in allowed_list:
        check_iv_cp(msg)
        gps(msg)
        show_map(msg)

bot.message_loop({'chat': handle})
print('Listening ...')

while 1:
    time.sleep(10)
