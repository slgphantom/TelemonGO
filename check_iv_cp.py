# encoding=utf8

import configparser
import json

#import for telegram
import sys
import time
import telepot

#import for pgoapi
from pgoapi import PGoApi
from pgoapi.hash_server import HashServer
from pgoapi import utilities as util

from pprint import PrettyPrinter
from random import uniform

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

Account_ACCUM = 0
place = None

#Chinese Pokemon & Moves Name

pkm_hk = json.load('pkm.json')
pkm_mv = json.load('pkm_mv.json')

# Configuration loading time

config = configparser.ConfigParser() # Load configuration parser
config.read('config.ini') # reads configuration file

allowed_list = json.loads(config.DEFAULT.Allowed_List) # reads json from configuration file

accounts = json.load('accounts.json') # reads username and password from json file
usernames = [] # List of usernames

for username in accounts:
    usernames.append(username) # append username into usernames array

# usernames: to replace "ac_sum" (Assuming ac_sum is to be used as a tracker of what account is being used at the moment.)

# Calculate Pokemon Level
def calc_level(pokemon_data):
    cpm = pokemon_data["cp_multiplier"]
    if cpm < 0.734:
        level = 58.35178527 * cpm * cpm - 2.838007664 * cpm + 0.8539209906
    else:
        level = 171.0112688 * cpm - 95.20425243
    level = (round(level) * 2) / 2.0
    return level

#Main Handler

def handle(msg):

    cmd = msg['text'].split(' ')

    pkm_id = int(cmd[1])
    pkm_raw = []
    pkm = []
    alt = uniform(0.0, 70.0)
    skip = 0
    trial = 0
    sum = 0
    pkm_confirmed = []

    #Access Control
    if msg['chat']['id'] in allowed_list:
        if "reply_to_message" in msg and 'location' in msg['reply_to_message'] and 'text' in msg and msg['text'][:3] == '/cp':

            def login():

                try:
                    #Support ptc account only

                    api.login('ptc', usernames[Account_ACCUM], password)
                    Account_ACCUM += 1

                    if Account_ACCUM == len(usernames): # if accumulator is at the end of the list,
                        Account_ACCUM = 0 # go back to 0

                    return

                except:
                    # if login failed, then directly send error message to telegram + re-run main()

                    SendM = "Login唔到wo" + "\n" + "嚟多次！" # NOTE: Change to "LET ME TRY AGAIN!" because re-run main()
                    logger.error('[login failed]')
                    bot.sendMessage(msg['chat']['id'], SendM)

                    Account_ACCUM += 1

                    return main()

            def telemon():

                cell_ids = util.get_cell_ids(target_lat, target_lng)
                timestamps = [0,] * len(cell_ids)
                req = api.create_request()
                req.get_map_objects(latitude = target_lat, longitude = target_lng, since_timestamp_ms = timestamps, cell_id = cell_ids)
                response = req.call()
                cells = response['responses']['GET_MAP_OBJECTS']['map_cells']
                print('Response dictionary:\n\r{}'.format(PrettyPrinter(indent=4).pformat(response)))


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
                    return telemon() # try again
                return

            def check():
                try:
                    encounter_response = api.encounter( encounter_id = pkm_confirmed[sum].get('encounter_id'), spawn_point_id = str(pkm_confirmed[sum].get('spawn_point_id')), player_latitude = target_lat, player_longitude = target_lng)
                    print('Response dictionary:\n\r{}'.format(PrettyPrinter(indent=4).pformat(encounter_response)))
                    time.sleep(1)
                    tth = pkm_confirmed[sum].get('expiration_timestamp_ms')

                    #Disappear Time
                    if str(tth) == '-1':
                        tth = '\n\n剩餘: ' + '>90s'
                    else:
                        tth = '\n\n剩餘: ' + str(int(int(pkm_confirmed[sum].get('expiration_timestamp_ms'))/1000 - time.time())) + 's'

                    iv_a = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_attack', 0)
                    iv_d = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_defense', 0)
                    iv_s = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_stamina', 0)
                    iv_0 = "{:.0f}".format(float(((int(iv_a) + int(iv_d) + int(iv_s)) * 100) / float(45)))
                    mv_1 = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['move_1']
                    mv_2 = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['move_2']
                    pkm_lvl = calc_level(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'])


                    pkm_n = pkm_hk.get(str(pkm_id))
                    mv_1_n = pkm_mv.get(str(mv_1))
                    mv_2_n = pkm_mv.get(str(mv_2))


                    #Send Results to Telegram
                    SendM = '#'+ str(pkm_n) + '  (' + str(iv_0) + '%)\n\n30+:\nIV: ' + str(iv_a) + '  |  ' + str(iv_d) + '  |  ' + str(iv_s) + '\nMV: ' + str(mv_1_n) + '  |  ' + str(mv_2_n) + '\nCP: ' + str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['cp']) + '\nLVL: ' + str(pkm_lvl)

                    #Unown Form
                    if int(pkm_id) == 201:

                        unown_ltr = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '?']

                        form = int(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['pokemon_display']['form'])

                        try:
                            form_l = unown_ltr[form]
                        except IndexError:
                            form_l = unown_ltr[0]

                        SendM = SendM + "\nLetter: " + form_l

                    SendM += tth

                    print SendM # debug message TODO: put it in a logger.

                    bot.sendMessage(msg['chat']['id'],SendM)

                    #A logging on telegram ()for owner
                    try:
                        SendM += '\n\n@' + str(msg['chat']['username'])
                    except:
                        pass

                    SendM += "\n\n" + str(accounts[Account_ACCUM-1]) + '\nHash_Remaining: ' + str(HashServer.status['remaining'])
                    bot.sendMessage(own_id,SendM)
                    return True

                except:
                    return False

            try:

                bot.sendMessage(msg['chat']['id'],"收到")

                target_lat = float(msg['reply_to_message']['location']['latitude'])
                target_lng = float(msg['reply_to_message']['location']['longitude'])

                if config.Restriction.lat == '' and config.Restriction.lng == '':
                    pass
                elif int(target_lat) < config.RangeRestriction.latmin or int(target_lat) > config.RangeRestriction.latmax or int(target_lng) < config.RangeRestriction.lngmin or int(target_lng) > config.RangeRestriction.lngmax:
                    bot.sendMessage(msg['chat']['id'], "唔支持國際航班")
                    return place is False
                    pass

                print "搵緊..."


                def main():
                    api.activate_hash_server(config.Hash_Key)
                    api.set_position(target_lat, target_lng, alt)

                    login()
                    telemon()

                    print accounts[Account_ACCUM-1]

                    if place is False:
                        pass

                    if trial >= 4:
                        print "SCAN FAILED: SPEEDLOCK"
                        SendM = "SPEEDLOCK咗，嚟多次！"
                        bot.sendMessage(msg['chat']['id'],SendM)

                        SendM += "\n"+ str(accounts[Account_ACCUM-1])
                        bot.sendMessage(own_id,SendM)

                        print "End"
                        pass
                        print "搵緊..."

                    n = len(pkm)

                    for i in pkm:
                        if i.get('pokemon_id') == int(pkm_id):
                            pkm_confirmed.append(i)

                    if len(pkm_confirmed) == 0:
                        SendM = "搵唔到wo\n有人搞事？？" + "\n" + "----------完----------"
                        bot.sendMessage(msg['chat']['id'],SendM)

                        SendM += "\n"+ str(accounts[Account_ACCUM-1])
                        bot.sendMessage(own_id,SendM)

                        print "NOT FOUND"

                    for i in pkm_confirmed:
                        check()
                        sum += 1

                    api.set_position(config.Location.lat, config.Location.lng, alt) # Go Home

                main()

            except Exception,e:
                SendM = "出事啦" + "\n" + "----------完----------"
                logger.error(str(e))
                bot.sendMessage(msg['chat']['id'], SendM)

                SendM += "\n"+ str(accounts[Account_ACCUM-1])
                bot.sendMessage(own_id,SendM)

        elif "reply_to_message" in msg and 'location' in msg['reply_to_message'] and 'text' in msg and msg['text'][:4] == '/gps':
            lat = float(msg['reply_to_message']['location']['latitude'])
            lng = float(msg['reply_to_message']['location']['longitude'])
            f = urlopen('https://maps.googleapis.com/maps/api/staticmap?zoom=17&size=512x512&maptype=hybrid&markers=color:red|' + str(lat) + ',' + str(lng))
            bot.sendPhoto(msg['chat']['id'],f)

        elif 'text' in msg and msg['text'][:4] == '/map':
            try:
                location = msg['text'].split(' ')
                bot.sendLocation(msg['chat']['id'], location[1], location[2])
            except:
                bot.sendMessage(msg['chat']['id'], "打 /map <lat> <lng>，獲得地圖一份")



bot.message_loop({'chat': handle})
print('Listening ...')

while True:
    time.sleep(10)
