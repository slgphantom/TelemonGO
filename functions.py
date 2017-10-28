#encoding=utf8

#-----import-----#
import ConfigParser
from datetime import datetime
import json
import logging
import pprint
import random
import re
import sys
import time
from pytz import timezone
from urllib import urlopen

from pgoapi import PGoApi
from pgoapi.hash_server import HashServer
from pgoapi import utilities as util
import requests
import telepot
#----------#


#-----logging-----#
logger = logging.getLogger('TelemonGO')
logger.setLevel(logging.DEBUG)
logger2 = logging.StreamHandler()
logger2.setLevel(logging.ERROR)
logger.addHandler(logger2)
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [line %(lineno)d] - [%(message)s]')
logger2.setFormatter(formatter)
#----------#


#-----config-----#
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

hash_key = config.get('DEFAULT', 'hash_key')
ac_list = eval(config.get('account', 'user'))
pw_list = eval(config.get('account', 'pass'))
home_lat = config.getfloat('Location', 'lat')
home_lng = config.getfloat('Location', 'lng')
allowed_list = eval(config.get('Telegram', 'allow_list'))
own_id = config.getint('Telegram', 'admin_id')
bot_token = config.get('Telegram', 'bot_token')
message_recieved_text = config.get('message', 'message_recieved_text').replace('\\n','\n')
text_style = config.get('message', 'text').replace('\\n','\n')
not_found_text = config.get('message', 'not_found_text').replace('\\n','\n')
speed_lock_text = config.get('message', 'speed_lock_text').replace('\\n','\n')
login_fail_text = config.get('message', 'login_fail_text').replace('\\n','\n')
not_in_range_text = config.get('message', 'not_in_range_text').replace('\\n','\n')
bot = telepot.Bot(bot_token)
#----------#


#-----loading json-----#
with open('pkmn_hk.json') as json_name:
    pkm_hk = json.load(json_name)

with open('pkm_mv.json') as json_mv:
    pkm_mv = json.load(json_mv)
#----------#


ac_sum = 0
place = None
api = PGoApi()
alt = random.uniform(0.0, 70.0)


#-----Telegram bot function-----#
def get_gps(msg):
    if "reply_to_message" in msg and 'location' in msg['reply_to_message'] and 'text' in msg and msg['text'].startswith('/gps'):
        lat = float(msg['reply_to_message']['location']['latitude'])
        lng = float(msg['reply_to_message']['location']['longitude'])
        f = urlopen('https://maps.googleapis.com/maps/api/staticmap?zoom=17&size=512x512&maptype=hybrid&markers=color:red|' + str(lat) + ',' + str(lng))
        bot.sendPhoto(msg['chat']['id'], f)
        pass


def get_map(msg):
    if 'text' in msg and msg['text'].startswith('/map'):
        try:
            #location = msg['text'].split(' ')
            location = re.split('[ ,]', msg['text'])
            bot.sendLocation(msg['chat']['id'], location[1], location[2])
        except:
            bot.sendMessage(msg['chat']['id'], "打 /map <lat> <lng>，獲得地圖一份", parse_mode = 'html')
        pass


def wecatch(msg):
    if 'text' in msg and 'https://wecatchpokemon.cdstud.io/?' in msg['text']:
        info = re.search("(?P<url>https?://[^\s]+)", msg['text']).group("url").replace('https://wecatchpokemon.cdstud.io/?', '')
        info = re.split('&|=', info)
        lat = float(info[1])
        lng = float(info[3])
        bot.sendLocation(msg['chat']['id'], lat, lng)
        travel(msg, lat, lng)
        pass


def poketrack(msg):
    if 'text' in msg and 'http://m.poketrack.xyz/' in msg['text']:
        info = re.search("(?P<url>https?://[^\s]+)", msg['text']).group("url")
        data = requests.get(info).url
        data2 = re.split('[=&]', data)
        lat = float(data2[1])
        lng = float(data2[3])
        bot.sendLocation(msg['chat']['id'], lat, lng)
        travel(msg, lat, lng)
        pass
#----------#


#-----Check CP-----#
def login():
    try:
        global ac_sum
        #Support ptc account onlt
        api.login('ptc', ac_list[ac_sum], pw_list[ac_sum])
        ac_sum += 1
        if ac_sum == len(ac_list):
            ac_sum = 0
            return True
    except:
        ac_sum += 1
        if ac_sum == len(ac_list):
            ac_sum = 0
            return True
        print "{}: login fail".format(ac_list[ac_sum])
        return False


def calc_level(pokemon_data):
    cpm = pokemon_data["cp_multiplier"]
    if cpm < 0.734:
        level = 58.35178527 * cpm * cpm - 2.838007664 * cpm + 0.8539209906
    else:
        level = 171.0112688 * cpm - 95.20425243
    level = (round(level) * 2) / 2.0
    return level


def telemon(target_lat, target_lng, trial=0):
    cell_ids = util.get_cell_ids(target_lat, target_lng)
    timestamps = [0,] * len(cell_ids)
    req = api.create_request()
    req.get_map_objects(latitude=target_lat, longitude=target_lng, since_timestamp_ms=timestamps, cell_id=cell_ids)
    response = req.call()
    cells = response['responses']['GET_MAP_OBJECTS']['map_cells']
    print 'Response dictionary:\n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(response))
    pkm_raw = []
    pkm = []
    for cell in cells:
        pkm_raw.extend(cell.get('catchable_pokemons', []))
    for i in pkm_raw:
        if i not in pkm:
            pkm.append(i)
    n = len(pkm)
    if n == 0 and trial < 4:
        trial += 1
        trial_count = "TRIAL: " + str(trial)
        print trial_count
        time.sleep(1)
        return telemon(target_lat, target_lng, trial)
    elif n == 0 and trial >= 4:
        return None
        pass
    return pkm


def check(msg, encounter_id, spawn_point_id, player_latitude, player_longitude, pkm_id, tth):
    encounter_response = api.encounter(encounter_id=encounter_id, spawn_point_id=spawn_point_id, player_latitude=player_latitude, player_longitude=player_longitude)
    print 'Response dictionary:\n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(encounter_response))
    time.sleep(1)
    #Disappear Time
    if str(tth) == '-1':
        tth = '>90s'
    else:
        tth = '{}s'.format(str(int(int(tth)/1000 - time.time())))

    iv_a = str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_attack', 0))
    iv_d = str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_defense', 0))
    iv_s = str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_stamina', 0))
    iv_percentage = str("{:.0f}".format(float(((int(iv_a) + int(iv_d) + int(iv_s)) * 100) / float(45))))
    mv_1 = str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['move_1'])
    mv_2 = str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['move_2'])
    pkm_lvl = str(calc_level(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']))
    cp = str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['cp'])


    pkm_n = pkm_hk.get(str(pkm_id)).encode('utf8')
    mv_1_n = pkm_mv.get(mv_1).encode('utf8')
    mv_2_n = pkm_mv.get(mv_2).encode('utf8')
    pkmid = str(pkm_id)

    form_l = ''
    if int(pkm_id) == 201:
        form = int(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['pokemon_display']['form'])
        form_l = 'A' if form is 1 else 'B' if form is 2 else 'C' if form is 3 else 'D' if form is 4 else 'E' if form is 5 else 'F' if form is 6 else 'G' if form is 7 else 'H' if form is 8 else 'I' if form is 9 else 'J' if form is 10 else 'K' if form is 11 else 'L' if form is 12 else 'M' if form is 13 else 'N' if form is 14 else 'O' if form is 15 else 'P' if form is 16 else 'Q' if form is 17 else 'R' if form is 18 else 'S' if form is 19 else 'T' if form is 20 else 'U' if form is 21 else 'V' if form is 22 else 'W' if form is 23 else 'X' if form is 24 else 'Y' if form is 25 else 'Z' if form is 26 else '!' if form is 27 else '?' if form is 28 else ''

    current_time = str(datetime.now(timezone('Asia/Hong_Kong')).strftime('%Y-%m-%d %H:%M:%S'))

    #Send Results to Telegram
    SendM = text_style
    for i in re.findall('<([^<>]+)>',text_style):
        SendM = SendM.replace(('<'+i+'>'), locals()[i])

    bot.sendMessage(msg['chat']['id'], SendM, parse_mode = 'html')

    #A logging on telegram ()for owner
    try:
        SendM += '\n\n@' + str(msg['chat']['username'])
    except:
        pass     
    SendM += "\n\n"+ str(ac_list[(ac_sum-1)]) + '\nHash_Remaining: ' + str(HashServer.status['remaining'])
    bot.sendMessage(own_id, SendM, parse_mode = 'html')
    return True


def main(msg, target_lat, target_lng, alt, pkm_id):
    global home_lat
    global home_lng
    sum = 0
    pkm_confirmed = []

    api.activate_hash_server(hash_key)
    api.set_position(target_lat, target_lng, alt)
    Login = login()
    #if Login is not True:
    #    SendM = login_fail_text
    #    logger.error('[login failed]')
    #    bot.sendMessage(msg['chat']['id'], SendM, parse_mode = 'html')
    #    SendM += "\n{}".format(str(ac_list[(ac_sum-1)]))
    #    bot.sendMessage(own_id, SendM, parse_mode = 'html')
    #    pass
    Telemon = telemon(target_lat, target_lng)
    print ac_list[(ac_sum-1)]
    if Telemon is None:
        print "SCAN FAILED: SPEEDLOCK"
        SendM = speed_lock_text
        bot.sendMessage(msg['chat']['id'], SendM, parse_mode = 'html')
        SendM += "\n"+ str(ac_list[(ac_sum-1)]) 
        bot.sendMessage(own_id,SendM, parse_mode = 'html')
        print "End"
        print "Finding..."
   

    for i in Telemon:
        if i.get('pokemon_id') == int(pkm_id):
            pkm_confirmed.append(i)

    if len(pkm_confirmed) == 0:
        SendM = not_found_text
        bot.sendMessage(msg['chat']['id'], SendM, parse_mode = 'html')
        SendM += "\n"+ str(ac_list[(ac_sum-1)])
        bot.sendMessage(own_id, SendM, parse_mode = 'html')
        print "NOT FOUND"

    for i in pkm_confirmed:
        check(msg, i.get('encounter_id'), i.get('spawn_point_id'), target_lat, target_lng, pkm_id, i.get('expiration_timestamp_ms'))
        sum += 1

    api.set_position(home_lat, home_lng, alt)


def check_iv_cp(msg):
    global ac_sum
    if "reply_to_message" in msg and 'location' in msg['reply_to_message'] and 'text' in msg and msg['text'].startswith('/cp'):
        cmd = msg['text'].split(' ')
        target_lat = float(msg['reply_to_message']['location']['latitude'])
        target_lng = float(msg['reply_to_message']['location']['longitude'])
        bot.sendMessage(msg['chat']['id'], message_recieved_text, parse_mode = 'html')
        if int(target_lat) > 22 or int(target_lat) < 22 or int(target_lng) > 114 or int(target_lng) < 113:
            bot.sendMessage(msg['chat']['id'], not_in_range_text, parse_mode = 'html')
            pass
        else:
            print "Finding..."
            Main = main(msg, target_lat, target_lng, alt, int(cmd[1]))
#----------#
