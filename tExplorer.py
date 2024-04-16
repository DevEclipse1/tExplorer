import curses
from curses import wrapper
import time
import os
import magic
import subprocess

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    cur_pos_y = 1
    pos_y = 1

    directory = os.getcwd()
    files_in_directory = []

    mY,mX = stdscr.getmaxyx()
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, directory, curses.A_UNDERLINE)

        files_in_directory = os.listdir(directory)

        cur_pos_y = 1

        stdscr.addstr(1, 0, "back", curses.A_REVERSE if pos_y == 1 else curses.A_BOLD)

        for file in files_in_directory:
            cur_pos_y += 1

            if cur_pos_y < mY:
                if pos_y == cur_pos_y:
                    attr = curses.A_REVERSE

                    if os.path.isdir(os.path.join(directory, file)):
                        stdscr.addstr(cur_pos_y, 0, "📁 ", curses.color_pair(1) | attr)
                        stdscr.addstr(file, attr)
                    else:
                        stdscr.addstr(cur_pos_y, 0, "📃 ", curses.color_pair(2) | attr)
                        stdscr.addstr(file, attr)
                else:
                    if os.path.isdir(os.path.join(directory, file)):
                        stdscr.addstr(cur_pos_y, 0, "📁 " + file)
                    else:
                        stdscr.addstr(cur_pos_y, 0, "📃 " + file)

        stdscr.refresh()

        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            pos_y = max(1, pos_y - 1)
        elif key == curses.KEY_DOWN:
            pos_y = min(len(files_in_directory) + 1, pos_y + 1)
        elif key == curses.KEY_ENTER or key == 10:
            if pos_y == 1:
                directory = os.path.dirname(directory)
            else:
                selected_file = files_in_directory[pos_y - 2]
                if os.path.isdir(os.path.join(directory, selected_file)):
                    directory = os.path.join(directory, selected_file)
                    pos_y = 1
                else:
                    subprocess.run(["nano", os.path.join(directory, selected_file)])
                    stdscr.clear()
                    break
        elif key == 127 or key == curses.KEY_BACKSPACE:
            directory = os.path.dirname(directory)

wrapper(main)
