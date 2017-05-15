# encoding=utf8  

#import for telegram
import sys
import time
import telepot
import requests
from urllib import urlopen
import ConfigParser
import json

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

#config
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
bot = telepot.Bot(bot_token)

ac_sum = 0
place = None

alt = random.uniform(0.0, 70.0)

with open('pkmn_hk.json') as json_name:
    pkm_hk = json.load(json_name)
with open('pkm_mv.json') as json_mv:
    pkm_mv = json.load(json_mv)

def calc_level(pokemon_data):
    cpm = pokemon_data["cp_multiplier"]
    if cpm < 0.734:
        level = 58.35178527 * cpm * cpm - 2.838007664 * cpm + 0.8539209906
    else:
        level = 171.0112688 * cpm - 95.20425243
    level = (round(level) * 2) / 2.0
    return level


def check_iv_cp(msg):
    global ac_sum

    #Access Control
    if 1:
        if "reply_to_message" in msg and 'location' in msg['reply_to_message'] and 'text' in msg and msg['text'][:3] == '/cp':
            cmd = msg['text'].split(' ')
            LOGIN = None
            def login():
                try:
                    global ac_sum
                    #Support ptc account onlt
                    api.login('ptc', ac_list[ac_sum], pw_list[ac_sum])
                    ac_sum += 1
                    if ac_sum == len(ac_list):
                        ac_sum = 0
                        return LOGIN is True
                except:
                    print "login fail"
                    ac_sum += 1
                    return LOGIN is False
            try:
                global place
                global home_lat
                global home_lng
                bot.sendMessage(msg['chat']['id'],"收到")

                target_lat = float(msg['reply_to_message']['location']['latitude'])
                target_lng = float(msg['reply_to_message']['location']['longitude'])
                if int(target_lat) > 22 or int(target_lat) < 22 or int(target_lng) > 114 or int(target_lng) < 113:
                    bot.sendMessage(msg['chat']['id'], "唔支持國際航班")
                    return place is False
                    pass
                pkm_id = int(cmd[1])
                pkm_raw = []
                pkm = []
                alt = random.uniform(0.0, 70.0)
                global skip
                global trial
                global End
                skip = 0
                trial = 0
                print "搵緊..."
                

                def telemon():

                    cell_ids = util.get_cell_ids(target_lat, target_lng)
                    timestamps = [0,] * len(cell_ids)
                    req = api.create_request()
                    req.get_map_objects(latitude = target_lat, longitude = target_lng, since_timestamp_ms = timestamps, cell_id = cell_ids)
                    response = req.call()
                    cells = response['responses']['GET_MAP_OBJECTS']['map_cells']
                    print('Response dictionary:\n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(response)))


                    for cell in cells:
                        pkm_raw.extend(cell.get('catchable_pokemons', []))
                    for i in pkm_raw:
                        if i not in pkm:
                            pkm.append(i)
                    n = len(pkm)
                    global trial
                    if n == 0 and trial < 4:
                        trial += 1
                        trial_count = "TRIAL: " + str(trial)
                        print trial_count
                        time.sleep(1)
                        return telemon()
                    return



        

                def main():
                    api.activate_hash_server(hash_key)
                    api.set_position(target_lat, target_lng, alt)
                    login()
                    telemon()
                    global trial
                    global place
                    print ac_list[(ac_sum-1)] 
                    if place is False:
                        pass
                    if trial >= 4:
                        print "SCAN FAILED: SPEEDLOCK"
                        SendM = "SPEEDLOCK咗，嚟多次！" 
                        bot.sendMessage(msg['chat']['id'],SendM)
                        SendM += "\n"+ str(ac_list[(ac_sum-1)]) 
                        bot.sendMessage(own_id,SendM)
                        print "End"
                        pass
                        print "搵緊..."
                    n = len(pkm)

                    def check():
                        if 1:
                            encounter_response = api.encounter( encounter_id = pkm_confirmed[sum].get('encounter_id'), spawn_point_id = str(pkm_confirmed[sum].get('spawn_point_id')), player_latitude = target_lat, player_longitude = target_lng)
                            print('Response dictionary:\n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(encounter_response)))
                            
                            time.sleep(1)
                            tth = pkm_confirmed[sum].get('expiration_timestamp_ms')

                            #Disappear Time
                            if str(tth) == '-1':
                                tth = u'\n\n剩餘: ' + '>90s'
                            else:
                                tth = u'\n\n剩餘: ' + str(int(int(pkm_confirmed[sum].get('expiration_timestamp_ms'))/1000 - time.time())) + 's'

                            iv_a = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_attack', 0)
                            iv_d = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_defense', 0)
                            iv_s = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'].get('individual_stamina', 0)
                            iv_0 = "{:.0f}".format(float(((int(iv_a) + int(iv_d) + int(iv_s)) * 100) / float(45)))
                            mv_1 = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['move_1']
                            mv_2 = encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['move_2']
                            
                            pkm_cp = str(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['cp'])
                            pkm_lvl = calc_level(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data'])


                            pkm_n = pkm_hk.get(str(pkm_id))
                            mv_1_n = pkm_mv.get(str(mv_1))
                            mv_2_n = pkm_mv.get(str(mv_2))
                            
                            address = json.loads(requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s&language=zh_hk' % (target_lat,target_lng,target_lat,target_lng)).content)['destination_addresses'][0].encode('utf8')
                            map_link = 'http://maps.google.com/maps?q=' + str(target_lat) + ',' + str(target_lng)



                            #Send Results to Telegram
                            SendM = '#'+ pkm_n + '  (' + str(iv_0) + '%)\n' + address + '['+ '<a href="{0}">地圖</a>'.format(map_link) +']\n\n[30+]\nCP: ' + pkm_cp + '  (' + str(pkm_lvl) + ')\nIV: ' + str(iv_a) + '  |  ' + str(iv_d) + '  |  ' + str(iv_s) + '\nMV: ' + mv_1_n + '  |  ' + mv_2_n
                            #Unown Form
                            if int(pkm_id) == 201:
                                form = int(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['pokemon_display']['form'])
                                form_l = 'A' if form is 1 else 'B' if form is 2 else 'C' if form is 3 else 'D' if form is 4 else 'E' if form is 5 else 'F' if form is 6 else 'G' if form is 7 else 'H' if form is 8 else 'I' if form is 9 else 'J' if form is 10 else 'K' if form is 11 else 'L' if form is 12 else 'M' if form is 13 else 'N' if form is 14 else 'O' if form is 15 else 'P' if form is 16 else 'Q' if form is 17 else 'R' if form is 18 else 'S' if form is 19 else 'T' if form is 20 else 'U' if form is 21 else 'V' if form is 22 else 'W' if form is 23 else 'X' if form is 24 else 'Y' if form is 25 else 'Z' if form is 26 else '!' if form is 27 else '?' if form is 28 else '' #neutral
                                SendM = SendM + "\nLetter: " + str(form_l)
                            SendM += tth
                            bot.sendMessage(msg['chat']['id'],SendM)

                            #A logging on telegram ()for owner
                            try:
                                SendM += '\n\n@' + str(msg['chat']['username'])
                            except:
                                pass        
                            SendM += "\n\n"+ str(ac_list[(ac_sum-1)]) + '\nHash_Remaining: ' + str(HashServer.status['remaining'])
                            bot.sendMessage(own_id,SendM)
                            return True
                                            
                        """except:
                            return False"""


                    sum = 0
                    pkm_confirmed = []
                    
                    for i in pkm:
                        if i.get('pokemon_id') == int(pkm_id):
                            pkm_confirmed.append(i)

                    if len(pkm_confirmed) == 0:
                        SendM = "搵唔到wo\n有人搞事？？" + "\n" + "----------完----------"
                        bot.sendMessage(msg['chat']['id'],SendM)
                        SendM += "\n"+ str(ac_list[(ac_sum-1)]) 
                        bot.sendMessage(own_id,SendM)
                        print "NOT FOUND"

                    for i in pkm_confirmed:
                        check()
                        sum += 1

                    api.set_position(home_lat, home_lng, alt) 

                main()


            except Exception,e:
                if LOGIN is not True:
                    SendM = "Login唔到wo" + "\n" + "嚟多次！"
                    logger.error('[login failed]')
                    bot.sendMessage(msg['chat']['id'], SendM)
                    SendM += "\n"+ str(ac_list[(ac_sum-1)]) 
                    bot.sendMessage(own_id,SendM)
                    return main()
                else:
                    SendM = "出事啦" + "\n" + "----------完----------"
                    logger.error(str(e))
                    bot.sendMessage(msg['chat']['id'], SendM)
                    SendM += "\n"+ str(ac_list[(ac_sum-1)]) 
                bot.sendMessage(own_id,SendM)
                
def gps(msg):
    if "reply_to_message" in msg and 'location' in msg['reply_to_message'] and 'text' in msg and msg['text'][:4] == '/gps':
        lat = float(msg['reply_to_message']['location']['latitude'])
        lng = float(msg['reply_to_message']['location']['longitude'])
        f = urlopen('https://maps.googleapis.com/maps/api/staticmap?zoom=17&size=512x512&maptype=hybrid&markers=color:red|' + str(lat) + ',' + str(lng))
        bot.sendPhoto(msg['chat']['id'],f)
        

def show_map(msg):
    if 'text' in msg and msg['text'][:4] == '/map':
        try:
            location = msg['text'].split(' ')
            bot.sendLocation(msg['chat']['id'], location[1], location[2])
        except:
            bot.sendMessage(msg['chat']['id'], "打 /map <lat> <lng>，獲得地圖一份")
            
def wecatch(msg):
    if 'text' in msg and 'https://wecatchpokemon.cdstud.io/?' in msg['text']:
        info = re.search("(?P<url>https?://[^\s]+)", msg['text']).group("url").replace('https://wecatchpokemon.cdstud.io/?','')
        info = re.split('&|=', info)
        bot.sendLocation(msg['chat']['id'], info[1], info[3], reply_to_message_id=msg['message_id'])
