
import datetime

"""
11/9 04:10:25.270  SPELL_INTERRUPT,Player-1603-09803D48,"Ловитар-Корольлич",0x512,0x0,Creature-0-1631-1877-14582-134990-0000C62E1D,"Diablo de polvo cargada",0xa48,0x0,116705,"Golpe de mano de lanza",0x1,265968,"Oleada de sanación",1
"""
testLine = '11/9 04:10:25.270  SPELL_INTERRUPT,Player-1603-09803D48,"Ловитар-Корольлич",0x512,0x0,Creature-0-1631-1877-14582-134990-0000C62E1D,"Diablo de polvo cargada",0xa48,0x0,116705,"Golpe de mano de lanza",0x1,265968,"Oleada de sanación",1'


def splitEvent(log_line):
    log_line.strip("")
    event_data = log_line.split(",")
    date, time, event = event_data[0].split()

    parsed_date = datetime.datetime.strptime(f"{date} {time}", "%d/%m %H:%M:%S.%f")
    return_arr = [parsed_date, event]
    return_arr.extend(event_data[1:])
    return return_arr


def constructEvent(line ,log: "dict") -> "dict":
    params = {}
    for param_name, param_index in log.items():
        params[param_name] = line[param_index]
    return params


log = splitEvent(testLine)
#print(log)

event_params = {
    "base_prefix_params": {"Spell_id":10, "Spell_name": 11, "Spell_school": 12},
    "Target_spell_params": {"Targe_spell_id": 13, "Target_spell_name": 14, "Target_spell_school": 15},
    "Target_spell_aura_params": {"Targe_spell_id": 13, "Target_spell_name": 14, "Target_spell_school": 15}, "Target_aura_type": 16,
    "Aura_params": {"Aura_type": 13, "Amount": 14},
    "Power_params": {"Amount": 13, "Power_type": 14, "Extra_amount": 15},
    "Damage_params": {
        "Amount":13,
        "Overkill": 14,
        "School": 16,
        "Resisted": 16,
        "Blocked": 17,
        "Absorbed": 18,
        "Critical": 19,
        "Glancing": 20,
        "Crushing": 21,
        "Is_off_hand": 22
    },
    "Missed": {"Misstype": 13, "Is_Off_Hand": 14, "Amount_missed": 15},
    "Heal": {"Amount": 13, "Over_healing": 14, "Absorbed": 15, "Critical": 16},
    "Energize": {"Amount": 13, "Over_Energize": 14, "Power_type": 15, "Alternate_power_type": 16},
    "Amount": {"Amount": 13},
    "Fail": {"Failed_type": 13},
    "Empty": {}
}

prefixes = {
    "SWING":          event_params["Empty"],
    "RANGE":          event_params["base_prefix_params"],
    "SPELL_PERIODIC": event_params["base_prefix_params"],
    "SPELL_BUILDING": event_params["base_prefix_params"],
    "SPELL":          event_params["base_prefix_params"],
    "ENVIRONMENTAL":  event_params["Empty"]
}

suffixes = {
    "DAMAGE":   event_params["Damage_params"],
    "MISSED":   event_params["Missed"],
    "HEAL":     event_params["Heal"],
    "ENERGIZE": event_params["Energize"],
    "DRAIN":    event_params["Power_params"],
    "INTERRUP": event_params["Target_spell_params"],
}

base_event = {
    "Time_stamp": 0,
    "Event": 1,
    "Source_GUID": 2,
    "Source_Name": 3,
    "Source_Flags": 4,
    "Source_Raid_Flags": 5,
    "Destination_GUID": 6, 
    "Destination_name": 7, 
    "Destination_Flags": 8,
    "Destination_raid_flags": 9}

def parseEvent(event: "str", Log: "List", event_params) -> "list":
    for prefix, params in prefixes.items():
        if event.find(prefix) >= 0:
            for arg_name, arg_index in params.items():
                event_params[arg_name] = Log[arg_index]
            break
    for suffix, params in suffixes.items():
        if event.find(suffix) >= 0:
            for arg_name, arg_index in params.items():
                event_params[arg_name] = Log[arg_index]


ev = constructEvent(log, base_event)
parseEvent(ev["Event"], log, ev)
print(ev)