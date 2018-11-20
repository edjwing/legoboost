import curses
import os

from time import sleep
from pylgbst import *
from pylgbst.comms import DebugServerConnection
from pylgbst.movehub import MoveHub

import Controller


def main_loop(win):
    # win.nodelay(True)
    win.clear()

    try:
        connection = DebugServerConnection()
        connection.disconnect()
        sleep(3)
        connection = DebugServerConnection()
    except BaseException:
        connection = get_connection_auto()

    try:
        hub = MoveHub(connection)
        sleep(1)
        if hub is not None:
            controller = Controller.Controller(hub)
            while True:
                try:
                    key = win.getkey()
                    if key == os.linesep:
                        break

                    str_key = str(key)
                    win.clear()
                    win.addstr("Input : " + str_key + '\n')

                    if str_key == 'KEY_UP':
                        controller.accel()
                    elif str_key == 'KEY_DOWN':
                        controller.deaccel()
                    elif str_key == 'KEY_LEFT':
                        controller.steer_left()
                    elif str_key == 'KEY_RIGHT':
                        controller.steer_right()

                    win.addstr(controller.__str__())

                except Exception as e:
                    pass
    finally:
        connection.disconnect()


if __name__ == '__main__':
    curses.wrapper(main_loop)
