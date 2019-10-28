import json

class Team:
    def __init__(self, date, ranking, duration, level, members):
        self.date = date
        self.ranking = ranking
        self.duration = duration
        self.level = level
        self.members = members

    @classmethod
    def fromAdaptor(cls, team: 'dict', model: 'dict') -> "Team":
        team_data = {}
        for key in model.keys():
            team_data[key] = team[model[key]]

        return cls.fromDictionary(team_data)


    @classmethod
    def fromDictionary(cls, team) -> "Team":
        return cls(
            date     = team["date"], 
            ranking  = team["ranking"], 
            duration = team["duration"], 
            level    = team["level"], 
            members  = team["members"])

    def __eq__(self, other):
        first_group = self.members
        second_group = other.members
        member_count = 0
        for member in first_group:
            for other_member in second_group:
                if member["profile"]["id"] == other_member["profile"][id]:
                    member_count += 1
                    continue

        return member_count > 3
        
    
    def __ne__(self,other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.level < other.level

    def __gt__(self,other):
        return self.level > other.level

class TeamRepo:
    def __init__(self, teams: "list"):
        self.runs = teams

    @classmethod
    def fromJsonFile(cls, path):
        with open(path, "r") as f:
            repo_data = json.load(f)
            repo_data = map(lambda x: Team.fromDictionary(x), repo_data)
            return cls(list(repo_data))
        
    def writeJson(self, file: "str"):
        with open(file, "w+") as f:
            team_data = map(lambda x: vars(x), self.runs)
            json.dump(list(team_data), f, indent=3)
    
    def __len__(self):
        return len(self.runs)

    def remove_possible_pugs(self):
        groups = []
        for i in range(len(self.runs)):
            group_count= 0
            for j in range(i + 1, len(self.runs)):
                if self.runs[i] == self.runs[j]:
                    group_count += 1
            if group_count > 2 and self.runs[i] not in groups:
                groups.append(self.runs)
        self.runs = groups
    
if __name__ == "__main__":
   pass