import time
import curses
from curses import textpad
import game


menu = ['Play', 'Scoreboard', 'Exit']

def print_menu(stdscr, current_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Rectangle for menu
    title = ' Terminal Snake '
    th = h//2 - len(menu)//2 - 3
    tw = w//2 - len(title)//2
    mbox = [[th, tw-5], [th+len(menu)+5, tw+len(title)+5]]
    textpad.rectangle(stdscr, mbox[0][0], mbox[0][1], mbox[1][0], mbox[1][1])

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(th, tw, title)
    stdscr.attroff(curses.color_pair(1))

    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == current_row:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def game_menu(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row = 0

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        if key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        if key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row] == 'Play':
                game.play_game(stdscr)
            elif menu[current_row] == 'Scoreboard':
                high_score = game.update_high_score()
                h, w = stdscr.getmaxyx()
                msg = ' Highest score: {} '.format(high_score)
                stdscr.attron(curses.color_pair(2))
                stdscr.clear()
                stdscr.addstr(h//2, w//2 - len(msg)//2, msg)
                stdscr.refresh()
                stdscr.attroff(curses.color_pair(2))
                stdscr.getch()
            elif menu[current_row] == 'Exit':
                break

        print_menu(stdscr, current_row)
        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(game_menu)
