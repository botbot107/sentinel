from threading import Thread
from pynput.mouse import Controller

from com.config.config_handler import ConfigHandler
from com.model.config import Config


class MouseGuard():

    def __init__(self):
        self.__config: Config = ConfigHandler.instance().get()
        self.__mouse = Controller()
        self.__is_on = False

    def start(self):
        self.__is_on = True
        T = Thread(target=self.__mouse_move)
        T.setDaemon(True)
        T.start()


    def stop(self):
        print('shout down Mouse')
        self.__is_on = False

    def __mouse_move(self):
        self.__before = self.__mouse.position
        while True:
            if self.__is_on == False:
                print('Mouse down')
                exit()
            current = self.__mouse.position
            if self.__before != current:
                print('Movement detected')
            self.__before = current
