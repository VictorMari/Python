import random

class Dice:
    def __init__(self):
        self.DiceSet = [random.randint(1,6) for i in range(5)]
    
    def __repr__(self):
        return repr(self.DiceSet)

    def reroll(self, *args):
        if len(args) > len(self.DiceSet):
            raise IndexError

        for ar in args:
            self.DiceSet[ar] = random.randint(1,6)
    
class PlayerScoreBoard:
    def __init__(self):
        self.current_category = 0
        self.remaining_categories = set(range(1,14))
        self.grand_total = 0
        self.upper_total = 0
        self.lower_total = 0

    def __repr__(self):
        return "Upper Half total: %d \nLower Half total: %d\n" % (self.upper_total, self.lower_total)

    def calculate_scores(self, rolls, category):
        self.rolls = rolls
        self.remaining_categories.remove(category)
        self.current_category = category
        
        if self.__isUpper__():
            self.upper_total += self.__getTotalMatchingDice__()
        else:
            self.lower_total += self.__getCurrentCategoryScore__()


    def __getCurrentCategoryScore__(self):
        helpers = self.__scoreHelpers__()
        return helpers[self.current_category - 7]()

    def __getTotalMatchingDice__(self):
        total_dices = filter(lambda x: x == self.current_category, self.rolls)
        return sum(total_dices)

    def __isUpper__(self):
        return self.current_category in range(1,7)
    
    def __scoreHelpers__(self):
        def findRepeats():
            combinations = [0] * 7
            for roll in self.rolls:
                combinations[roll] += 1
            return combinations

        def threeOfKind():
            combinations = findRepeats()
            if max(combinations) >= 3:
                return sum(self.rolls)
            return 0

        def fourOfKind():
            combinations = findRepeats()
            if max(combinations) >= 4:
                return sum(self.rolls)
            return 0

        def fullHouse():
            combinations = findRepeats()
            if 2 in combinations and 3 in combinations:
                return 25
            return 0

        def smallStraigh():
            sets = [set(range(1,5)),set(range(2,6)),set(range(3,7))]
            for s in sets:
                if s.issubset(self.rolls):
                    return 30
            return 0

        def largeStraigh():
            if set(range(1,6)).issubset(self.rolls) or set(range(2,7)).issubset(self.rolls):
                return 40
            return 0

        def yahtzee():
            combinations = findRepeats()
            return 50 if max(combinations) == 5 else 0
        
        def chance():
            return sum(self.rolls)
        category_functions = [threeOfKind, fourOfKind, fullHouse, smallStraigh, largeStraigh, yahtzee, chance]
        return category_functions

class Game:
    def __init__(self):
        total_players = input("Enter ammount of players")
        total_players = int(total_players)
        score_boards = [PlayerScoreBoard()] * total_players
        player = 1
        for i in range(1,14):
            for n in score_boards:
                print("Round %d, its player %d turn" % (i,player))
                input("Press a key to roll")
                self.playRound()
                player += 1
            player = 1

    def playRound(self):
        roll = Dice()
        
        round_roll = 1
        while round_roll < 4:
            print(roll)
            keeps = input("Enter which dice to keep or press enter to stop")
            keeps = keeps.split(" ")
            keeps = map(lambda x: int(x), keeps)
            keeps = list(keeps)
            if len(keeps) == 0:
                break
            
            roll.reroll(*keeps)
            round_roll += 1
Game()

