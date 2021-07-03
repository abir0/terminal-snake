from random import randint
import time
import curses
from curses import textpad


def init_curses(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    stdscr.nodelay(1)
    stdscr.timeout(100) # timeout for key press

def make_food(box, snake):
    food = None
    while food is None:
        food = [randint(box[0][0] + 1, box[1][0] - 1), randint(box[0][1] + 1, box[1][1] - 1)]
        if food in snake:
            food = None
    return food

def update_high_score():
    try:
        with open('score.snake', 'r') as f:
            high_score = int(f.read().strip())
    except FileNotFoundError:
        with open('score.snake', 'w') as f:
            f.write('0')
            high_score = 0
    return high_score

def play_game(stdscr):
    init_curses(stdscr)

    # Create the gamebox
    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh-3, sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    # Create score
    score = 0
    score_msg = 'Score: {}'.format(score)
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(2, 4, score_msg)
    stdscr.attroff(curses.color_pair(2))

    # Create the snake with 3 blocks
    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    dir = curses.KEY_RIGHT  # initial moving direction
    snake_block = '✱'

    for y, x in snake:
        stdscr.addstr(y, x, snake_block)

    # Make snake food
    food = make_food(box, snake)
    food_block = '@'
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(food[0], food[1], food_block)
    stdscr.attroff(curses.color_pair(1))

    while True:
        key = stdscr.getch()
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            dir = key

        # Find new head position
        head = snake[0]
        if dir == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif dir == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif dir == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif dir == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]

        # Move the snake using new head
        snake.insert(0, new_head)
        stdscr.addstr(new_head[0], new_head[1], snake_block)

        # Eat food
        if snake[0] == food:
            food = make_food(box, snake)
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(food[0], food[1], food_block)
            stdscr.attroff(curses.color_pair(1))

            # Update current score
            score += 1
            score_msg = 'Score: {}'.format(score)
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(2, 4, score_msg)
            stdscr.attroff(curses.color_pair(2))
            stdscr.refresh()
            continue
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # Game over screen
        if (snake[0][0] in [box[0][0], box[1][0]] or
            snake[0][1] in [box[0][1], box[1][1]] or
            snake[0] in snake[1:]):

            # Upade high score
            high_score = update_high_score()
            if score > high_score:
                with open('score.snake', 'w') as f:
                    f.write(str(score))

            msg = "Game Over!"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.timeout(-1)
            stdscr.getch()
            time.sleep(0.5)
            break

        stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(play_game)
