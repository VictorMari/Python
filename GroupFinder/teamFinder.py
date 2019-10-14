import json

class Team:
    def __init__(self, run_data):
        self.date = run_data["completed_timestamp"]
        self.ranking = run_data["ranking"]
        self.members = run_data["members"]
        self.duration = run_data["duration"]
        self.level = run_data["keystone_level"]

    def _eq_(self, other):
        if other.date != self.date:
            return False
        if other.ranking != self.ranking:
            return False
        if other._player_id_sum_() != self._player_id_sum_():
            return False
    
    def _player_id_sum_(self):
        s = 0
        for player in self.members:
            s += player["profile"]["id"]
        return s

    def _lt_(self, other):
        return self.level < other.level

    def _gt_(self,other):
        return self.level > other.level



class Mgroup:
    def __init__(self, team, Id):
        self.count = 1
        self.Team = team
        self.id = Id


def read_player_data():
    with open("players.json", "r") as f:
        js = json.load(f)
        return js

def is_possible_team(group1, group2):
    matches = 0
    for player in group1:
        player_name = player["profile"]["id"]
        for member in group2:
            member_name = member["profile"]["id"]
            if player_name == member_name:
                matches += 1
    return matches >= 4

def aggregate_teams(leaderboards):
    runs = set(leaderboards) #remvoe duplicates
    runs = list(runs)
    possible_teams = list()
    for i in range(len(runs)):
        group = Mgroup(runs[i], i)
        for j in range(i+1, len(runs)):
            if is_possible_team(runs[i].members, runs[j].members):
                group.count += 1
        if group.count > 1:
            possible_teams.append(group)

def __aggregator__(groups):
    hordes = filter(lambda x: x["keystone_level"] >= 15 and x["members"][0]["faction"]["type"] == "HORDE", groups)
    hordes = map(lambda x: Team(x), hordes)
    return list(hordes)

def old_main():
    runs = read_player_data()
    possible_teams = list()
    for i in range(len(runs)):
        team = {"id": i, "count": 0, "members": runs[i]}
        for j in range(i+1, len(runs)):
            if is_possible_team(runs[i], runs[j]):
                team["count"] += 1
        if team["count"] > 0:
            possible_teams.append(team)
    
    with open("possible_teams.json", "w+") as f:
        json_data = json.dumps(possible_teams, indent=3)
        f.write(json_data)
    
    print(len(possible_teams))


if __name__ == "__main__":
    with open("players.json", "r") as f:
        response = json.load(f)
        response = __aggregator__(response)
        response = map(lambda x: vars(x), response)
        #print(json.dumps(list(response)))
        with open("test.json", "w+") as f:
            f.write(json.dumps(list(response)))