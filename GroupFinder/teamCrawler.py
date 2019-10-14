import requests
import json
from teamFinder import aggregate_teams
from teamFinder import *
# routes
""" 
    leader board  -> /data/wow/connected-realm/{server id}/mythic-leaderboard/{dungeon id}/period/{period id}?
    Server index  -> /data/wow/connected-realm/index 
    dungeon index -> /data/wow/mythic-keystone/dungeon/index
    period index  -> /data/wow/mythic-keystone/period/index
"""

# answer objects
""" 
    Connected server -> {"realms":[{id,name}]}
    Sanguino -> {"id": 1382}
    connected_sanguino -> {"id": 1379}
    current period = 719
"""

token = "EUudu6Y5mlFzeIJ3QfhU2F7qnvM40AJCb3"
host = "https://eu.api.blizzard.com"
server_index_route = "/data/wow/connected-realm/index"
period_index_route = "/data/wow/mythic-keystone/period/index"
dungeon_index_route = "/data/wow/mythic-keystone/dungeon/index"

headers = {"Authentication":token}
parameters = {
    "namespace": "dynamic-eu",
    "locale": "en-US",
    "access_token": token
}

def make_request(url, parameters):
    print(f"GET...{url}")
    response = requests.get(url, params=parameters, timeout=0.3)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error when processing endpoint {url} status: {response.status_code}")
        return False


def find_server(name):
    #requets list of servers
    route = f"{host}{server_index_route}"
    print(f"Requesting server indexes at {route}")
    servers = make_request(route, parameters)
    servers = map(lambda x: x["href"], servers["connected_realms"])
    servers = list(servers)
    print(f"Got: {len(servers)} total servers")

    #find argumen in servers
    print(f"Finding Sanguino coneected realms")
    for url in servers:
        realm_data = make_request(url, parameters)
        connected_realms = realm_data["realms"]
        connected_realms = filter(lambda r: r["slug"] == name, connected_realms)
        connected_realms = list(connected_realms)
        if len(connected_realms) > 0:
            return realm_data["id"]

def get_current_period():
    route = f"{host}{period_index_route}"
    print(f"Requesting current period index at {route}")
    indexes = make_request(route, parameters)
    return indexes["current_period"]["id"]

def get_dungeon_index():
    route = f"{host}{dungeon_index_route}"
    print(f"Requesting current dungeon index at {route}")
    indexes = make_request(route, parameters)
    indexes = map(lambda x: x["id"], indexes["dungeons"])
    return list(indexes)


def __aggregator__(groups):
    hordes = filter(lambda x: x["keystone_level"] >= 15 and x["members"][0]["faction"]["type"] == "HORDE", groups)
    hordes = map(lambda x: Team(x), hordes)
    return list(hordes)


def get_dungeon_leaderboards(realm_id):
    period = get_current_period()
    dungeon_id = get_dungeon_index()
    players = list()
    print("Requesting dungeon leader boards")
    for dungeon in dungeon_id:
        route = f"{host}/data/wow/connected-realm/{realm_id}/mythic-leaderboard/{dungeon}/period/{period}"
        leaders = make_request(route, parameters)
        members = __aggregator__(leaders["leading_groups"])
        players.extend(members)

    return players


if __name__ == "__main__":
    ply = get_dungeon_leaderboards(1379)

    with open("players.json", "w+") as f:
        json_data = json.dumps(ply, indent=3)
        f.write(json_data)    