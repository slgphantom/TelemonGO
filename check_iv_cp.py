# encoding=utf8  

#import for telegram
import sys
import time
import telepot


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

#Chinese Pokemon & Moves Name
pkm_hk = {"1":"奇異種子","2":"奇異草","3":"奇異花","4":"小火龍","5":"火恐龍","6":"噴火龍","7":"車厘龜","8":"卡美龜","9":"水箭龜", "10":"綠毛蟲","11":"鐵甲蟲","12":"巴他蝶","13":"獨角蟲","14":"鐵殼蛹","15":"大針蜂","16":"波波","17":"比比鳥","18":"大比鳥","19":"小哥達","20":"哥達","21":"鬼雀","22":"魔雀","23":"阿柏蛇","24":"阿柏怪","25":"比卡超","26":"雷超","27":"穿山鼠","28":"穿山王","29":"尼美蘭","30":"尼美蘿","31":"尼美后","32":"尼多郎","33":"尼多利","34":"尼多王","35":"皮皮","36":"皮可斯","37":"六尾","38":"九尾","39":"波波球","40":"肥波球","41":"波音蝠","42":"大口蝠","43":"行路草","44":"怪味花","45":"霸王花","46":"蘑菇蟲","47":"巨菇蟲","48":"毛毛蟲","49":"魔魯風","50":"地鼠","51":"三頭地鼠","52":"喵喵怪","53":"高竇貓","54":"傻鴨","55":"高超鴨","56":"猴怪","57":"火爆猴","58":"護主犬","59":"奉神犬","60":"蚊香蝌蚪","61":"蚊香蛙","62":"大力蛙","63":"卡斯","64":"尤基納","65":"富迪","66":"鐵腕","67":"大力","68":"怪力","69":"喇叭芽","70":"口呆花","71":"大食花","72":"大眼水母","73":"多腳水母","74":"小拳石","75":"滾動石","76":"滾動岩","77":"小火馬","78":"烈焰馬","79":"小呆獸","80":"大呆獸","81":"小磁怪","82":"三合一磁怪","83":"火蔥鴨","84":"多多","85":"多多利","86":"小海獅","87":"白海獅","88":"爛泥怪","89":"爛泥獸","90":"貝殼怪","91":"鐵甲貝","92":"鬼斯","93":"鬼斯通","94":"耿鬼","95":"大岩蛇","96":"食夢獸","97":"催眠獸","98":"大鉗蟹","99":"巨鉗蟹", "100":"霹靂蛋","101":"雷霆蛋","102":"蛋蛋","103":"椰樹獸","104":"卡拉卡拉","105":"格拉格拉","106":"沙古拉","107":"比華拉","108":"大舌頭","109":"毒氣丸","110":"毒氣雙子","111":"鐵甲犀牛","112":"鐵甲暴龍","113":"吉利蛋","114":"長籐怪","115":"袋獸","116":"噴墨海馬","117":"飛刺海馬","118":"獨角金魚","119":"金魚王","120":"海星星","121":"寶石海星","122":"吸盤小丑","123":"飛天螳螂","124":"紅唇娃","125":"電擊獸","126":"鴨嘴火龍","127":"鉗刀甲蟲","128":"大隻牛","129":"鯉魚王","130":"鯉魚龍","131":"背背龍","132":"百變怪","133":"伊貝","134":"水伊貝","135":"雷伊貝","136":"火伊貝","137":"立方獸","138":"菊石獸","139":"多刺菊石獸","140":"萬年蟲","141":"鐮刀蟲","142":"化石飛龍","143":"卡比獸","144":"急凍鳥","145":"雷鳥","146":"火鳥","147":"迷你龍","148":"哈古龍","149":"啟暴龍","150":"超夢夢","151":"夢夢","152":"菊草葉","153":"月桂葉","154":"大菊花","155":"火球鼠","156":"火岩鼠","157":"火暴獸","158":"小鋸鱷","159":"藍鱷","160":"大力鱷","161":"尾立","162":"大尾立","163":"咕咕","164":"貓頭夜鷹","165":"芭瓢蟲","166":"安瓢蟲","167":"線球","168":"阿利多斯","169":"叉字蝠","170":"燈籠魚","171":"電燈怪","172":"比超","173":"皮寶寶","174":"小波球","175":"小刺蛋","176":"波克基古","177":"天然雀","178":"天然鳥","179":"咩利羊","180":"綿綿","181":"電龍","182":"美麗花","183":"瑪利露","184":"瑪利露麗","185":"胡說樹","186":"牛蛙君","187":"毽子草","188":"毽子花","189":"毽子綿","190":"長尾怪手","191":"向日種子","192":"向日花怪","193":"陽陽瑪","194":"烏波","195":"沼王","196":"太陽伊貝","197":"月伊貝","198":"黑暗鴉","199":"河馬王","200":"夢妖","201":"未知圖騰","202":"果然翁","203":"麒麟奇","204":"榛果球","205":"佛烈託斯","206":"土龍弟弟","207":"天蠍","208":"大鋼蛇","209":"布魯","210":"布魯皇","211":"千針魚","212":"巨鉗螳螂","213":"壺壺","214":"赫拉克羅斯","215":"狃拉","216":"熊寶寶","217":"圈圈熊","218":"熔岩蟲","219":"熔岩蝸牛","220":"小山豬","221":"長毛豬","222":"太陽珊瑚","223":"鐵炮魚","224":"章魚桶","225":"信使鳥","226":"巨翅飛魚","227":"盔甲鳥","228":"戴魯比","229":"黑魯加","230":"刺龍王","231":"小小象","232":"冬凡","233":"立方獸２","234":"驚角鹿","235":"圖圖犬","236":"巴爾郎","237":"柯波朗","238":"迷唇娃","239":"電擊怪","240":"小鴨嘴龍","241":"大奶罐","242":"幸福蛋","243":"雷公","244":"炎帝","245":"水君","246":"由基拉","247":"沙基拉","248":"班吉拉","249":"利基亞","250":"鳳凰","251":"雪拉比"}
pkm_mv = {"13": "Wrap","14": "Hyper Beam","16": "Dark Pulse","18": "Sludge","20": "Vice Grip","21": "Flame Wheel","22": "Megahorn","24": "Flamethrower","26": "Dig","28": "Cross Chop","30": "Psybeam","31": "Earthquake","32": "Stone Edge","33": "Ice Punch","34": "Heart Stamp","35": "Discharge","36": "Flash Cannon","38": "Drill Peck","39": "Ice Beam","40": "Blizzard","42": "Heat Wave","45": "Aerial Ace","46": "Drill Run","47": "Petal Blizzard","48": "Mega Drain","49": "Bug Buzz","50": "Poison Fang","51": "Night Slash","53": "Bubble Beam","54": "Submission","56": "Low Sweep","57": "Aqua Jet","58": "Aqua Tail","59": "Seed Bomb","60": "Psyshock","62": "Ancient Power","63": "Rock Tomb","64": "Rock Slide","65": "Power Gem","66": "Shadow Sneak","67": "Shadow Punch","69": "Ominous Wind","70": "Shadow Ball","72": "Magnet Bomb","74": "Iron Head","75": "Parabolic Charge","77": "Thunder Punch","78": "Thunder","79": "Thunderbolt","80": "Twister","82": "Dragon Pulse","83": "Dragon Claw","84": "Disarming Voice","85": "Draining Kiss","86": "Dazzling Gleam","87": "Moonblast","88": "Play Rough","89": "Cross Poison","90": "Sludge Bomb","91": "Sludge Wave","92": "Gunk Shot","94": "Bone Club","95": "Bulldoze","96": "Mud Bomb","99": "Signal Beam", "100": "X Scissor","101": "Flame Charge","102": "Flame Burst","103": "Fire Blast","104": "Brine","105": "Water Pulse","106": "Scald","107": "Hydro Pump","108": "Psychic","109": "Psystrike","111": "Icy Wind","114": "Giga Drain","115": "Fire Punch","116": "Solar Beam","117": "Leaf Blade","118": "Power Whip","121": "Air Cutter","122": "Hurricane","123": "Brick Break","125": "Swift","126": "Horn Attack","127": "Stomp","129": "Hyper Fang","131": "Body Slam","132": "Rest","133": "Struggle","134": "Scald (Blastoise)","135": "Hydro Pump (Blastoise)","136": "Wrap (Green)","137": "Wrap (Pink)","200": "Fury Cutter","201": "Bug Bite","202": "Bite","203": "Sucker Punch","204": "Dragon Breath","205": "Thunder Shock","206": "Spark","207": "Low Kick","208": "Karate Chop","209": "Ember","210": "Wing Attack","211": "Peck","212": "Lick","213": "Shadow Claw","214": "Vine Whip","215": "Razor Leaf","216": "Mud Shot","217": "Ice Shard","218": "Frost Breath","219": "Quick Attack","220": "Scratch","221": "Tackle","222": "Pound","223": "Cut","224": "Poison Jab","225": "Acid","226": "Psycho Cut","227": "Rock Throw","228": "Metal Claw","229": "Bullet Punch","230": "Water Gun","231": "Splash","233": "Mud Slap","234": "Zen Headbutt","235": "Confusion","236": "Poison Sting","237": "Bubble","238": "Feint Attack","239": "Steel Wing","240": "Fire Fang","241": "Rock Smash","242": "Transform","243": "Counter","244": "Powder Snow","245": "Close Combat","246": "Dynamic Punch","247": "Focus Blast","248": "Aurora Beam","249": "Charge Beam","250": "Volt Switch","251": "Wild Charge","252": "Zap Cannon","253": "Dragon Tail","254": "Avalanche","255": "Air Slash","256": "Brave Bird","257": "Sky Attack","258": "Sand Tomb","259": "Rock Blast","260": "Infestation","261": "Struggle Bug","262": "Silver Wind","263": "Astonish","264": "Hex","265": "Night Shade","266": "Iron Tail","267": "Gyro Ball","268": "Heavy Slam","269": "Fire Spin","270": "Overheat","271": "Bullet Seed","272": "Grass Knot","273": "Energy Ball","274": "Extrasensory","275": "Futuresight","276": "Mirror Coat","277": "Outrage","278": "Snarl","279": "Crunch","280": "Foul Play","281": "Hidden Power"}

#Calculate Pokemon Level
def calc_level(pokemon_data):
    cpm = pokemon_data["cp_multiplier"]
    if cpm < 0.734:
        level = 58.35178527 * cpm * cpm - 2.838007664 * cpm + 0.8539209906
    else:
        level = 171.0112688 * cpm - 95.20425243
    level = (round(level) * 2) / 2.0
    return level

#Main Function
def handle(msg):
    global ac_sum

    #Access Control
    if msg['chat']['id'] in allowed_list:
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
                        #return main()
                        print "End"
                        pass
                        print "搵緊..."
                    n = len(pkm)

                    def check():
                        try:
                            encounter_response = api.encounter( encounter_id = pkm_confirmed[sum].get('encounter_id'), spawn_point_id = str(pkm_confirmed[sum].get('spawn_point_id')), player_latitude = target_lat, player_longitude = target_lng)
                            print('Response dictionary:\n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(encounter_response)))
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
                                form = int(encounter_response['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['pokemon_display']['form'])
                                form_l = 'A' if form is 1 else 'B' if form is 2 else 'C' if form is 3 else 'D' if form is 4 else 'E' if form is 5 else 'F' if form is 6 else 'G' if form is 7 else 'H' if form is 8 else 'I' if form is 9 else 'J' if form is 10 else 'K' if form is 11 else 'L' if form is 12 else 'M' if form is 13 else 'N' if form is 14 else 'O' if form is 15 else 'P' if form is 16 else 'Q' if form is 17 else 'R' if form is 18 else 'S' if form is 19 else 'T' if form is 20 else 'U' if form is 21 else 'V' if form is 22 else 'W' if form is 23 else 'X' if form is 24 else 'Y' if form is 25 else 'Z' if form is 26 else '!' if form is 27 else '?' if form is 28 else '' #neutral
                                SendM = SendM + "\nLetter: " + str(form_l)
                            SendM += tth
                            print SendM
                            bot.sendMessage(msg['chat']['id'],SendM)

                            #A looging on telegram ()for owner
                            try:
                                SendM += '\n\n@' + str(msg['chat']['username'])
                            except:
                                pass        
                            SendM += "\n\n"+ str(ac_list[(ac_sum-1)]) + '\nHash_Remaining: ' + str(HashServer.status['remaining'])
                            bot.sendMessage(own_id,SendM)
                            return True
                                            
                        except:
                            return False


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

while 1:
    time.sleep(10)
