import curses
import random
from curses import wrapper

class Snake:
    def __init__(self):
        self.current_direction = 1
        self.body = [(10,11), (10, 12),(10,13)]

    def draw(self, win):
        win.clear()
        for v, h in self.body:
            win.addch(v, h, curses.ACS_PI)
    
    def move(self):
        self.body = self.body[1:]
        k, v = self.body[-1]
        #move up
        if self.current_direction == 1:
            self.append_node((k - 1, v))
        #move right
        if self.current_direction == 2:
            self.append_node((k, v + 1))
        #move down
        if self.current_direction == 3:
            self.append_node((k + 1, v))
        #move left
        if self.current_direction == 4:
            self.append_node((k, v -1))

    def append_node(self, node):
        if node in self.body:
            raise Exception("YOU DIE")
        else:
            self.body.append(node)

    def head(self):
        return self.body[-1]
    def eat(self):
        k, v = self.body[0]
        queue = tuple()
        if self.current_direction == 1:
            queue = (k + 1, v)
        if self.current_direction == 2:
            queue = (k, v - 1)
        if self.current_direction == 3:
            queue = (k -1, v)
        if self.current_direction == 4:
            queue = (k, v + 1)
        self.body.insert(0, queue)

class Game:
    def __init__(self, props):
        self.props = props
        self.Snake = Snake()
        self.food = (10, 10)
        wrapper(self.main)
    def main(self, win):
        curses.curs_set(0)
        window = win.subwin(*self.props["window_size"])
        window.keypad(1)
        window.timeout(self.props["timeout"])
        while True:
            self.game_tick(window)
    
    def game_tick(self, window):
        window.box()
        self.Snake.move()
        key = window.getch()
        direction_keys = "wdsa"
        if key == curses.KEY_DOWN:
            curses.flash()
        if key == curses.KEY_UP:
            curses.endwin()
            quit()
        if key in [119, 100, 115, 97]:
            self.Snake.current_direction = direction_keys.index(chr(key)) +1 
        self.Snake.draw(window)
        window.addch(*self.food, curses.ACS_PI)

        if self.Snake.head() == self.food:
            self.gen_food()
            self.Snake.eat()
    
    def gen_food(self):
        x = random.randint(6, 30)
        y = random.randint(6, 30)
        self.food = (x,y)


if __name__ == "__main__":
    game_props = {
        "window_size": (40, 90, 0, 0),
        "timeout": 120
    }

    Game(game_props)