
import datetime
from Combat_log_event_table import event_data

"""
11/9 04:10:25.270  SPELL_INTERRUPT,Player-1603-09803D48,"Ловитар-Корольлич",0x512,0x0,Creature-0-1631-1877-14582-134990-0000C62E1D,"Diablo de polvo cargada",0xa48,0x0,116705,"Golpe de mano de lanza",0x1,265968,"Oleada de sanación",1
11/9 04:10:25.667  SPELL_DAMAGE,Player-1379-07C27DCA,"Baltisito-Sanguino",0x511,0x0,Creature-0-1631-1877-14582-134600-0001C62E1D,"Tirador barrearena",0xa48,0x0,300917,"Juicio de la tormenta",0x8,Creature-0-1631-1877-14582-134600-0001C62E1D,0000000000000000,1154574,1304246,0,0,2700,0,1,0,0,0,3233.33,3148.70,1038,3.0121,120,7157,3578,-1,8,0,0,0,1,nil,nil
"""

testLine = '11/9 04:10:25.270  SPELL_INTERRUPT,Player-1603-09803D48,"Ловитар-Корольлич",0x512,0x0,Creature-0-1631-1877-14582-134990-0000C62E1D,"Diablo de polvo cargada",0xa48,0x0,116705,"Golpe de mano de lanza",0x1,265968,"Oleada de sanación",1'
damage_test = '11/9 04:10:25.667  SPELL_DAMAGE,Player-1379-07C27DCA,"Baltisito-Sanguino",0x511,0x0,Creature-0-1631-1877-14582-134600-0001C62E1D,"Tirador barrearena",0xa48,0x0,300917,"Juicio de la tormenta",0x8,Creature-0-1631-1877-14582-134600-0001C62E1D,0000000000000000,1154574,1304246,0,0,2700,0,1,0,0,0,3233.33,3148.70,1038,3.0121,120,7157,3578,-1,8,0,0,0,1,nil,nil'

def splitEvent(log_line):
    log_line.strip("")
    event_data = log_line.split(",")
    date, time, event = event_data[0].split()

    parsed_date = datetime.datetime.strptime(f"{date} {time}", "%d/%m %H:%M:%S.%f")
    return_arr = [parsed_date, event]
    return_arr.extend(event_data[1:])
    return return_arr

log = splitEvent(testLine)
#print(log)


def get_event_params(event: "str") -> "dict":
    for event_prefix in event_data["Preffixes"].keys():
        if event.find(event_prefix) >= 0:
            for event_suffix in event_data["Suffixes"].keys():
                if event.find(event_suffix) >= 0:
                    return [
                        *event_data["Params"]["Base_event_params"],
                        *event_data["Preffixes"][event_prefix], 
                        *event_data["Params"]["Advanced_params"],
                        *event_data["Suffixes"][event_suffix]]

def parse_combat_event(log: "str"):
    log_arguments = splitEvent(log)
    event_parameters = get_event_params(log_arguments[1])
    parsed_event = dict(zip(event_parameters, log_arguments))
    return parsed_event

print(parse_combat_event(damage_test))