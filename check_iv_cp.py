# encoding=utf8  

#import for telegram
import sys
import time
import telepot
import requests
import functions

#import for pgoapi
from pgoapi import PGoApi
from pgoapi.hash_server import HashServer
from pgoapi import utilities as util
import pprint
import random
api = PGoApi()

#logging
import logging
logger = logging.getLogger('TelemonGO')
logger.setLevel(logging.DEBUG)
logger2 = logging.StreamHandler()
logger2.setLevel(logging.ERROR)
logger.addHandler(logger2)
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [line %(lineno)d] - [%(message)s]')
logger2.setFormatter(formatter)

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

ac_sum = 0
place = None

pkm_hk = json.load('pkmn_hk.json')
pkm_mv = json.load('pkm_mv.json')

def handle(msg):
    global ac_sum

    #Access Control
    if msg['chat']['id'] in allowed_list:
        check_iv_cp()
        gps()
        show_map()

bot.message_loop({'chat': handle})
print('Listening ...')

while 1:
    time.sleep(10)
