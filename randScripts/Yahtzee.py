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
        self.grand_total += self.upper_total + self.lower_total
    def __int__(self):
        return self.grand_total

    def __gt__(self, other):
        return self.__int__() > int(other)

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
        total_players = self.getUserInput({
            "messege": "Enter number of players",
            "error": "Input can´t be negative"},
            lambda x: int(x) < 1)
        total_players = int(total_players)
        score_boards = [0] * total_players
        score_boards = map(lambda x: PlayerScoreBoard(), score_boards)
        score_boards = list(score_boards)
        player = 1
        for i in range(1,2):
            for n in score_boards:
                print("Round %d, its player %d turn" % (i,player))
                input("Press a key to roll")
                self.playRound()
                n.calculate_scores(self.rolls, self.category)
                print(n)
                player += 1
            player = 1
        winner_score  = max(score_boards)
        player_number = score_boards.index(winner_score)
        print(f'Winner is Player{player_number}\n{winner_score}') 
        

    def playRound(self):
        roll = Dice()
        category = self.getUserInput({
            "messege": "Enter round category",
            "error": "Category was out of range"
        }, self.__checkCategory__)
        round_roll = 1
        while round_roll < 3:
            print(roll)
            keeps = self.getUserInput({
                "messege": "Enter which dice to reroll",
                "error": "Dice numbers were out of range"
            }, self.__checkRolls__)
            if len(keeps) == 0:
                break
            keeps = keeps.split(" ")
            keeps = map(lambda x: int(x), keeps)
            keeps = list(keeps)
            roll.reroll(*keeps)
            round_roll += 1

        print(roll)
        self.category = int(category)
        self.rolls = roll.DiceSet
    
    def getUserInput(self, output_info, validation):
            while True:
                userInput = input(output_info["messege"])
                try:
                    if len(userInput) == 0:
                        print("Input can not be empty")
                    if validation(userInput):
                        print(output_info["error"])
                    else:
                        break
                except ValueError:
                    print("Input was NaN")
            return userInput
    
    def __checkCategory__(self, uInput):
        category = int(uInput)
        return category < 1 or category > 13 

    def __checkRolls__(self, uInput):
        if len(uInput) == 0:
            return False
        for dice in uInput.split(" "):
            if int(dice) < 0 or int(dice) > 4:
                return True
        return False


if __name__ == '__main__':
    Game()

