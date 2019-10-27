import json

class Team:
    def __init__(self, run_data):
        self.date = run_data["date"]
        self.ranking = run_data["ranking"]
        self.duration = run_data["duration"]
        self.level = run_data["level"]
        self.members = run_data["members"]

    def _eq_(self, other):
        if other._player_id_sum_() != self._player_id_sum_():
            return False
        return True
    
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
    def __init__(self, team, count):
        self.count = count
        self.Team = vars(team)

    def __eq__(self, value):
        return self.Team.__eq__(value)


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
    #runs = set(leaderboards) #remove duplicates
    runs = leaderboards
    possible_teams = list()
    for i in range(len(runs)):
        group = Mgroup(runs[i], i)
        for j in range(i+1, len(runs)):
            if is_possible_team(runs[i].members, runs[j].members):
                group.count += 1
        if group.count > 1:
            possible_teams.append(group)
    return possible_teams

def get_possible_teams(leaderboards, teams):
    if len(leaderboards) < 2:
        return
    
    current_run = leaderboards[0]
    not_equal_run = lambda x: not is_possible_team(current_run.members, x.members)
    left_runs = list(filter(not_equal_run, leaderboards))

    teams.append(current_run)
    get_possible_teams(left_runs, teams)




if __name__ == "__main__":
   pass