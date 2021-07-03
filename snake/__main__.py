import curses
from menu import menu, print_menu, game_menu

curses.wrapper(game_menu)
