event_parameters = {
    "base_prefix_params": ["Spell_id", "Spell_name", "Spell_school"],
    "Advanced_params": [
        "Unit_GUID", 
        "Owner_GUID", 
        "Current_HP", 
        "Max_HP", 
        "Attack_power", 
        "Spell_power", 
        "Armor", 
        "Resource_type", 
        "Current_resource", 
        "Max_resource",
        "Resource_cost",
        "Coord",
        "UI_map_id",
        "Facing"
    ],
    "Target_spell_params":      ["Targe_spell_id", "Target_spell_name", "Target_spell_school"],
    "Target_spell_aura_params": ["Targe_spell_id", "Target_spell_name", "Target_spell_school", "Target_aura_type"],
    "Aura_params":              ["Aura_type", "Amount"],
    "Power_params":             ["Amount", "Power_type", "Extra_amount"],
    "Damage_params": [
        "Amount",
        "Overkill",
        "School",
        "Resisted",
        "Blocked",
        "Absorbed",
        "Critical",
        "Glancing",
        "Crushing",
        "Is_off_hand"
    ],
    "Base_event_params":[
        "Time_stamp",
        "Event",
        "Source_GUID",
        "Source_Name",
        "Source_Flags",
        "Source_Raid_Flags",
        "Destination_GUID", 
        "Destination_name", 
        "Destination_Flags",
        "Destination_raid_flags"
    ],
    "Missed":   ["Misstype", "Is_Off_Hand", "Amount_missed"],
    "Heal":     ["Amount", "Over_healing", "Absorbed", "Critical"],
    "Energize": ["Amount", "Over_Energize", "Power_type", "Alternate_power_type"],
    "Amount":   ["Amount"],
    "Fail":     ["Failed_type"],
    "Empty": {},
}

Suffixes = {
    "DAMAGE":   event_parameters["Damage_params"],
    "MISSED":   event_parameters["Missed"],
    "HEAL":     event_parameters["Heal"],
    "ENERGIZE": event_parameters["Energize"],
    "DRAIN":    event_parameters["Power_params"],
    "INTERRUPT": event_parameters["Target_spell_params"],
}

Prefixes = {
    "SWING":          event_parameters["Empty"],
    "RANGE":          event_parameters["base_prefix_params"],
    "SPELL_PERIODIC": event_parameters["base_prefix_params"],
    "SPELL_BUILDING": event_parameters["base_prefix_params"],
    "SPELL":          event_parameters["base_prefix_params"],
    "ENVIRONMENTAL":  event_parameters["Empty"]
}

event_data = {
    "Params":    event_parameters,
    "Suffixes":  Suffixes,
    "Preffixes": Prefixes
}